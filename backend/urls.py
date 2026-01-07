"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static 

from rest_framework import permissions
from drf_yasg.views import  get_schema_view
from drf_yasg import  openapi

admin.site.site_header = "پنل مدیریت فروشگاه دینوما"
admin.site.site_title = "مدیریت سایت "
admin.site.index_title = " خوش آمدید به داشبورد مدیریت دینوما" 


schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce Back-End API",
        default_version='v1',
        description="This is the Documentation for the backend API",
        contact=openapi.Contact(email="m.dahmardeh16@gmail.com"),
        license=openapi.License(name= "دینوما")
    ),
    public=True,
    permission_classes = (permissions.AllowAny,)
)
urlpatterns = [
    path('admin/', admin.site.urls ),
    path('api/v1/' , include('api.urls')),

    #Documentations
    path("" , schema_view.with_ui('swagger' , cache_timeout =0 ) , 
    name='schema-swagger-ui')

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)