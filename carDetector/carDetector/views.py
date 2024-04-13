from django.http import HttpResponse

def health(request):
    return HttpResponse("OK")

def index(request):
    return HttpResponse("Hello, world. You're at the carDetector index.")