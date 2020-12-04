

class MissingParameterException(AlipayExcepton):
    '''
    Raised when the create payment url process
    is missing some parameters needed to continue
    '''
    pass

class ParameterValueErrorException(AlipayExcepton):
    '''
    Raised when the given parameter's value is incorrect
    '''
    pass

class TokenAuthorizationErrorException(AlipayExcepton):
    '''
    The error occurred when getting token
    '''
    pass
    
