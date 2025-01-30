from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.contrib import admin

from pages import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_phones, name='show_phones'),
    path('places/<int:location_id>/', views.get_location, name='get_location'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
