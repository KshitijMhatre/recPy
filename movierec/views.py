from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm

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

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'movierec/index.html', {})
    context = {
        "form": form,
    }
    return render(request, 'movierec/register.html', context)