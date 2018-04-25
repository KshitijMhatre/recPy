from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json,requests
from movierec import myconfig


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/preview.html')
    else:                
        return render(request,'bookrec/index.html')      



from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *

client = RecombeeClient(myconfig.book_db,myconfig.btoken)


def detail(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/login.html')
    else:
        user = request.user
        isbn_id= request.GET.get("isbn_id")
        
        result = client.send(GetItemValues(isbn_id))
        result = formatRes(result)
        return render(request, 'bookrec/detail.html', {'res': result})


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


def search_books(request):
    if request.method== "POST":
        query = request.POST.get("q")
        if query:
            result = client.send(ListItems(filter="\""+query+"\" in 'Book-Title'" , return_properties = True, included_properties = ['Book-Title','Book-Author']))
            data = {"Search": result}
            data = json.dumps(data)

            return render(request, 'bookrec/search_result.html', {'result':data })
        else:
            return render(request, 'bookrec/search_result.html')




def recommend_books(request):
    if request.method== "POST":
        uid = request.POST.get("uid")        
        if uid:
            recommended= client.send(RecommendItemsToUser(10, 10,return_properties = True,included_properties = ['Book-Title','Book-Author','Image-URL-L']))                        
            return render(request, 'bookrec/recom_result.html', {'result':json.dumps(recommended) })
        else:
            return render(request, 'bookrec/recom_result.html')

def rate_books(request):
    if request.method == "POST":
        my_uid=request.POST.get("uid")        
        my_isbn=request.POST.get("isbn")        
        my_rating=float(request.POST.get("rating"))        
        
        client.send(AddRating(my_uid,my_isbn,(my_rating-5)/5,cascade_create= True))
    return render(request, 'bookrec/recom_result.html')

def related_books(request):
    if request.method== "POST":
        uid = request.POST.get("uid")  
        isbn = request.POST.get("isbn")      
        if uid:
            recommended= client.send(RecommendItemsToItem(isbn ,uid ,5))                         
            data = {"related":[]}
            for item in recommended["recomms"]:                   
                data["related"].append(item)            
            return render(request, 'bookrec/related_result.html', {'result':data})
        else:
            return render(request, 'bookrec/related_result.html')

def formatRes(res):
    formated={}
    for k in res:
        if '-' in k:
            formated[k.replace('-','')]=res[k]
        else:
            formated[k]=res[k]
    return formated