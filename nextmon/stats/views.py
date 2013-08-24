# Create your views here.
from django import forms
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, Template
from django.template.loader import get_template

import django_filters

import nextmon.nextbus.models
import nextmon.stats.models

class StatFilter(django_filters.FilterSet):
    start_day= django_filters.DateFilter(name="day", lookup_type="gte")
    end_day = django_filters.DateFilter(name="day", lookup_type="lte")
    route = django_filters.ModelChoiceFilter(queryset=nextmon.nextbus.models.NBRoute.objects)
    stop = django_filters.ModelChoiceFilter(queryset=nextmon.nextbus.models.NBStop.objects)

    class Meta:
        model = nextmon.stats.models.DailySummary
        fields = ['start_day', 'end_day', 'route', 'stop', ]
        order_by = ['day', 'route', 'stop', ]


def summary(request, ):
    qs = nextmon.stats.models.DailySummary.objects.order_by('day')
    f = StatFilter(request.GET, queryset=qs)
    render_results = 'route' in request.GET
    context = {
        'filter': f,
        'render_results': render_results,
    }
    return render_to_response('stats/summary.html', context, context_instance=RequestContext(request), )
