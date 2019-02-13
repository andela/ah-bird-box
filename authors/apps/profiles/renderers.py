import json

from ..authentication.renderers import UserJSONRenderer


class ProfileJSONRenderer(UserJSONRenderer):

    def render(self, data, media_type=None, renderer_context=None):
        """
        overide UserJSONRenderer to render our data under the "profile" namespace.  # noqa
        """
        return json.dumps({
            'profile': data
        })
