from datetime import datetime, time, timedelta
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from django.http import HttpResponse
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from .forms import CategoryForm, ProductForm, StockMovementForm
from .models import Category, Product, StockMovement


def es_administrador(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def category_list(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    categories = Category.objects.all()  # pylint: disable=no-member
    return render(
        request,
        'inventory/category_list.html',
        {'categories': categories, 'form': form},
    )


@login_required
def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    low_stock = request.GET.get('low_stock', '')

    products = Product.objects.all()  # pylint: disable=no-member

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        )

    selected_category = None
    if category_id:
        products = products.filter(category_id=category_id)
        selected_category = int(category_id)

    if low_stock == '1':
        products = products.filter(current_stock__lte=F('min_stock'))

    categories = Category.objects.all()  # pylint: disable=no-member

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
        'low_stock': low_stock,
    }
    return render(request, 'inventory/product_list.html', context)


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(
        request,
        'inventory/product_form.html',
        {'form': form, 'title': 'Agregar Producto'},
    )


@login_required
def record_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.user = request.user
            try:
                movement.save()
                return redirect('product_list')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = StockMovementForm()

    return render(request, 'inventory/movement_form.html', {'form': form})


@login_required
def movement_list(request):
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    product_id = request.GET.get('product', '')
    movement_type = request.GET.get('movement_type', '')
    search_query = request.GET.get('q', '')

    movements = StockMovement.objects.select_related(  # pylint: disable=no-member
        'product', 'user'
    ).all()

    # Aplicar Filtros
    if date_from:
        movements = movements.filter(created_at__date__gte=date_from)
    if date_to:
        movements = movements.filter(created_at__date__lte=date_to)
    if product_id:
        movements = movements.filter(product_id=product_id)
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    if search_query:
        movements = movements.filter(
            Q(reason__icontains=search_query)
            | Q(entity_name__icontains=search_query)
            | Q(user__username__icontains=search_query)
        )

    movements = movements.order_by('-created_at')

    annotated_movements = movements.annotate(
        subtotal=ExpressionWrapper(
            Cast(F('quantity'), output_field=DecimalField(max_digits=12, decimal_places=2))
            * F('product__price'),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
    )

    total_out = (
        annotated_movements.filter(movement_type='OUT').aggregate(
            total=Sum('subtotal')
        )['total']
        or 0
    )
    total_in = (
        annotated_movements.filter(movement_type='IN').aggregate(
            total=Sum('subtotal')
        )['total']
        or 0
    )
    units_out = (
        movements.filter(movement_type='OUT').aggregate(total=Sum('quantity'))[
            'total'
        ]
        or 0
    )
    units_in = (
        movements.filter(movement_type='IN').aggregate(total=Sum('quantity'))[
            'total'
        ]
        or 0
    )

    products = Product.objects.all()  # pylint: disable=no-member

    context = {
        'movements': annotated_movements,
        'products': products,
        'date_from': date_from,
        'date_to': date_to,
        'selected_product': (
            int(product_id) if product_id and product_id.isdigit() else None
        ),
        'selected_type': movement_type,
        'search_query': search_query,
        'total_out': total_out,
        'total_in': total_in,
        'units_out': units_out,
        'units_in': units_in,
        'total_records': movements.count(),
    }
    return render(request, 'inventory/movement_list.html', context)


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)  # pylint: disable=no-member
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'inventory/product_form.html',
        {'form': form, 'title': 'Editar Producto'},
    )


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)  # pylint: disable=no-member
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(
        request, 'inventory/product_confirm_delete.html', {'product': product}
    )


@login_required
def export_movements_excel(request):
    """Exporta los movimientos filtrados a un archivo Excel (.xlsx)"""
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    product_id = request.GET.get('product', '')
    movement_type = request.GET.get('movement_type', '')
    search_query = request.GET.get('q', '')

    movements = StockMovement.objects.select_related('product', 'user').all()  # pylint: disable=no-member

    if date_from:
        movements = movements.filter(created_at__date__gte=date_from)
    if date_to:
        movements = movements.filter(created_at__date__lte=date_to)
    if product_id:
        movements = movements.filter(product_id=product_id)
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    if search_query:
        movements = movements.filter(
            Q(reason__icontains=search_query)
            | Q(entity_name__icontains=search_query)
            | Q(user__username__icontains=search_query)
        )

    wb = Workbook()
    ws = wb.active
    ws.title = "Historial StockFlow"

    headers = ['Fecha', 'Producto', 'SKU', 'Tipo', 'Cantidad', 'Precio Unit.', 'Subtotal Est.', 'Motivo / Entidad', 'Usuario']
    ws.append(headers)

    for m in movements:
        subtotal = m.quantity * m.product.price
        ws.append([
            m.created_at.strftime('%d/%m/%Y %H:%M'),
            m.product.name,
            m.product.sku,
            m.get_movement_type_display(),
            m.quantity,
            float(m.product.price),
            float(subtotal),
            m.reason or '-',
            m.user.username if m.user else 'Sistema'
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Historial_Movimientos_StockFlow.xlsx"'
    wb.save(response)
    return response


@login_required
def export_movements_pdf(request):
    """Exporta los movimientos filtrados a un documento PDF"""
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    product_id = request.GET.get('product', '')
    movement_type = request.GET.get('movement_type', '')
    search_query = request.GET.get('q', '')

    movements = StockMovement.objects.select_related('product', 'user').all()  # pylint: disable=no-member

    if date_from:
        movements = movements.filter(created_at__date__gte=date_from)
    if date_to:
        movements = movements.filter(created_at__date__lte=date_to)
    if product_id:
        movements = movements.filter(product_id=product_id)
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    if search_query:
        movements = movements.filter(
            Q(reason__icontains=search_query)
            | Q(entity_name__icontains=search_query)
            | Q(user__username__icontains=search_query)
        )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Movimientos_StockFlow.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("<b>StockFlow - Reporte de Movimientos</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    data = [['Fecha', 'Producto', 'Tipo', 'Cant.', 'Subtotal', 'Usuario']]
    for m in movements:
        subtotal = m.quantity * m.product.price
        data.append([
            m.created_at.strftime('%d/%m/%Y'),
            m.product.name[:20],
            m.get_movement_type_display(),
            str(m.quantity),
            f"${subtotal:.2f}",
            m.user.username if m.user else 'Sistema'
        ])

    table = Table(data, colWidths=[80, 150, 70, 50, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))

    elements.append(table)
    doc.build(elements)
    return response


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def dashboard(request):
    """Vista principal con métricas e indicadores de rendimiento (KPIs)"""
    total_products = Product.objects.count()  # pylint: disable=no-member
    total_categories = Category.objects.count()  # pylint: disable=no-member

    inventory_value = Product.objects.aggregate(  # pylint: disable=no-member
        total_val=Sum(
            ExpressionWrapper(
                F('price') * F('current_stock'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    )['total_val'] or 0

    low_stock_count = Product.objects.filter(  # pylint: disable=no-member
        current_stock__lte=F('min_stock')
    ).count()

    categories_data = Category.objects.annotate(  # pylint: disable=no-member
        product_count=Count('products')
    ).values('name', 'product_count')

    cat_labels = [c['name'] for c in categories_data]
    cat_counts = [c['product_count'] for c in categories_data]

    top_sales = (
        StockMovement.objects.filter(movement_type='OUT')  # pylint: disable=no-member
        .values('product__name')
        .annotate(total_out=Sum('quantity'))
        .order_by('-total_out')[:5]
    )

    top_labels = [item['product__name'] for item in top_sales]
    top_counts = [item['total_out'] for item in top_sales]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'inventory_value': inventory_value,
        'low_stock_count': low_stock_count,
        'cat_labels': cat_labels,
        'cat_counts': cat_counts,
        'top_labels': top_labels,
        'top_counts': top_counts,
    }
    return render(request, 'inventory/dashboard.html', context)


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def executive_report(request):
    """Reporte Ejecutivo de Rotación de Inventario y Análisis de Capital"""
    days_range = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days_range)

    products = Product.objects.all()  # pylint: disable=no-member
    report_data = []

    total_units_sold = 0
    total_revenue_estimated = 0.0
    stagnant_products_count = 0

    for product in products:
        out_movements = StockMovement.objects.filter(  # pylint: disable=no-member
            product=product,
            movement_type='OUT',
            created_at__gte=start_date
        ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

        in_movements = StockMovement.objects.filter(  # pylint: disable=no-member
            product=product,
            movement_type='IN',
            created_at__gte=start_date
        ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

        # Cálculo de Índice de Rotación (Unidades Vendidas / Stock Actual)
        turnover_rate = round(out_movements / product.current_stock, 2) if product.current_stock > 0 else float(out_movements)

        if turnover_rate >= 1.5:
            status = 'Alta'
            status_color = 'emerald'
        elif turnover_rate >= 0.5:
            status = 'Media'
            status_color = 'amber'
        elif out_movements > 0:
            status = 'Baja'
            status_color = 'rose'
        else:
            status = 'Sin Movimiento'
            status_color = 'slate'
            stagnant_products_count += 1

        total_units_sold += out_movements
        total_revenue_estimated += float(out_movements * product.price)

        report_data.append({
            'product': product,
            'in_units': in_movements,
            'out_units': out_movements,
            'turnover_rate': turnover_rate,
            'status': status,
            'status_color': status_color,
            'capital_in_stock': product.current_stock * product.price,
        })

    context = {
        'days_range': days_range,
        'report_data': report_data,
        'total_units_sold': total_units_sold,
        'total_revenue_estimated': total_revenue_estimated,
        'stagnant_products_count': stagnant_products_count,
    }
    return render(request, 'inventory/executive_report.html', context)


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def export_executive_excel(request):
    """Exporta el Análisis de Rotación del Reporte Ejecutivo a un archivo Excel (.xlsx)"""
    days_range = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days_range)

    wb = Workbook()
    ws = wb.active
    ws.title = f"Rotación ({days_range}d)"

    headers = ['SKU', 'Producto', 'Stock Actual', 'Entradas', 'Salidas', 'Índice Rotación', 'Capital en Stock', 'Nivel de Rotación']
    ws.append(headers)

    for product in Product.objects.all():  # pylint: disable=no-member
        out_movements = StockMovement.objects.filter(  # pylint: disable=no-member
            product=product, movement_type='OUT', created_at__gte=start_date
        ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

        in_movements = StockMovement.objects.filter(  # pylint: disable=no-member
            product=product, movement_type='IN', created_at__gte=start_date
        ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

        turnover_rate = round(out_movements / product.current_stock, 2) if product.current_stock > 0 else float(out_movements)

        if turnover_rate >= 1.5:
            status = 'Alta'
        elif turnover_rate >= 0.5:
            status = 'Media'
        elif out_movements > 0:
            status = 'Baja'
        else:
            status = 'Sin Movimiento'

        ws.append([
            product.sku,
            product.name,
            product.current_stock,
            in_movements,
            out_movements,
            turnover_rate,
            float(product.current_stock * product.price),
            status
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="Reporte_Ejecutivo_Rotacion_{days_range}dias.xlsx"'
    wb.save(response)
    return response


@login_required
@user_passes_test(es_administrador, login_url='product_list')
def export_executive_pdf(request):
    """Exporta el Análisis de Rotación del Reporte Ejecutivo a un documento PDF"""
    days_range = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days_range)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Ejecutivo_Rotacion_{days_range}dias.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph(f"<b>StockFlow - Reporte Ejecutivo de Rotación ({days_range} días)</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 14))

    data = [['SKU', 'Producto', 'Stock', 'Ent.', 'Sal.', 'Índice', 'Estado']]

    for product in Product.objects.all():  # pylint: disable=no-member
        out_movements = StockMovement.objects.filter(  # pylint: disable=no-member
            product=product, movement_type='OUT', created_at__gte=start_date
        ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

        in_movements = StockMovement.objects.filter(  # pylint: disable=no-member
            product=product, movement_type='IN', created_at__gte=start_date
        ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

        turnover_rate = round(out_movements / product.current_stock, 2) if product.current_stock > 0 else float(out_movements)

        if turnover_rate >= 1.5:
            status = 'Alta'
        elif turnover_rate >= 0.5:
            status = 'Media'
        elif out_movements > 0:
            status = 'Baja'
        else:
            status = 'Sin Movimiento'

        data.append([
            product.sku,
            product.name[:22],
            str(product.current_stock),
            f"+{in_movements}",
            f"-{out_movements}",
            str(turnover_rate),
            status
        ])

    table = Table(data, colWidths=[65, 160, 50, 45, 45, 55, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))

    elements.append(table)
    doc.build(elements)
    return response



