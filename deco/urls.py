"""
URL configuration for deco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from ananta import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('update-enquiry/<int:pk>/', views.update_enquiry, name='update_enquiry'),
    path('delete-enquiry/<int:pk>/', views.delete_enquiry, name='delete_enquiry'),
    path('staff-access/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='logout'),
    path('dashboard/product/add/', views.add_product, name='add_product'),
    path('dashboard/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('upload-gallery/', views.upload_gallery, name='upload_gallery'),
    path('delete-gallery/<int:pk>/', views.delete_gallery, name='delete_gallery'),
]



# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)