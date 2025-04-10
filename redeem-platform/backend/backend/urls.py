from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse

def api_root(request):
    if request.headers.get('accept') == 'application/json':
        return JsonResponse({
            'status': 'API is running',
            'endpoints': {
                'admin': '/admin/',
                'api': {
                    'auth': {
                        'login': '/api/auth/login/',
                        'register': '/api/auth/register/',
                        'logout': '/api/auth/logout/',
                    },
                    'profile': '/api/profile/',
                    'codes': '/api/codes/',
                    'transactions': '/api/transactions/',
                }
            }
        })
    return render(request, 'api/docs.html')

urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
