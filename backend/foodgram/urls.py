from django.contrib import admin
from django.urls import include, path

import api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
