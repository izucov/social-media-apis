from rest_framework.throttling import UserRateThrottle


class CustomThrottle(UserRateThrottle):
    rate = '3/minute'

    def allow_request(self, request, view):
        if request.method == "POST":
            return super().allow_request(request, view)
        return True
