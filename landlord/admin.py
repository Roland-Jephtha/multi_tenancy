from django.contrib import admin
from .models import User, LandLord, Apartment, Dependent, Security, News, BoardNotification

# Register your models here.


admin.site.register(User)
admin.site.register(LandLord)
admin.site.register(Apartment)
admin.site.register(Dependent)
admin.site.register(Security)
admin.site.register(News)
admin.site.register(BoardNotification)