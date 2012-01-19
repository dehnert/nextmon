# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NBAgency'
        db.create_table('nextbus_nbagency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('nextbus', ['NBAgency'])

        # Adding model 'NBStop'
        db.create_table('nextbus_nbstop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.NBAgency'])),
            ('tag', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('existent', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('nextbus', ['NBStop'])

        # Adding unique constraint on 'NBStop', fields ['agency', 'tag']
        db.create_unique('nextbus_nbstop', ['agency_id', 'tag'])

        # Adding model 'NBRoute'
        db.create_table('nextbus_nbroute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.NBAgency'])),
            ('tag', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('existent', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('nextbus', ['NBRoute'])

        # Adding unique constraint on 'NBRoute', fields ['agency', 'tag']
        db.create_unique('nextbus_nbroute', ['agency_id', 'tag'])

        # Adding M2M table for field stops on 'NBRoute'
        db.create_table('nextbus_nbroute_stops', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nbroute', models.ForeignKey(orm['nextbus.nbroute'], null=False)),
            ('nbstop', models.ForeignKey(orm['nextbus.nbstop'], null=False))
        ))
        db.create_unique('nextbus_nbroute_stops', ['nbroute_id', 'nbstop_id'])

        # Adding model 'PredictionCycle'
        db.create_table('nextbus_predictioncycle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('nextbus', ['PredictionCycle'])

        # Adding model 'NBPrediction'
        db.create_table('nextbus_nbprediction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.NBRoute'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.NBStop'])),
            ('dirTag', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('cycle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nextbus.PredictionCycle'])),
            ('seconds', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('arrival_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('nextbus', ['NBPrediction'])

        # Adding unique constraint on 'NBPrediction', fields ['route', 'stop', 'cycle']
        db.create_unique('nextbus_nbprediction', ['route_id', 'stop_id', 'cycle_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'NBPrediction', fields ['route', 'stop', 'cycle']
        db.delete_unique('nextbus_nbprediction', ['route_id', 'stop_id', 'cycle_id'])

        # Removing unique constraint on 'NBRoute', fields ['agency', 'tag']
        db.delete_unique('nextbus_nbroute', ['agency_id', 'tag'])

        # Removing unique constraint on 'NBStop', fields ['agency', 'tag']
        db.delete_unique('nextbus_nbstop', ['agency_id', 'tag'])

        # Deleting model 'NBAgency'
        db.delete_table('nextbus_nbagency')

        # Deleting model 'NBStop'
        db.delete_table('nextbus_nbstop')

        # Deleting model 'NBRoute'
        db.delete_table('nextbus_nbroute')

        # Removing M2M table for field stops on 'NBRoute'
        db.delete_table('nextbus_nbroute_stops')

        # Deleting model 'PredictionCycle'
        db.delete_table('nextbus_predictioncycle')

        # Deleting model 'NBPrediction'
        db.delete_table('nextbus_nbprediction')


    models = {
        'nextbus.nbagency': {
            'Meta': {'object_name': 'NBAgency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
        'nextbus.predictioncycle': {
            'Meta': {'object_name': 'PredictionCycle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['nextbus']
