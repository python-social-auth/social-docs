Use Cases
=========

Some miscellaneous options and use cases for python-social-auth_.


Return the user to the original page
------------------------------------

There's a common scenario to return the user back to the original page from
where they requested to login. For that purpose, the usual ``next`` query-string
argument is used. The value of this parameter will be stored in the session and
later used to redirect the user when login was successful.

In order to use it, just define it with your link. For instance, when using
Django::

    <a href="{% url 'social:begin' 'facebook' %}?next={{ request.path }}">Login with Facebook</a>


Pass custom GET/POST parameters and retrieve them on authentication
-------------------------------------------------------------------

In some cases, you might need to send data over the URL, and retrieve it while
processing the after-effect. For example, for conditionally executing code in
custom pipelines.

In such cases, add it to ``SOCIAL_AUTH_FIELDS_STORED_IN_SESSION``.

In your settings::

    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['key']

In template::

    <a href="{% url 'social:begin' 'facebook' %}?key={{ value }}">Login with Facebook</a>

In your custom pipeline, retrieve it using::

    strategy.session_get('key')



Retrieve Google+ Friends
------------------------

Google provides a `People API endpoint`_ to retrieve the people in your circles
on Google+. In order to access that API first we need to define the needed
scope::

    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/plus.login'
    ]

Once we have the ``access token`` we can call the API like this::

    import requests

    user = User.objects.get(...)
    social = user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://www.googleapis.com/plus/v1/people/me/people/visible',
        params={'access_token': social.extra_data['access_token']}
    )
    friends = response.json()['items']


Associate users by email
------------------------

Sometimes it's desirable that social accounts are automatically associated if
the email already matches a user account.

For example, if a user signed up with their Facebook account, then logged out and
next time tries to use Google OAuth2 to login, it could be nice (if both social
sites have the same email address configured) that the user gets into their
initial account created by Facebook backend.

This scenario is possible by enabling the ``associate_by_email`` pipeline
function, like this::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

This feature is disabled by default because it's not 100% secure to automate
this process with all the backends. Not all the providers will validate your
email account and others users could take advantage of that.

Take for instance User A registered in your site with the email
``foo@bar.com``. Then a malicious user registers into another provider that
doesn't validate their email with that same account. Finally this user will turn
to your site (which supports that provider) and sign up to it, since the email
is the same, the malicious user will take control over the User A account.


Signup by OAuth access_token
----------------------------

It's a common scenario that mobile applications will use an SDK to signup
a user within the app, but that signup won't be reflected by
python-social-auth_ unless the corresponding database entries are created. In
order to do so, it's possible to create a view / route that creates those
entries by a given ``access_token``. Take the following code for instance (the
code follows Django conventions, but versions for others frameworks can be
implemented easily)::

    from django.contrib.auth import login

    from social_django.utils import psa

    # Define an URL entry to point to this view, call it passing the
    # access_token parameter like ?access_token=<token>. The URL entry must
    # contain the backend, like this:
    #
    #   url(r'^register-by-token/(?P<backend>[^/]+)/$',
    #       'register_by_access_token')

    @psa('social:complete')
    def register_by_access_token(request, backend):
        # This view expects an access_token GET parameter, if it's needed,
        # request.backend and request.strategy will be loaded with the current
        # backend and strategy.
        token = request.GET.get('access_token')
        user = request.backend.do_auth(token)
        if user:
            login(request, user)
            return 'OK'
        else:
            return 'ERROR'

The snippet above is quite simple, it doesn't return JSON and usually this call
will be done by AJAX. It doesn't return the user information, but that's
something that can be extended and filled to suit the project where it's going
to be used.

**Note**: when dealing with ``OAuth1``, the ``access_token`` is
          actually a query-string composed by ``oauth_token`` and
          ``oauth_token_secret``, python-social-auth_ expects this to be a
          ``dict`` with those keys, but if an string is detected, it will treat
          it as a query string in the form ``oauth_token=123&oauth_token_secret=456``.


Multiple scopes per provider
----------------------------

At the moment python-social-auth_ doesn't provide a method to define multiple
scopes for single backend, this is usually desired since it's recommended to
ask the user for the minimum scope possible and increase the access when it's
really needed. It's possible to add a new backend extending the original one to
accomplish that behavior. There are two ways to do it.

1. Overriding ``get_scope()`` method::

    from social_core.backends.facebook import FacebookOAuth2


    class CustomFacebookOAuth2(FacebookOauth2):
        def get_scope(self):
            scope = super(CustomFacebookOAuth2, self).get_scope()
            if self.data.get('extrascope'):
                scope = scope + [('foo', 'bar')]
            return scope


   This method is quite simple, it overrides the method that returns the scope
   value in a backend (``get_scope()``) and adds extra values to the list if it
   was indicated by a parameter in the ``GET`` or ``POST`` data
   (``self.data``).

   Put this new backend in some place in your project and replace the original
   ``FacebookOAuth2`` in ``AUTHENTICATION_BACKENDS`` with this new version.

   When overriding this method, take into account that the default output the
   base class for ``get_scope()`` is the raw value from the settings (whatever
   they are defined), doing this will actually update the value in your
   settings for all the users::

    scope = super(CustomFacebookOAuth2, self).get_scope()
    scope += ['foo', 'bar']

   Instead do it like this::

    scope = super(CustomFacebookOAuth2, self).get_scope()
    scope = scope + ['foo', 'bar']

2. It's possible to do the same by defining a second backend which extends from
   the original but overrides the name, this will imply new URLs and also new
   settings for the new backend (since the name is used to build the settings
   names), it also implies a new application in the provider since not all
   providers give you the option of defining multiple redirect URLs. To do it
   just add a backend like::

    from social_core.backends.facebook import FacebookOAuth2


    class CustomFacebookOAuth2(FacebookOauth2):
        name = 'facebook-custom'

   Put this new backend in some place in your project keeping the original
   ``FacebookOAuth2`` in ``AUTHENTICATION_BACKENDS``. Now a new set of URLs
   will be functional::

    /login/facebook-custom
    /complete/facebook-custom
    /disconnect/facebook-custom

   And also a new set of settings::

    SOCIAL_AUTH_FACEBOOK_CUSTOM_KEY = '...'
    SOCIAL_AUTH_FACEBOOK_CUSTOM_SECRET = '...'
    SOCIAL_AUTH_FACEBOOK_CUSTOM_SCOPE = [...]

   When the extra permissions are needed, just redirect the user to
   ``/login/facebook-custom`` and then get the social auth entry for this new
   backend with ``user.social_auth.get(provider='facebook-custom')`` and use
   the ``access_token`` in it.


Enable a user to choose a username from their World of Warcraft characters
--------------------------------------------------------------------------

If you want to register new users on your site via battle.net, you can enable
these users to choose a username from their own World-of-Warcraft characters.
To do this, use the ``battlenet-oauth2`` backend along with a small form to
choose the username.

The form is rendered via a partial pipeline item like this::

    @partial
    def pick_character_name(backend, details, response, is_new=False, *args, **kwargs):
        if backend.name == 'battlenet-oauth2' and is_new:
            data = backend.strategy.request_data()
            if data.get('character_name') is None:
                # New user and didn't pick a character name yet, so we render
                # and send a form to pick one. The form must do a POST/GET
                # request to the same URL (/complete/battlenet-oauth2/). In this
                # example we expect the user option under the key:
                #   character_name
                # you have to filter the result list according to your needs.
                # In this example, only guild members are allowed to sign up.
                char_list = [
                    c['name'] for c in backend.get_characters(response.get('access_token'))
                        if 'guild' in c and c['guild'] == '<guild name>'
                ]
                return render_to_response('pick_character_form.html', {'charlist': char_list, })
            else:
                # The user selected a character name
                return {'username': data.get('character_name')}

Don't forget to add the partial to the pipeline::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'path.to.pick_character_name',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

It needs to be somewhere before create_user because the partial will change the
username according to the users choice.


Re-prompt Google OAuth2 users to refresh the ``refresh_token``
--------------------------------------------------------------

A ``refresh_token`` also expire, a ``refresh_token`` can be lost, but they can
also be refreshed (or re-fetched) if you ask to Google the right way. In order
to do so, set this setting::

    SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
        'access_type': 'offline',
        'approval_prompt': 'auto'
    }

Then link the users to ``/login/google-oauth2?approval_prompt=force``. If you
want to refresh the ``refresh_token`` only on those users that don't  have it,
do it with a pipeline function::

    def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
        if backend.name == 'google-oauth2' and social and \
           response.get('refresh_token') is None and \
           social.extra_data.get('refresh_token') is None:
            return redirect('/login/google-oauth2?approval_prompt=force')

Set this pipeline after ``social_user``::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'path.to.redirect_if_no_refresh_token',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )


Improve unicode cleanup from usernames
--------------------------------------

It's possible to improve the username cleanup by using an external library like
Unidecode_ or Text-Unicode_. You can integrate these by using the
`SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION` documented at `Username Generation`_
section. For instance, this will do the work::

    SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'unidecode.unidecode'


.. _python-social-auth: https://github.com/python-social-auth
.. _People API endpoint: https://developers.google.com/+/api/latest/people/list
.. _Unidecode: https://pypi.org/project/Unidecode/
.. _Text-Unicode: https://github.com/kmike/text-unidecode/
.. _Username Generation: configuration/settings.html#username-generation
