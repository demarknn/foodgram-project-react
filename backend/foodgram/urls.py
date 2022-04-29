from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

import api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api.urls)),
    # path('api/', include('djoser.urls')),
    # path('api/', include('djoser.urls.jwt')),
    path('api/auth/token/login/', views.obtain_auth_token),
]
