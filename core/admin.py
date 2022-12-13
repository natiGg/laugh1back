from django.contrib import admin
from authentication.models import User

from core.models import UserProfile
from core.models import Joke,Reaction,Comment,Roast

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Joke)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Roast)
