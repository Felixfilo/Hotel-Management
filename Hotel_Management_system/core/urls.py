from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('dashbord', views.dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/create/', views.reservation_create, name='reservation_create'),
    path('reservations/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
     path('reservations/<int:reservation_id>/confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('reservations/<int:reservation_id>/update-payment/', views.update_payment, name='update_payment'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]