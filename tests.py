import unittest
import server
from model import db, connect_to_db

class FlickrMatchTests(unittest.TestCase):
    """Tests for FlickrMatch sites."""
    def setUp(self):
        """Stuff to do before every test."""
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn("Find match through Flickr photos", result.data)

    def test_bestnine(self):
        result = self.client.post('/userinfo', data={
            'username1': 'Alexander Lauterbach Photography',
            'username2': 'kenny barker',
            'name1': 'alex',
            'name2': 'kenny',
            'urls1': ['https://farm5.staticflickr.com/4291/35918274276_6ea2043fec_q.jpg', 'https://farm5.staticflickr.com/4283/35375296251_fe0a400d30_q.jpg', 'https://farm5.staticflickr.com/4256/34389434093_0987d2a3aa_q.jpg', 'https://farm5.staticflickr.com/4717/26188479028_68ca6660b6_q.jpg', 'https://farm2.staticflickr.com/1626/24566193744_2ea8a1d930_q.jpg', 'https://farm9.staticflickr.com/8701/16921672996_9af7f132af_q.jpg', 'https://farm3.staticflickr.com/2862/12722036585_6a95fd7ff1_q.jpg', 'https://farm8.staticflickr.com/7447/12089646585_f32531ac60_q.jpg', 'https://farm8.staticflickr.com/7354/10097130576_99e14ca925_q.jpg'],
            'urls2':['https://farm4.staticflickr.com/3732/11351383465_a89fa93a7c_q.jpg', 'https://farm9.staticflickr.com/8509/8552151240_2d7860f97d_q.jpg', 'https://farm9.staticflickr.com/8050/8417699864_5646842484_q.jpg', 'https://farm9.staticflickr.com/8441/7757130470_6ebc274b30_q.jpg', 'https://farm9.staticflickr.com/8185/8119610535_704e601867_q.jpg', 'https://farm8.staticflickr.com/7257/7751477406_bb926a20d5_q.jpg', 'https://farm9.staticflickr.com/8016/7643534820_ae79ecf6fe_q.jpg', 'https://farm8.staticflickr.com/7278/7531796316_a04d5b397e_q.jpg', 'https://farm8.staticflickr.com/7213/7398098972_8f3c25edaf_q.jpg']
            })
        self.assertIn("Best Nine on Flickr", result.data)

    def test_wordmatch(self):
        result = self.client.get('/tags-bubble')
        self.assertIn("in photo tags", result.data)

    def test_pathmatch(self):
        result = self.client.get('/geo')
        self.assertIn("photo path", result.data)


class FlikrMatchDatabase(unittest.TestCase):
    """Flask test that use the database."""
    def setUP(self):
        """Stuff to do before every test."""
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        

if __name__ == "__main__":
    unittest.main()