# Create your views here.
from django import forms
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, Template
from django.template.loader import get_template

import django_filters

import nextmon.nextbus.models
import nextmon.stats.models

class StatFilter(django_filters.FilterSet):
    day = django_filters.DateRangeFilter()
    route = django_filters.ModelChoiceFilter(queryset=nextmon.nextbus.models.NBRoute.objects)
    stop = django_filters.ModelChoiceFilter(queryset=nextmon.nextbus.models.NBStop.objects)

    class Meta:
        model = nextmon.stats.models.DailySummary
        fields = ['day', 'route', 'stop', ]


def summary(request, ):
    f = StatFilter(request.GET, queryset=nextmon.stats.models.DailySummary.objects.all())
    context = {
        'filter': f,
    }
    return render_to_response('stats/summary.html', context, context_instance=RequestContext(request), )
