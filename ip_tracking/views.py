from django.http import JsonResponse
from ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate, login

from django.http import HttpResponse

# Optional: custom handler
def rate_limit_exceeded_view(request, exception=None):
    return JsonResponse({"error": "Rate limit exceeded. Please try again later."}, status=429)

# Example login view
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
def login_view(request):
    """
    Authenticated users: max 10 requests/minute
    Anonymous users: max 5 requests/minute
    """
    # If anonymous, apply tighter limit
    if not request.user.is_authenticated:
        return _anonymous_login_view(request)

    # Process login for authenticated
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        return JsonResponse({"message": "Login successful"})
    return JsonResponse({"error": "Invalid credentials"}, status=400)

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def _anonymous_login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        return JsonResponse({"message": "Login successful"})
    return JsonResponse({"error": "Invalid credentials"}, status=400)

