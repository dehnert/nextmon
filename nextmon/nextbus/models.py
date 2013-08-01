import datetime

from django.db import models

DAY_START_OFFSET = datetime.timedelta(hours=6)

class NBAgency(models.Model):
    name = models.SlugField()

    def __unicode__(self, ):
        return u"<Agency: %s>" % (self.name, )

class NBStop(models.Model):
    agency = models.ForeignKey(NBAgency)
    tag = models.SlugField()
    title = models.CharField(max_length=100)
    existent = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('agency', 'tag', ),
        )

    def __unicode__(self, ):
        return u"<Stop: %s.%s>" % (self.agency.name, self.tag, )

class NBRoute(models.Model):
    agency = models.ForeignKey(NBAgency)
    tag = models.SlugField()
    title = models.CharField(max_length=100)
    stops = models.ManyToManyField(NBStop)
    existent = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('agency', 'tag', ),
        )

    def __unicode__(self, ):
        return u"<Route: %s.%s>" % (self.agency.name, self.tag, )

class PredictionCycle(models.Model):
    time = models.DateTimeField(default=datetime.datetime.now, db_index=True, )
    effective_date = models.DateField(db_index=True, )

    def save(self, ):
        if not self.effective_date:
            self.effective_date = (self.time - DAY_START_OFFSET).date()
        super(PredictionCycle, self).save()

    def __unicode__(self, ):
        return u"<Cycle: %d: %s>" % (self.pk, self.time, )

class NBPrediction(models.Model):
    route = models.ForeignKey(NBRoute)
    stop = models.ForeignKey(NBStop)
    dirTag = models.CharField(max_length=20, null=True, blank=True, )
    cycle = models.ForeignKey(PredictionCycle)
    seconds = models.IntegerField(null=True, blank=True, )
    arrival_time = models.DateTimeField(null=True, blank=True, )

    class Meta:
        unique_together = (
            ('route', 'stop', 'cycle', ),
        )
