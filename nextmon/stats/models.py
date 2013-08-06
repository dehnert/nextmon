import datetime

from django.db import models
from django.db.models import F

import nextbus.models

# Create your models here.
class DailySummary(models.Model):
    day = models.DateField(db_index=True, )
    route = models.ForeignKey(nextbus.models.NBRoute, db_index=True, )
    stop = models.ForeignKey(nextbus.models.NBStop, db_index=True, )
    num_checks = models.IntegerField(help_text="Number of attempts to get a prediction.")
    num_predictions = models.IntegerField(help_text="Number of predictions.")
    num_less_10min = models.IntegerField(help_text="Number of predictions of less than ten minutes.")
    num_less_4min = models.IntegerField(help_text="Number of predictions of less than four minutes.")

    def __unicode__(self, ):
        return u"d=%s, r=%s, s=%s: c=%d, p=%d" % (
            self.day,
            self.route,
            self.stop,
            self.num_checks,
            self.num_predictions,
        )

    @classmethod
    def ensure_summary(cls, entries, data):
        key = (data['route'], data['stop'], data['cycle__effective_date'])
        if not key in entries:
            entry = cls(
                day=data['cycle__effective_date'],
                num_checks=0,
                num_predictions=0,
                num_less_10min=0,
                num_less_4min=0,
            )
            entry.route_id=data['route']
            entry.stop_id=data['stop']
            entries[key] = entry
        return entries[key]

    @classmethod
    def populate(cls, after=None, before=None, ):
        entries = {}

        base = nextbus.models.NBPrediction.objects
        if not after:
            try:
                max_day = cls.objects.order_by('-day')[0]
                after = max_day.day
            except IndexError:
                after = datetime.date.min
        if not before:
            before = datetime.date.today() - datetime.timedelta(days=2)
        base = base.filter(
            cycle__effective_date__lt=before,
            cycle__effective_date__gt=after,
        )
        base = base.values('route', 'stop', 'cycle__effective_date', )


        anno = base.annotate(stat=models.Count('id'))
        for day in anno:
            summary = cls.ensure_summary(entries, day)
            summary.num_checks = day['stat']

        anno = base.exclude(seconds=None)
        anno = anno.annotate(stat=models.Count('id'))
        for day in anno:
            summary = cls.ensure_summary(entries, day)
            summary.num_predictions = day['stat']

        anno = base.filter(seconds__lt=60*10)
        anno = anno.annotate(stat=models.Count('id'))
        for day in anno:
            summary = cls.ensure_summary(entries, day)
            summary.num_less_10min = day['stat']

        anno = base.filter(seconds__lt=60*4)
        anno = anno.annotate(stat=models.Count('id'))
        for day in anno:
            summary = cls.ensure_summary(entries, day)
            summary.num_less_4min = day['stat']

        cls.objects.bulk_create(entries.values(), batch_size=1000)
