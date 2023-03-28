"""
-------------------------------------------------
    File Name:   c_renderer.py
    Description: 
        
    Author:      chaizz
    Date:        2023/3/14 10:59
-------------------------------------------------
    Change Activity:
          2023/3/14 10:59
-------------------------------------------------
"""

from rest_framework.renderers import JSONRenderer


class custom_renderer(JSONRenderer):
    """
    统一返回正常格式
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)

        if renderer_context["response"].status_code == 200 or renderer_context["response"].status_code == 201:
            data = {
                "status_code": 200,
                "message": "success",
                "data": data,
            }
        renderer_context["response"].status_code = 200
        return super().render(data, accepted_media_type, renderer_context)
