from .api import add_handler
from .base import URLHandler
from .models import URLRoute
from django.db import models
from django.test import TestCase

class ModelA(models.Model):
    url = models.CharField(max_length=200)

    def get_absolute_url(self):
        return self.url

class ModelB(models.Model):
    url = models.CharField(max_length=200)

    def get_absolute_url(self):
        return self.url

class ARoutes(URLHandler):
    model = ModelA

class BRoutes(URLHandler):
    model = ModelB

add_handler(ARoutes())
add_handler(BRoutes())

class RouteTests(TestCase):
    def test_update(self):
        ModelA(url='/test').save()
        route = URLRoute.objects.get()
        self.assertEqual(route.target, unicode(ModelA.objects.get().pk))
        self.assertEqual(route.url, '/test')
        self.assertEqual(route.handler, 'ARoutes')

        ModelB(url='/bla/').save()
        self.assertEqual(URLRoute.objects.count(), 2)
        route = URLRoute.objects.get(url='/bla/')
        self.assertEqual(route.target, unicode(ModelB.objects.get().pk))
        self.assertEqual(route.url, '/bla/')
        self.assertEqual(route.handler, 'BRoutes')

        a = ModelA.objects.get()
        b = ModelB.objects.get()
        a.url = '/test2/'
        a.save()
        b.url = '/bla2'
        b.save()
        a.url, b.url = b.url, a.url
        a.save()
        self.assertEqual(URLRoute.objects.count(), 1)
        b.save()
        self.assertEqual(URLRoute.objects.count(), 2)
        aroute = URLRoute.objects.get(url='/bla2')
        broute = URLRoute.objects.get(url='/test2/')
        self.assertEqual(aroute.target, unicode(a.pk))
        self.assertEqual(aroute.handler, 'ARoutes')
        self.assertEqual(broute.target, unicode(b.pk))
        self.assertEqual(broute.handler, 'BRoutes')
