"""UnifiedTT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include,path

from MDAT import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('MDAT.urls')),
    path('new_admin/', views.new_admin, name='new_admin'),
    path('update_database_dss', views.update_database_dss, name='update_database_dss'),
    path('loginsuccess/', views.loginsuccess, name='loginsuccess'),
    path('fill_time_table_using_dss_data/', views.fill_time_table_using_dss_data, name='fill_time_table_using_dss_data'),
    path('student/', views.find_tt_student, name='student'),
    path('find_free_slots/', views.find_free_slots, name='find_free_slots'),

    #path('', TemplateView.as_view(template_name="loginpage.html")),
    path('', views.home, name='home'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),

]
