from hashlib import md5
from urllib.parse import urlencode
from .exceptions import AlipayExcepton,ParameterValueErrorException,MissingParameterException,TokenAuthorizationErrorException
class Alipay(object):
    GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'

    NOTIFY_GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'\
        '?service=notify_verify&partner=%s&notify_id=%s'

    sign_tuple = ('sign_type', 'MD5', 'MD5')
    sign_key = False

    def __init__(self,pid,key,seller_email=None,seller_id=None):
        self.key = key
        self.pid = pid
        self.default_params = {'_input_charset':'utf-8',
                                'partner':pid,
                                'payment_type':'1'}
        # 优先使用 seller_id (与接口端的行为一致)
        if seller_id is not None:
            self.default_params['seller_id'] = seller_id
        elif seller_email is not None:
            self.default_params['seller_email'] = seller_email
        else:
            raise MissingParameterException('missing parameter seller_id or seller_email')

    def _decode_params(self,params):
        return {
                    k:v.encode('utf-8')
                    if isinstance(v,str) 
                    else v.encode('utf-8')
                    for k,v in params
                }
    def _generate_md5_sign(self,params):
        src = '&'.join(['%s=%s' % (key,value) for key,value in sorted(params.items())])+self.key
        return md5(src)

    def _check_params(self,params,names):
        if not all(k in params for k in names):
            raise MissingParameterException(' missing parameters')
    def _build_url(self,service,paramnames=None,**kw):
        '''
        创建带签名的请求地址，paramnames为需要八号的参谋名，由于避免出现过多的参数，默认使用全部的参数
        '''
        params = self.default_params.copy()
        params['service'] = service
        params.update(kw)
        if paramnames:
            params = dict([(k,params[k]) for k in paramnames if k in params])
        signkey,signvalue,signdescription = self.sign_tuple
        signmethod = getattr(self,'_generate_%s_sign' % signdescription.lower(),
        None #getattr raise AttributeError If not default provided
        )
        if signmethod is None:
            raise NotImplementedError("This type '%s' of sign is not implemented yet." % signmethod)
        if self.sign_key:
            params.update({signkey,signvalue})
        params.update({signkey:signvalue,'sign':signmethod(params)})
        return '%s?%s' % (self.GATEWAY_URL,urlencode(self._decode_params(params)))
        
    def create_direct_pay_by_user_url(self,**kw):
        self._check_params(kw,('out_trade_no','subject'))
        if not kw.get('total_fee') and \
            not (kw.get('price') and kw.get('quantity')):
            raise ParameterValueErrorException('total_fee or (price and quantity) must have one.')
        url =self._build_url('create_direct_pay_by_user',**kw)
        return url