from django import forms
from .models import Category, Product, StockMovement

class CategoryForm(forms.ModelForm):
    class Meta:

        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' focus:ring-2 focus:ring-blue-500 focus:outline-none'
                    ),
                    'placeholder': 'Ej: Electrónica, Indumentaria...',
                }
            ),
        }

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product
        fields = [
            'sku',
            'name',
            'category',
            'description',
            'price',
            'current_stock',
            'min_stock',
            'image_url',
        ]
        widgets = {
            'sku': forms.TextInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    ),
                    'rows': 3,
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    ),
                    'step': '0.01',
                }
            ),
            'current_stock': forms.NumberInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'min_stock': forms.NumberInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'image_url': forms.URLInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    ),
                    'placeholder': 'https://images.unsplash.com/...',
                }
            ),
        }

class StockMovementForm(forms.ModelForm):

    class Meta:

        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reason', 'entity_name']
        widgets = {
            'product': forms.Select(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'movement_type': forms.Select(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    )
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    ),
                    'min': '1',
                }
            ),
            'reason': forms.TextInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    ),
                    'placeholder': 'Ej. Venta local, Compra de stock...',
                }
            ),
            'entity_name': forms.TextInput(
                attrs={
                    'class': (
                        'w-full p-2 border border-gray-300 rounded-lg text-sm'
                        ' mb-4'
                    ),
                    'placeholder': (
                        'Ej. Distribuidora Sur S.A. / Juan Pérez'
                    ),
                }
            ),
        }
