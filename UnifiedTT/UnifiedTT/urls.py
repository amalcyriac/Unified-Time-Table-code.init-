from django.contrib import admin
from django.urls import include,path

from MDAT import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('MDAT.urls')),
    path('new_admin', views.new_admin, name='new_admin'),
    path('student', views.find_tt_student, name='student'),
]
