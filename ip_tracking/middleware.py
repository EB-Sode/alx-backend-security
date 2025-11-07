from django.http import HttpResponseForbidden
from django.core.cache import cache
import ipapi
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    """Middleware to log IP address, timestamp, path, and geolocation of every request."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client's IP address
        ip_address = self.get_client_ip(request)
        
        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("403 Forbidden: Your IP address has been blocked.")
        
        # Get the request path
        path = request.path
        
        # Get geolocation data (with caching)
        country, city = self.get_geolocation(ip_address)
        
        # Log the request to the database
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            country=country,
            city=city
        )
        
        # Continue processing the request
        response = self.get_response(request)
        return response

    def get_geolocation(self, ip_address):
        """Get geolocation data for an IP address with 24-hour caching."""
        cache_key = f"geo_{ip_address}"
        
        # Try to get cached data
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Skip geolocation for local/private IPs
        if self.is_private_ip(ip_address):
            return None, None
        
        # Fetch geolocation data using ipapi
        try:
            location = ipapi.location(ip_address)
            
            if location:
                country = location.get('country_name')
                city = location.get('city')
            else:
                country = None
                city = None
                
        except Exception as e:
            # If geolocation fails, return None values
            print(f"Geolocation error for {ip_address}: {str(e)}")
            country = None
            city = None
        
        # Cache the result for 24 hours (86400 seconds)
        geo_data = (country, city)
        cache.set(cache_key, geo_data, 86400)
        
        return country, city
    
    def is_private_ip(self, ip):
        """Check if IP is private/local."""
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return True
        
        # Check for private IP ranges
        parts = ip.split('.')
        if len(parts) == 4:
            try:
                first_octet = int(parts[0])
                second_octet = int(parts[1])
                
                # Private IP ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
                if first_octet == 10:
                    return True
                if first_octet == 172 and 16 <= second_octet <= 31:
                    return True
                if first_octet == 192 and second_octet == 168:
                    return True
            except ValueError:
                pass
        
        return False

    def get_client_ip(self, request):
        """Extract the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Get the first IP in the chain (client's real IP)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    