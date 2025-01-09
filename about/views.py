from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View


class WhoAmIView(View):
    def get(self, request, *args, **kwargs):
        client_ip = self.get_client_ip(request)
        client_browser = request.META.get("HTTP_USER_AGENT", "Unknown")
        server_time = now()

        data = {
            "client_ip": client_ip,
            "client_browser": client_browser,
            "server_time": server_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JsonResponse(data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "Unknown")
        return ip
