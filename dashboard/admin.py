from django.contrib import admin
from .models import Meeting, Message, Slot, Groupdetail

admin.site.register(Meeting)
admin.site.register(Slot)
admin.site.register(Message)
admin.site.register(Groupdetail)

# Register your models here.
