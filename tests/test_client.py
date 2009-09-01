import unittest
import urllib2

from meaningtoolws.scoring_exceptions import \
                        NoTextScoringError, NoClassifiersScoringError, \
                        MissingComponentsScoringError, CannotDetectLanguageScoringError, \
                        UndispatchableRequestScoringError
from meaningtoolws.ct import Client


from base import data_response, fail_response

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.client= Client(u'api-key', u'ct-uuid')

    def test_no_text(self):
        urllib2.urlopen= fail_response(NoTextScoringError)
        self.assertRaises(NoTextScoringError, self.client.get_categories, u'text', u'pepe')

    def test_no_classifiers(self):
        urllib2.urlopen= fail_response(NoClassifiersScoringError)
        self.assertRaises(NoClassifiersScoringError, self.client.get_categories, u'text', u'pepe')

    def test_missing_components(self):
        urllib2.urlopen= fail_response(MissingComponentsScoringError)
        self.assertRaises(MissingComponentsScoringError, self.client.get_categories, u'text', u'pepe')

    def test_cannot_detect_lang(self):
        urllib2.urlopen= fail_response(CannotDetectLanguageScoringError)
        self.assertRaises(CannotDetectLanguageScoringError, self.client.get_categories, u'text', u'pepe')

    def test_cannot_detect_lang(self):
        urllib2.urlopen= fail_response(CannotDetectLanguageScoringError)
        self.assertRaises(CannotDetectLanguageScoringError, self.client.get_categories, u'text', u'pepe')

    def test_data_response(self):
        data= {u'categories': [{u'score': 0.18388247648468797, u'name': u'Gaming'}, \
                               {u'score': 0.15857251730433639, u'name': u'Arts'}, \
                               {u'score': 0.16063399113213972, u'name': u'Lifestyle'}, \
                               {u'score': 0.26083577259764912, u'name': u'Movies'}]}

        urllib2.urlopen= data_response(data)
        result= self.client.get_categories(u'url', u'http://en.wikipedia.org/wiki/Angelina_Jolie')
        self.assertEqual(data, result.data)
