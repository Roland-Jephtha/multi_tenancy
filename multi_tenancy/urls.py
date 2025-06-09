from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from multi_tenancy.views import login, signup, index




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('landlord/', include('landlord.urls'))
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




