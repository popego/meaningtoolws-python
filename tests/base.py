try:
    import json
except:
    import simplejson as json


class DummyResponse(object):
    """
    Simula una response del urllib2.urlopen
    """
    def __init__(self, result):
        self.result= result
    def read(self):
        return self.result

def fail_response(exception):
    """
    dada una excepcion, genera una `DummyResponse` que simula una respuesta del servidor con esa excepcion
    """
    def do_response(req):
        result= json.dumps(dict(status='error',
                    errcode=exception.get_code(),
                    message=exception.message,
                    data={}))
        return DummyResponse(result)

    return do_response

def data_response(data):
    """
    Dada una excepcion, genera una `DummyResponse` que simula una respuesta del servidor con esa `data`
    """
    def do_response(req):
        result= json.dumps(dict(status=u'ok',
                    errcode='ok',
                    message='cool',
                    data=data))
        return DummyResponse(result)

    return do_response

