from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import path, include
>>>>>>> feature/api
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls')),
]
