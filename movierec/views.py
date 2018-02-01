from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movierec/preview.html')
    else:
        return HttpResponse("Hello, world. You're at the polls index.")