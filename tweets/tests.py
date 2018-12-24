from django.test import TestCase
from . twitter import resident, fetch

# Create your tests here.

class TwitterTest(TestCase):
    def test_resident(self):
        result=resident("@mehmetyildi","@kadikoybelediye")
        self.assertEquals(result,1)

    def test_keyword(self):
        keyword="gitar"
        result=len(fetch(keyword))
        self.assertEqual(result,3)

    # def test_filter(self):
    #     result=len(filter("@kadikoybelediye",fetch("gitar")))
    #     self.assertLess(result,3)
