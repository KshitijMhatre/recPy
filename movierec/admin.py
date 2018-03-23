from django.contrib import admin

# Register your models here.
from movierec.models import Profile,Ratings
admin.site.register(Profile)
admin.site.register(Ratings)