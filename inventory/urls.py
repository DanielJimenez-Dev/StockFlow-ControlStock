from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('nuevo/', views.product_create, name='product_create'),
    path('editar/<int:pk>/', views.product_update, name='product_update'),
    path('eliminar/<int:pk>/', views.product_delete, name='product_delete'),
    path('movimiento/', views.record_movement, name='record_movement'),
    path('historial/', views.movement_list, name='movement_list'),
    path('historial/exportar/excel/', views.export_movements_excel, name='export_movements_excel'),
    path('historial/exportar/pdf/', views.export_movements_pdf, name='export_movements_pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('executive-report/', views.executive_report, name='executive_report'),
    path('executive-report/export/excel/', views.export_executive_excel, name='export_executive_excel'),
    path('executive-report/export/pdf/', views.export_executive_pdf, name='export_executive_pdf'),
]