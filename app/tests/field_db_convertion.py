from django.test import TestCase
from app.models import FieldsWithoutOptionsModel
from google.appengine.api.datastore import Get
from google.appengine.ext.db import Key
from google.appengine.api.datastore_types import Text, Category, Email, Link, \
    PhoneNumber, PostalAddress, Text, Blob, ByteString, GeoPt, IM, Key, \
    Rating, BlobKey
from google.appengine.api import users
import datetime

class FieldDBConvertionTest(TestCase):
    def testDBConvertion(self):
        actual_datetime = datetime.datetime.now()
        entity = FieldsWithoutOptionsModel(
            datetime=actual_datetime, date=actual_datetime.date(),
            time=actual_datetime.time(), floating_point=5.97, boolean=True,
            null_boolean=False, text='Hallo', email='hallo@hallo.com',
            ip_address='194.167.1.1', slug='you slugy slut :)',
            url='http://www.scholardocs.com', long_text=1000*'A', xml=2000*'B',
            integer=-400, small_integer=-4, positiv_integer=400,
            positiv_small_integer=4)
        entity.save()

        # get the gae entity (not the model instance) and test if the fields
        # have been converted right to the corresponding gae database types
        gae_entity = Get(Key.from_path(FieldsWithoutOptionsModel._meta.db_table,
            entity.pk))

        for name, gae_db_type in [('long_text', Text), ('xml', Text),
                ('text', unicode), ('ip_address', unicode), ('slug', unicode),
                ('email', unicode), ('url', unicode), ('time', datetime.datetime),
                ('datetime', datetime.datetime), ('date', datetime.datetime),
                ('floating_point', float), ('boolean', bool),
                ('null_boolean', bool), ('integer', (int, long)),
                ('small_integer', (int, long)), ('positiv_integer', (int, long)),
                ('positiv_small_integer', (int, long))] :
            self.assertTrue(type(gae_entity[
                FieldsWithoutOptionsModel._meta.get_field_by_name(
                    name)[0].column]) in (isinstance(gae_db_type, (list, tuple)) and \
                        gae_db_type or (gae_db_type, )))

        # get the model instance and check if the fields convert back to the
        # right types
        entity = FieldsWithoutOptionsModel.objects.get()
        for name, expected_type in [('long_text', unicode), ('xml', unicode),
                ('text', unicode), ('ip_address', unicode), ('slug', unicode),
                ('email', unicode), ('url', unicode), ('datetime', datetime.datetime),
                ('date', datetime.date), ('time', datetime.time),
                ('floating_point', float), ('boolean', bool),
                ('null_boolean', bool), ('integer', (int, long)),
                ('small_integer', (int, long)), ('positiv_integer', (int, long)),
                ('positiv_small_integer', (int, long))]:
            self.assertTrue(type(getattr(entity, name)) in (isinstance(
                expected_type, (list, tuple)) and expected_type or (expected_type, )))
