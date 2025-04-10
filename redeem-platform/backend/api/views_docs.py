from django.views.generic import TemplateView
from django.http import JsonResponse

class ApiDocsView(TemplateView):
    template_name = 'api/docs.html'

    def get(self, request, *args, **kwargs):
        api_info = {
            'status': 'API is running',
            'endpoints': {
                'admin': '/admin/',
                'api': {
                    'auth': {
                        'login': {
                            'url': '/api/auth/login/',
                            'method': 'POST',
                            'description': 'Login with username and password',
                            'fields': ['username', 'password']
                        },
                        'register': {
                            'url': '/api/auth/register/',
                            'method': 'POST',
                            'description': 'Register a new user account',
                            'fields': ['username', 'email', 'password', 'confirm_password']
                        },
                        'logout': {
                            'url': '/api/auth/logout/',
                            'method': 'POST',
                            'description': 'Logout the current user'
                        }
                    },
                    'profile': {
                        'url': '/api/profile/',
                        'method': 'GET',
                        'description': 'Get user profile information'
                    },
                    'codes': {
                        'url': '/api/codes/',
                        'methods': ['GET', 'POST'],
                        'description': 'List and create redeem codes',
                        'endpoints': {
                            'detail': '/api/codes/<id>/',
                            'active': '/api/codes/?is_active=true'
                        }
                    },
                    'transactions': {
                        'url': '/api/transactions/',
                        'methods': ['GET', 'POST'],
                        'description': 'List and create transactions'
                    }
                }
            }
        }

        if request.headers.get('accept') == 'application/json':
            return JsonResponse(api_info)
        
        return super().get(request, *args, **kwargs)
