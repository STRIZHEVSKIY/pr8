from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CityViewSet, PDFFileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', CityViewSet)
router.register(r'pdf_files', PDFFileViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('error/', views.error_view, name='error'),
    path('books/', views.city_list, name='city_list'),
    path('books/<int:id>/', views.city_details, name='city_details'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('download_pdf/', views.download_list, name='download_list'),
    path('download_pdf/<int:id>/', views.download_pdf, name='download_pdf'),
    path('save_image/', views.save_image, name='save_image'),
    path('statistics/', views.statistics, name='statistics'),
    path('generate_fixtures/', views.generate_fixtures, name='generate_fixtures'),
    path('settings/', views.settings_view, name='settings'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
