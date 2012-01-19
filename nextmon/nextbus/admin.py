from django.contrib import admin

import nextbus.models

class Admin_NBAgency(admin.ModelAdmin):
    list_display = ( 'id', 'name', )
    list_display_links = ( 'id', 'name', )
admin.site.register(nextbus.models.NBAgency, Admin_NBAgency)

class Admin_NBRoute(admin.ModelAdmin):
    list_display = ( 'id', 'tag', 'title', 'existent', 'enabled', )
    list_display_links = ( 'id', 'tag', 'title', )
admin.site.register(nextbus.models.NBRoute, Admin_NBRoute)

class Admin_NBStop(admin.ModelAdmin):
    list_display = ( 'id', 'tag', 'title', 'agency', 'existent', 'enabled', )
    list_display_links = ( 'id', 'tag', 'title', )
admin.site.register(nextbus.models.NBStop, Admin_NBStop)

class Admin_PredictionCycle(admin.ModelAdmin):
    list_display = ( 'id', 'time', )
admin.site.register(nextbus.models.PredictionCycle, Admin_PredictionCycle)

class Admin_NBPrediction(admin.ModelAdmin):
    list_display = ( 'route', 'stop', 'cycle', 'seconds', 'arrival_time', )
admin.site.register(nextbus.models.NBPrediction, Admin_NBPrediction)

