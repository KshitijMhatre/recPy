from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm
import json,requests


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/preview.html')
    else:
        query = request.GET.get("q")
        if query:
            rest_api ='https://www.omdbapi.com/?apikey=feaa306&s='            
            result = requests.get(rest_api+query)
            data = result.json()


            return render(request, 'movierec/index.html', {'result':data })
        else:
            return render(request, 'movierec/index.html')        

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)                
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
                return render(request, 'movierec/index.html', {})
    context = {
        "form": form,
    }
    return render(request, 'movierec/register.html', context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'movierec/login.html', context)


def detail(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/login.html')
    else:
        user = request.user
        mov_id= request.GET.get("mov_id")
        
        rest_api ='https://www.omdbapi.com/?apikey=feaa306&i='            
        result = requests.get(rest_api+mov_id)
        data = result.json()        
                
        return render(request, 'movierec/detail.html', {'data': data, 'user': user})


# @login_required
# @transaction.atomic
#need to add pages
def update_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/preview.html')
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })