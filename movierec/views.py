from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .views import UserForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/preview.html')
    else:
        return HttpResponse("Hello, world. You're at the polls index.")

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'movierec/index.html', {})
            else:
                return render(request, 'movierec/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'movierec/login.html', {'error_message': 'Invalid login'})
    return render(request, 'movierec/login.html')