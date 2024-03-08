from django.http import JsonResponse


def ping(request) -> JsonResponse:
    """
    A simple view to check if the server is running
    """
    return JsonResponse({"status": "OK"})
