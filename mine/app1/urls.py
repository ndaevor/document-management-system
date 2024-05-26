from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app1 import views
from django.urls import path
from .views import HomePage, SignuPage, loginPage, LogoutPage, upload_document, document_download, delete_document, settingsPage
from django.urls import path, include
urlpatterns = [
    
       
    path('',views.SignuPage,name='signup'),
    path('login/', views.loginPage, name='login'),
    path('home/',views.HomePage,name='home'),
    path('settings/', views.settingsPage, name='settings'),
    path('logout/',views.LogoutPage,name='logout'),
    path('upload/', views.upload_document, name='upload_document'),
    path('download/<int:document_id>/', views.document_download, name='document_download'),
    path('document/delete/<int:document_id>/', views.delete_document, name='document_delete'),
    
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)