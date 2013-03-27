# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'PredictionCycle', fields ['time']
        db.create_index('nextbus_predictioncycle', ['time'])


    def backwards(self, orm):
        # Removing index on 'PredictionCycle', fields ['time']
        db.delete_index('nextbus_predictioncycle', ['time'])


    models = {
        'nextbus.nbagency': {
            'Meta': {'object_name': 'NBAgency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'nextbus.nbprediction': {
            'Meta': {'unique_together': "(('route', 'stop', 'cycle'),)", 'object_name': 'NBPrediction'},
            'arrival_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cycle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.PredictionCycle']"}),
            'dirTag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBRoute']"}),
            'seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBStop']"})
        },
        'nextbus.nbroute': {
            'Meta': {'unique_together': "(('agency', 'tag'),)", 'object_name': 'NBRoute'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBAgency']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'existent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nextbus.NBStop']", 'symmetrical': 'False'}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nextbus.nbstop': {
            'Meta': {'unique_together': "(('agency', 'tag'),)", 'object_name': 'NBStop'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBAgency']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'existent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nextbus.predictioncycle': {
            'Meta': {'object_name': 'PredictionCycle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'})
        }
    }

    complete_apps = ['nextbus']