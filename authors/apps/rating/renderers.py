import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class RatingsRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` may or may not contain an `errors` key.
        #  We want the default JSONRenderer to handle rendering errors,
        # so we need to check for this case.

        # checks for the 'detail' key from the data given, then checks for
        # the 'errors' key. If both are not found then errors is set to None
        errors = None
        if not isinstance(data, ReturnList):
            errors = data.get('detail') if data.get('detail', None) is not \
                None else data.get('errors', None)

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            if isinstance(errors, ReturnDict):
                # here, the 'errors' key was found and will be used in the
                # response
                return super().render(data)
            else:
                # here, the errors key was not found and will be added manually
                errors = dict(errors=dict(detail=errors)
                              )
                return super().render(errors)

        # wrap the data under the 'ratings' namespace
        output = dict(ratings=data)
        return json.dumps(output)
