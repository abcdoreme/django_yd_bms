from django.db import models

# Create your models here.

class Record(models.Model):
    mac = models.CharField(max_length=18, verbose_name="MAC", unique=True)
    gponsn = models.CharField(max_length=12, verbose_name="SN", unique=True)
    ssid = models.CharField(max_length=10, verbose_name="SSID")
    psk = models.CharField(max_length=16, verbose_name="PSK")
    userpass = models.CharField(max_length=16, verbose_name="UserPwd")    
    password = models.CharField(max_length=32, verbose_name="Password")
    # tr069 = models.CharField(max_length=128, verbose_name="TR069", blank=True, default="")
    haswifi = models.IntegerField(verbose_name="WiFi")
    province = models.CharField(max_length=16, verbose_name="Province", blank=True, default="")
    shortconn = models.BooleanField(max_length=16, verbose_name="Short Connection", blank=True, default=True)
    heartbeat = models.IntegerField(verbose_name="Heartbeat", blank=True, default=120)
    
    def __str__(self):
        return self.mac
    
    # class Meta:
    #     db_table = 'record'

class Device(models.Model):
    mac = models.CharField(max_length=18, verbose_name="MAC", unique=True)
    gponsn = models.CharField(max_length=12, verbose_name="SN", unique=True)
    tr069 = models.CharField(max_length=128, verbose_name="TR069", blank=True, default="")
    status = models.IntegerField(verbose_name="Status", blank=True, default=0)
    pluginList = models.JSONField(default=dict, verbose_name="Plugins", blank=True)
    
    
    def __str__(self):
        return self.mac

