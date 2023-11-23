=====
graphql_user
=====

graphql_user is a Django app to conduct web-based graphql_user. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "graphql_user" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_filters",
        "graphene_django",
        "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
        'rest_framework',
        "graphql_user",
    ]

2. Add the setting for the graphene and graphql_jwt in the settings.py


    ``Defining the auth user model``

    AUTH_USER_MODEL = 'graphql_user.User'

    ``Adding the jwt auth backend for grapghql jwt authentication.```
    AUTHENTICATION_BACKENDS = [
        "graphql_jwt.backends.JSONWebTokenBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]
    
    ``Graphene settings ref: https://docs.graphene-python.org/projects/django/en/latest/settings/ ``
    GRAPHENE = {
        "SCHEMA": "user.schema.schema",
        "MIDDLEWARE": [
            "graphql_jwt.middleware.JSONWebTokenMiddleware",
        ],
    }

    ``Graphql_jwt settings ref: https://django-graphql-jwt.domake.io/settings.html ``
    GRAPHQL_JWT = {
        "JWT_ALLOW_ARGUMENT": True,
        "JWT_PAYLOAD_HANDLER": "user.utils.jwt_payload",
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
        "JWT_EXPIRATION_DELTA": timedelta(minutes=5),
        "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    }


Include the graphql_user URLconf in your project urls.py like this::

    path("graphql_user/", include("graphql_user.urls")),

3. Run ``python manage.py migrate`` to create the graphql_user models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/graphql_user/ to participate in the poll.