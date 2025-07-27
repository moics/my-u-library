from django.urls import path
from . import views_api

urlpatterns = [

    path('auth/login/', views_api.APILoginView.as_view(), name='api_login'),
    path('auth/logout/', views_api.APILogoutView.as_view(), name='api_logout'),
    path('users/register/', views_api.APIRegisterUserView.as_view(), name='api_register_user'), # Librarian only


    path('books/', views_api.APIBookListView.as_view(), name='api_book_list'),
    path('books/<int:pk>/', views_api.APIBookDetailView.as_view(), name='api_book_detail')
]