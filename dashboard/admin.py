from django.contrib import admin
from .models import Meeting, Message, Slot, Slotsopento

admin.site.register(Meeting)
admin.site.register(Slot)
admin.site.register(Slotsopento)
admin.site.register(Message)
# Register your models here.
