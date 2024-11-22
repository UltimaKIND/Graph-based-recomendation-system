from django.test import TestCase
from graph_recsys.models import Genre, Track, Prefer


class GenreTest(TestCase):
    def test_str_method(self):
        test_genre = Genre(name="test")
        self.assertEqual(str(test_genre), "test")

class TrackTest(TestCase):
    def test_str_method(self):
        test_track = Track(name="test")
        self.assertEqual(str(test_track), "test")

class PreferTest(TestCase):
    def test_str_method(self):
        test_prefer = Prefer(1)
        self.assertEqual(str(test_prefer), '1')
