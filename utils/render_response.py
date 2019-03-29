from rest_framework.renderers import JSONRenderer


# class CustomJsonRenderer(JSONRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         if renderer_context:
#             if isinstance(data, dict):
#                 msg = 'post'
#             else:
#                 msg = 'get'
#             response = renderer_context['response']
#             code = -1 if response.status_code >= 400 else 0
#             res = {
#                 'code': code,
#                 'msg': msg,
#                 'data': data
#             }
#             return super().render(res, accepted_media_type, renderer_context)
#         else:
#             return super().render(data, accepted_media_type, renderer_context)


class CustomJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context['response']
            res = {'code': response.status_code, 'data': data}
            if response.status_code in range(400, 500):
                error_list = []
                for e in data.values():
                    error_list.append(str(e[0]))
                res['msg'] = ';'.join(error_list)
                res.pop('data')
            return super().render(res, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)
