from django.contrib import admin
from django.urls import path, include
import home.views
import component.views
import symptom.views
import skincare.views
import search.views
import information.views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.views.home, name = "home"),
    path('comp/', include('component.urls')),
    path('symp/', include('symptom.urls')),
    path('skin/', include('skincare.urls')),
    path('information/',include('information.urls')),
    path('search/', search.views.search, name = "search"),
    path('ajax/',search.views.ajax,name="ajax"),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('sitemap.xml/', TemplateView.as_view(template_name="sitemap.xml", content_type='text/plain'))
]
