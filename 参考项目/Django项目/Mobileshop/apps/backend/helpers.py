from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        if isinstance(data, list):
            data = {"data": data}
        data.setdefault("code", 200)
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class InputErrorMessage(JSONResponse):
    def __init__(self, message, **kwargs):
        super().__init__({"code": 400, "message": message}, **kwargs)
