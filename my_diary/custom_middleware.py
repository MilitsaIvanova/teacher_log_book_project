from django.shortcuts import redirect

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not (request.user.is_staff or request.user.is_superuser):
            return redirect('/restricted-access/')  # Redirect to a restricted access page
        return self.get_response(request)