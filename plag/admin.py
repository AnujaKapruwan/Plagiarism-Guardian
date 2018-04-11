from django.contrib import admin
from plag.models import  ProtectedResource, ScanResult, ScanLog, Query

admin.site.register(ProtectedResource)
admin.site.register(ScanResult)
admin.site.register(ScanLog)
admin.site.register(Query)