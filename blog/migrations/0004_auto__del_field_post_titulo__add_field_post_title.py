# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Post.titulo'
        db.delete_column(u'blog_post', 'titulo')

        # Adding field 'Post.title'
        db.add_column(u'blog_post', 'title',
                      self.gf('django.db.models.fields.CharField')(default='VARCHAR(200)', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Post.titulo'
        db.add_column(u'blog_post', 'titulo',
                      self.gf('django.db.models.fields.CharField')(default='VARCHAR(200)', max_length=200),
                      keep_default=False)

        # Deleting field 'Post.title'
        db.delete_column(u'blog_post', 'title')


    models = {
        u'blog.post': {
            'Meta': {'object_name': 'Post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_data': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['blog']