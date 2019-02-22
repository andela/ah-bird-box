from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    schema = coreapi.Document(
        title='Authors Haven API',
        url='https://ah-bird-box-staging.herokuapp.com',
        content={
            'Authentication': {
                'create_user': coreapi.Link(
                    url='/api/users/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='A unique word that will identify the user.' # noqa
                        ),
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='A user\'s valid e-mail address'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='A strong password for the user'
                        )
                    ],
                    description='Create a new Account.'
                ),
                'login_user': coreapi.Link(
                    url='/api/users/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='A user\'s e-mail address'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The password of User.'
                        )
                    ],
                    description='Login a User.'
                ),
                'social auth': coreapi.Link(
                    url='/api/social/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='provider',
                            required=True,
                            location='form',
                            description='The name of the provider.'
                        ),
                        coreapi.Field(
                            name='access_token',
                            required=True,
                            location='form',
                            description='The acess token of the User.'
                        ),
                        coreapi.Field(
                            name='access_token_secret',
                            required=False,
                            location='form',
                            description='The access token secret of the User (twitter).' # noqa
                        )
                    ],
                    description='Login via social sites'
                ),
                'password_reset': coreapi.Link(
                    url='/api/users/password_reset/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='The email of the User.'
                        ),
                    ],
                    description='Request for a password reset.'
                ),
                'password_update': coreapi.Link(
                    url='/api/users/password_update/{token}',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The password of the User.'
                        ),
                        coreapi.Field(
                            name='confirm_password',
                            required=True,
                            location='form',
                            description='The password of User.'
                        )
                    ],
                    description='Update password of a User.'
                ),
            },
            'Profile': {
                'get_user_profile': coreapi.Link(
                    url='/api/profiles/{username}/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        )

                    ],
                    description='Get profile of a single user.'

                ),
                'update_user_profile': coreapi.Link(
                    url='/api/profiles/{username}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        ),
                        coreapi.Field(
                            name='bio',
                            required=False,
                            location='form',
                            description='The bio of the User.'
                        ),
                        coreapi.Field(
                            name='company',
                            required=False,
                            location='form',
                            description='The company of User.'
                        ),
                        coreapi.Field(
                            name='website',
                            required=False,
                            location='form',
                            description='The website of the user.'
                        ),
                        coreapi.Field(
                            name='phone',
                            required=False,
                            location='form',
                            description='The phone number of the User.'
                        ),
                        coreapi.Field(
                            name='image_url',
                            required=False,
                            location='form',
                            description='The image of User.'
                        )
                    ],
                    description='Update user profile'
                ),
                'get_all_profiles': coreapi.Link(
                    url='/api/profiles/',
                    action='GET',
                    description='Get all profiles'
                ),
                'follow_user': coreapi.Link(
                    url='/api/profiles/{username}/follow/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the user'
                        )
                    ],
                    description='Follow a user'
                ),
                'unfollow_user': coreapi.Link(
                    url='/api/profiles/{username}/follow/',
                    action='DELETE',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the user'
                        )
                    ],
                    description='Unfollow a user'
                ),
                'get_following': coreapi.Link(
                    url='/api/profiles/{username}/following/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the user'
                        )
                    ],
                    description='Get the list of followers and following'
                ),
            },
            'Articles': {
                'create_article': coreapi.Link(
                    url='/api/articles/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='title',
                            required=True,
                            location='form',
                            description='The title of the article.'
                        ),
                        coreapi.Field(
                            name='description',
                            required=True,
                            location='form',
                            description='The article description.'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='The article body'
                        ),
                        coreapi.Field(
                            name='image_url',
                            required=False,
                            location='form',
                            description='The article body'
                        )
                    ],
                    description='Create Article'
                ),
                'get_articles': coreapi.Link(
                    url='/api/articles/',
                    action='GET',
                    description='Display all the articles.',
                ),
                'get_single_article': coreapi.Link(
                    url='/api/articles/{slug}/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )],
                    description='Display a single article',
                ),
                'update_single_article': coreapi.Link(
                    url='/api/articles/{slug}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='title',
                            location='form',
                            description='New title'
                        ),
                        coreapi.Field(
                            name='description',
                            location='form',
                            description='New description'
                        ),
                        coreapi.Field(
                            name='image_url',
                            location='form',
                            description='New image url'
                        ),
                    ],
                    description='Update an article',
                ),
                'delete_single_article': coreapi.Link(
                    url='/api/articles/{slug}/',
                    action='DELETE',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )
                    ],
                    description='Delete an article',
                ),
                'comments': coreapi.Link(
                    url='/api/articles/{slug}/comments/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='Body of the comemnt'
                        ),
                    ],
                    description='Comment on an article',
                ),
                'get all comments': coreapi.Link(
                    url='/api/articles/{slug}/comments/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                    ],
                    description='Get all coments on an article',
                ),
                'get a specific comment': coreapi.Link(
                    url='/api/articles/{slug}/comments/{id}/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='The id of the comment.'
                        ),
                    ],
                    description='Get a specific comment',
                ),
                'update_single_comment': coreapi.Link(
                    url='/api/articles/{slug}/comments/{id}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='The id of the comment.'
                        ),

                        coreapi.Field(
                            name='body',
                            location='form',
                            description='New body on the comment'
                        ),
                    ],
                    description='Update a comment',
                ),
                'delete_single_comment': coreapi.Link(
                    url='/api/articles/{slug}/comments/{id}/',
                    action='DELETE',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='The id of the comment.'
                        ),
                    ],
                    description='Delete a comment',
                ),
                'thread': coreapi.Link(
                    url='/api/articles/{slug}/comments/{id}/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='Id of the comment'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='Body of a single thread'
                        ),
                    ],
                    description='Comment on a comment',
                ),

                'rate_an_article': coreapi.Link(
                    url='/api/articles/{slug}/ratings/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='stars',
                            required=True,
                            location='form',
                            description='Rating of the article'
                        ),
                    ],
                    description='Rate an article',
                ),
                'get_rating_for an_article': coreapi.Link(
                    url='/api/articles/{slug}/ratings/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )],
                    description='Display rating of an article',
                ),
                'get_comment_editing_history': coreapi.Link(
                    url='/api/articles/{slug}/comments/{id}/history/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='Id of the comment'
                        ),
                    ],
                    description='Get the editing history of comments'
                ),
                'like_articles': coreapi.Link(
                    url='api/articles/{slug}/like/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                    ],
                    description='Like an article'
                ),
                'unlike_articles': coreapi.Link(
                    url='api/articles/{slug}/dislike/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                    ],
                    description='Dislike an article'
                ),
            }
        }
    )

    return response.Response(schema)
