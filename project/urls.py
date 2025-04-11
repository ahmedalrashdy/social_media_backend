
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('accounts/', include('accounts.urls')),
    
    
    
    #api
    path('api/v1/auth/', include('accounts.api_urls')),
     path('api/v1/personal-posts/', include('personal_posts.urls')),
]




from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


