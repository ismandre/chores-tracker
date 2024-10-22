from django.contrib import admin

from .models import Chore, Room, History, HistoryEntry

admin.site.register(Chore)
admin.site.register(Room)
admin.site.register(History)
admin.site.register(HistoryEntry)
