from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm
import json,requests
from .models import Ratings
from . import myconfig


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/preview.html')
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
        old_rating=0
        try:                 
            obj = Ratings.objects.get(uid=user.profile.u_id,imdb=mov_id)
            old_rating=obj.rating                 
        except Ratings.DoesNotExist:
            pass        
        rest_api ='https://www.omdbapi.com/?apikey='+myconfig.mov_key+'&i='            
        result = requests.get(rest_api+mov_id+'&plot=full')
        data = result.json()        
                
        return render(request, 'movierec/detail.html', {'data': data, 'user': user,'rating':old_rating})


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
    return render(request, 'movierec/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def search_movies(request):
    if request.method== "POST":
        query = request.POST.get("q")
        if query:
            rest_api ='https://www.omdbapi.com/?apikey='+myconfig.mov_key+'&s='            
            result = requests.get(rest_api+query)
            data = result.json()

            return render(request, 'movierec/search_result.html', {'result':data })
        else:
            return render(request, 'movierec/search_result.html')


from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *

client = RecombeeClient(myconfig.mov_db,myconfig.token)


def recommend_movies(request):
    if request.method== "POST":
        uid = request.POST.get("uid")        
        if uid:
            recommended= client.send(RecommendItemsToUser(uid ,5)) 
            data={"recomms":[]}
            rest_api ='https://www.omdbapi.com/?apikey='+myconfig.mov_key+'&i='
            for item in recommended["recomms"]:   
                fid = item["id"].replace('tt','')
                result = requests.get(rest_api+'tt'+fid)                       
                data["recomms"].append(result.json())            
            return render(request, 'movierec/recom_result.html', {'result':data })
        else:
            return render(request, 'movierec/recom_result.html')

def rate_movies(request):
    if request.method == "POST":
        my_uid=request.POST.get("uid")        
        my_imdb=request.POST.get("imdb")        
        my_rating=float(request.POST.get("rating"))        
        obj,created= Ratings.objects.update_or_create(uid=my_uid,imdb=my_imdb,defaults = {'rating':my_rating})        
        if(created):            
            client.send(AddRating(my_uid,my_imdb[2:],(my_rating-3)/2,cascade_create= True))
        else:            
            client.send(DeleteRating(my_uid,my_imdb[2:]))
            client.send(AddRating(my_uid,my_imdb[2:],(my_rating-3)/2,cascade_create= True))
    return render(request, 'movierec/recom_result.html')

def related_movies(request):
    if request.method== "POST":
        uid = request.POST.get("uid")  
        imdb = request.POST.get("imdb")      
        if uid:
            recommended= client.send(RecommendItemsToItem(imdb[2:] ,uid ,5)) 
            data={"related":[]}
            rest_api ='https://www.omdbapi.com/?apikey='+myconfig.mov_key+'&i='
            for item in recommended["recomms"]:   
                fid = item["id"].replace('tt','')
                result = requests.get(rest_api+'tt'+fid)                 
                data["related"].append(result.json())            
            return render(request, 'movierec/related_result.html', {'result':data })
        else:
            return render(request, 'movierec/related_result.html')
