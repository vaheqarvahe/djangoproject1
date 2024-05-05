from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up),
    path('sign_in/', views.sign_in),
    path('genres/', views.get_genre),
    path('countries/', views.get_country),
    path('years/', views.get_year),
    path('translations/', views.get_translation),
    path('add_films/', views.add_film),
    path('add_update/', views.update_film),
    path('user/', views.get_user),
    path('get_one_films/<int:pk>/', views.get_one_film),
    path('get_all_films/', views.get_all_film),
    path('get_search/', views.get_search),
    path('get_search/genre/', views.filter_by_genre),
    path('delete/film/<int:pk>/', views.delete_film),
    path('confirm/', views.activate),
    path('payment/<int:pk>/', views.payment),
    path('log_out/', views.logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
