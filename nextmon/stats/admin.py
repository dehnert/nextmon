from django.contrib import admin

import stats.models

class Admin_DailySummary(admin.ModelAdmin):
    list_display = (
        'id',
        'day', 'route', 'stop',
        'num_checks', 'num_predictions', 'num_less_10min', 'num_less_4min',
    )
    list_display_links = ( 'id', )
    date_hierarchy = 'day'
    list_filter = ['route', 'stop', ]
admin.site.register(stats.models.DailySummary, Admin_DailySummary)

