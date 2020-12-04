import unittest
from urllib.parse import parse_qs,urlparse

class AlipayTests(unittest.TestCase):
    def Alipay(self, *a, **kw):
        from .payment import Alipay
        return Alipay(*a, **kw)

    def setUp(self):
        self.alipay = self.Alipay(pid='pid',key='key',seller_email='xxx@gmail.com')
    def tearDown(self):
        '''
        end of the testing
        '''

    def test_create_direct_pay_by_user_url(self):

        # arrange
        params = {
            'out_trade_no':'1',
            'subject':'test',
            'price':'0.01',
            'quantity':1
        }
        #act
        url =self.alipay.create_direct_pay_by_user_url(**params)
        self.assertIn('create_direct_pay_by_user',url)
        