from django.http import HttpResponse


# Create your views here.
def register(request):
    return HttpResponse("<h1>Welcome to the registration page.</h1>")