from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

admin.site.site_header="Smart Finance Manager"
admin.site.index_title="transcation tracker"
admin.site.site_header='All Transcations'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect root to finance
    path('', lambda request: redirect('/finance/', permanent=False)),
    path('finance/', include('home.urls'))
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
