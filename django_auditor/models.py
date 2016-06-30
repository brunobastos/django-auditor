# coding: utf-8

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Auditor(models.Model):
	field = models.CharField(max_length=255, blank=True)
	action = models.CharField(max_length=6)
	old_value = models.TextField(blank=True, null=True)
	new_value = models.TextField(blank=True, null=True)
	stamp = models.DateTimeField(auto_now_add=True)
	user = models.CharField(max_length=255)
	content_type = models.ForeignKey(ContentType, blank=True)
	object_id = models.PositiveIntegerField(blank=True)
	content_object = models.TextField()
	if 'tenant' in settings.AUDITOR:
		tenant = models.ForeignKey(settings.AUDITOR['tenant'])

	class Meta:
		ordering = ['-id']
		db_table = 'auditor'