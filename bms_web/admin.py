from django.contrib import admin
from .models import Record, Device

# Register your models here.

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('mac', 'gponsn', 'userpass', 'ssid', 'psk', 'password')
    list_filter = ('mac', 'gponsn')
    search_fields = ('mac','gponsn')
    list_editable = ('userpass', 'ssid', 'psk', 'password')
    
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'gponsn', 'tr069', 'status', 'pluginList')
    list_filter = ('mac', 'gponsn')
    search_fields = ('mac','gponsn')
    list_editable = ('tr069', 'status', 'pluginList')
