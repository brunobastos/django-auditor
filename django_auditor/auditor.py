# coding: utf-8

from .models import Auditor
from django.contrib.contenttypes.models import ContentType
from copy import deepcopy
from django.conf import settings

class Audit:
    def __init__(self, request, obj):
        self.original_object = deepcopy(obj)
        self.modified_object = obj
        self.user = str(request.user)
        self.content_type = ContentType.objects.get_for_model(
            self.original_object)
        if 'tenant' in settings.AUDITOR:
            self.tenant = request.tenant
        else:
            self.tenant = None

    def create_audit(self, action='', field=False):
        audit = Auditor(content_type=self.content_type)
        audit.object_id = self.original_object.pk
        audit.user = self.user
        audit.action = action
        audit.content_object = self.original_object
        audit.tenant = self.tenant
        if field:
            audit.field = field
        audit.save()

    def create(self):
        self.create_audit(action='CREATE')
        
    def delete(self):
        self.create_audit(action='DELETE')

    def audit_field(self, action='', field=''):
        """
        Pass an action and a field to register a 
        particular change
        """
        self.create_audit(action=action, field=field)
        
    def update(self, modified_object=False):
        """
        Although the modified_object argument is optional,
        you may want to pass the modified object
        """
        if modified_object:
            self.modified_object = modified_object

        # Loop through object fields
        for field in self.original_object._meta.get_fields():

            # Try to get the field value
            try:
                original_value = getattr(self.original_object, field.name)
                modified_value = getattr(self.modified_object, field.name)

                # Don't audit related fields in order to avoid duplicated data
                if str(field.name)[-3:] == '_id':
                    audit_field = False
                else:
                    audit_field = True

            except:
                audit_field = False

            if (audit_field and
                field.name != 'id' and
                (original_value != modified_value) and not
                ((original_value is None and modified_value == '') or
                    (original_value == '' and modified_value is None))):
                """
                Check if fields values are different (id field excluded)
                Don't audit if value change from None to '' or '' to None
                """

                audit = Auditor(content_type=self.content_type)
                audit.object_id = self.modified_object.pk
                audit.user = self.user
                audit.action = "UPDATE"

                try:
                    audit.field = self.original_object._meta.get_field(field.name).verbose_name
                except:
                    continue

                audit.content_object = self.modified_object

                # Store the choice name, otherwise store original value
                if (hasattr(self.original_object, 'get_' + str(field.name) + '_display') and
                    hasattr(self.modified_object, 'get_' + str(field.name) + '_display')):

                    audit.old_value = getattr(self.original_object, 'get_%s_display' % field.name)()
                    audit.new_value = getattr(self.modified_object, 'get_%s_display' % field.name)()
                else:
                    audit.old_value = original_value
                    audit.new_value = modified_value

                audit.tenant = self.tenant

                audit.save()
