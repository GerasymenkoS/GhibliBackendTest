import datetime

from django.test import TestCase, RequestFactory


# Create your tests here.
from GhibliAPIApp.views import get_all_movies, data_producer


class GhibliTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_answ(self):
        request = self.factory.get('/movies/')
        response = get_all_movies(request)
        self.assertEqual(response.status_code, 200)

        start = datetime.datetime.now()
        request = self.factory.get('/movies/')
        get_all_movies(request)
        stop = datetime.datetime.now()
        elapsed = stop - start

        self.assertLess(elapsed, datetime.timedelta(seconds=60))

    def test_correctness_of_data(self):
        request = self.factory.get('/movies/')
        all_data = data_producer(request)
        self.assertIsNotNone(all_data)
        self.assertGreater(len(all_data), 3)
        self.assertTrue('director' in all_data[0])


