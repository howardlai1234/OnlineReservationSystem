from django.contrib import admin
from ORS.model import Meeting, Message, Slot, Slotsopento

admin.site.Register(Meeting)
admin.site.Register(Slot)
admin.site.Register(Slotsopento)
admin.site.Register(Message)
# Register your models here.
