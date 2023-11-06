from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Define a URL pattern to capture an integer parameter
    path('watch/<int:param>/', views.watch, name='watch'),
    path('manage/<int:param>/', views.manage, name='manage'),

    path('search', views.search, name='search'),  # Uses a query string
    path('login', views.login, name='login'),
    path('upload', views.upload, name='upload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)