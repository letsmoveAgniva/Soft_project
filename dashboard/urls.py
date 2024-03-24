from django.urls import path
from . import views


urlpatterns=[
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/',views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>/',views.staff_detail, name='dashboard-staff-detail'),
    path('product/',views.product, name='dashboard-product'),
    path('product/delete/<int:pk>/',views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/',views.product_update, name='dashboard-product-update'),
    path('order/',views.order, name='dashboard-order'),
    path('order/update/<int:pk>/',views.order_update, name='dashboard-order-update'),
    path('sales_statistics/', views.sales_statistics, name='sales_statistics'),
    path('edit-information/', views.edit_information, name='edit-information'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing/', views.billing, name='billing'),
]
