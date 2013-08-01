# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DailySummary'
        db.create_table('stats_dailysummary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.NBRoute'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.NBStop'])),
            ('num_checks', self.gf('django.db.models.fields.IntegerField')()),
            ('num_predictions', self.gf('django.db.models.fields.IntegerField')()),
            ('num_less_10min', self.gf('django.db.models.fields.IntegerField')()),
            ('num_less_4min', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('stats', ['DailySummary'])


    def backwards(self, orm):
        
        # Deleting model 'DailySummary'
        db.delete_table('stats_dailysummary')


    models = {
        'nextbus.nbagency': {
            'Meta': {'object_name': 'NBAgency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'nextbus.nbroute': {
            'Meta': {'unique_together': "(('agency', 'tag'),)", 'object_name': 'NBRoute'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBAgency']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'existent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nextbus.NBStop']", 'symmetrical': 'False'}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nextbus.nbstop': {
            'Meta': {'unique_together': "(('agency', 'tag'),)", 'object_name': 'NBStop'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBAgency']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'existent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stats.dailysummary': {
            'Meta': {'object_name': 'DailySummary'},
            'day': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_checks': ('django.db.models.fields.IntegerField', [], {}),
            'num_less_10min': ('django.db.models.fields.IntegerField', [], {}),
            'num_less_4min': ('django.db.models.fields.IntegerField', [], {}),
            'num_predictions': ('django.db.models.fields.IntegerField', [], {}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBRoute']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nextbus.NBStop']"})
        }
    }

    complete_apps = ['stats']
