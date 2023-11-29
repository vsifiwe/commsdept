from django.contrib import admin
from .models import Ticket, User, FollowUp

# Register your models here.
admin.site.register(Ticket)
admin.site.register(User)
admin.site.register(FollowUp)
