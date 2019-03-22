from rest_framework.renderers import JSONRenderer


class CustomJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = 'post'
            else:
                msg = 'get'
            response = renderer_context['response']
            code = -1 if response.status_code >= 400 else 0
            res = {
                'c': code,
                'm': msg,
                'd': data
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
