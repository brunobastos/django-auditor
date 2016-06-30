django-auditor
==============

This Django app logs changes to models objects in a simple and 
granular way. This app supports multi-tenant environments 
which use django-tenant-schemas.

Requirements
------------

Python 3.4

Django 1.8

Installation (for environments without django-tenant-schemas)
-------------------------------------------------------------

Add "auditor" to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_auditor',
    )

Add an empty dict 'AUDITOR' on your settings:

.. code-block:: python

    AUDITOR = {}

Include the auditor URLconf in your project urls.py like this:

.. code-block:: python
    
    url(r'^auditor/', include('django_auditor.urls'))

Run `python manage.py makemigrations` to create the migration
file for auditor model.

Run `python manage.py migrate` to apply the migration and 
create the Auditor model.


Installation (django-tenant-schemas environments)
-------------------------------------------------

Add "auditor" to your SHARED_APPS or TENANT_APPS setting 
like this:

.. code-block:: python
   
    SHARED_APPS = (
        ...
        'django_auditor',
    )

or

.. code-block:: python

    TENANT_APPS = (
        ...
        'django_auditor',
    )

Add a dict 'AUDITOR' on your settings, specify a 'tenant' 
key with the value of your tenant model:

.. code-block:: python

    AUDITOR = {'tenant':'customers.Client'}

Include the auditor URLconf in your project urls.py like this:

.. code-block:: python

    url(r'^auditor/', include('django_auditor.urls'))

Run `python manage.py makemigrations` to create the migration
file for auditor model.

Run `python manage.py migrate_schemas` to apply the migration and 
create the Auditor model.

Usage and Examples
------------------

Create an instance of Audit passing request and the object you want 
to log, then call the method create(), update() or delete() 
to generate a log with the appropriate action: CREATE, UPDATE or 
DELETE.

First you have to import the Audit class:

.. code-block:: python

    from django_auditor.auditor import Audit

**New object**
    
.. code-block:: python

    new_car = Car(name='Civic', manufacturer='Honda', color='Red')
    new_car.save()
    auditor = Audit(request, new_car).create()

|Example Create|

**Update Object**

.. code-block:: python
    
    change_car = Car.objects.get(name='Civic')
    auditor = Audit(request, change_car)
    change_car.name = 'City'
    change_car.color = 'Yellow'
    change_car.save()
    auditor.update()

|Example Update|

**Delete Object**

.. code-block:: python

    remove_car = Car.objects.get(name='City')
    auditor = Audit(request, remove_car)
    remove_car.delete()
    auditor.delete()

|Example Delete|

Now open http://yoursiteURL/auditor to check your logs.

.. |Example Create| image:: http://brunobastos.net/wp-content/uploads/2016/06/django-auditor-create-example.png
.. |Example Update| image:: http://brunobastos.net/wp-content/uploads/2016/06/django-auditor-update-example.png
.. |Example Delete| image:: http://brunobastos.net/wp-content/uploads/2016/06/django-auditor-delete-example.png