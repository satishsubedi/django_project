"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from authentication.api.views import activate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/notification/',include('app_notification.api.urls')),
    path('api/hospital/',include('hospital.api.urls')),
    path('api/patient/',include('patient.api.urls')),
    path('api/account/',include('authentication.api.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
  

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)