Pipeline
========

python-social-auth_ uses an extendible pipeline mechanism where developers can
introduce their functions during the authentication, association and
disconnection flows.

The functions will receive a variable set of arguments related to the current
process, common arguments are the current ``strategy``, ``user`` (if any) and
``request``. It's recommended that all the function also define an ``**kwargs``
in the parameters to avoid errors for unexpected arguments.

Each pipeline entry can return a ``dict`` or ``None``, any other type of return
value is treated as a response instance and returned directly to the client,
check *Partial Pipeline* below for details.

If a ``dict`` is returned, the value in the set will be merged into the
``kwargs`` argument for the next pipeline entry, ``None`` is taken as if ``{}``
was returned.


Authentication Pipeline
-----------------------

The final process of the authentication workflow is handled by an operations
pipeline where custom functions can be added or default items can be removed to
provide a custom behavior. The default pipeline is a mechanism that creates
user instances and gathers basic data from providers.

The default pipeline is composed by::

    (
        # Get the information we can about the user and return it in a simple
        # format to create the user instance later. In some cases the details are
        # already part of the auth response from the provider, but sometimes this
        # could hit a provider API.
        'social_core.pipeline.social_auth.social_details',

        # Get the social uid from whichever service we're authing thru. The uid is
        # the unique identifier of the given user in the provider.
        'social_core.pipeline.social_auth.social_uid',

        # Verifies that the current auth process is valid within the current
        # project, this is where emails and domains whitelists are applied (if
        # defined).
        'social_core.pipeline.social_auth.auth_allowed',

        # Checks if the current social-account is already associated in the site.
        'social_core.pipeline.social_auth.social_user',

        # Make up a username for this person, appends a random string at the end if
        # there's any collision.
        'social_core.pipeline.user.get_username',

        # Send a validation email to the user to verify its email address.
        # Disabled by default.
        # 'social_core.pipeline.mail.mail_validation',

        # Associates the current social details with another user account with
        # a similar email address. Disabled by default.
        # 'social_core.pipeline.social_auth.associate_by_email',

        # Create a user account if we haven't found one yet.
        'social_core.pipeline.user.create_user',

        # Create the record that associates the social account with the user.
        'social_core.pipeline.social_auth.associate_user',

        # Populate the extra_data field in the social record with the values
        # specified by settings (and the default ones like access_token, etc).
        'social_core.pipeline.social_auth.load_extra_data',

        # Update the user record with any changed info from the auth service.
        'social_core.pipeline.user.user_details',
    )


It's possible to override it by defining the setting ``SOCIAL_AUTH_PIPELINE``.
For example, a pipeline that won't create users, just accept already registered
ones would look like this::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

Note that this assumes the user is already authenticated, and thus the ``user`` key
in the dict is populated. In cases where the authentication is purely external, a
pipeline method must be provided that populates the ``user`` key. Example::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'myapp.pipeline.load_user',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

It is also possible to define pipelines on a per backend basis by defining a setting
such as ``SOCIAL_AUTH_TWITTER_PIPELINE``. Backend specific pipelines will override
the non specific pipelines (i.e. the default pipeline and ``SOCIAL_AUTH_PIPELINE``).

Each pipeline function will receive the following parameters:
    * Current strategy (which gives access to current store, backend and request)
    * User ID given by authentication provider
    * User details given by authentication provider
    * ``is_new`` flag (initialized as ``False``)
    * Any arguments passed to ``auth_complete`` backend method, default views
      pass these arguments:

      * current logged in user (if it's logged in, otherwise ``None``)
      * current request


Disconnection Pipeline
----------------------

Like the authentication pipeline, it's possible to define a disconnection
pipeline if needed.

For example, this can be useful on sites where a user that disconnects all the
related social account is required to fill a password to ensure the
authentication process in the future. This can be accomplished by overriding
the default disconnection pipeline and setup a function that checks if the user
has a password, in case it doesn't a redirect to a fill-your-password form can
be returned and later continue the disconnection process, take into account
that disconnection ensures the POST method by default, a simple method to
ensure this, is to make your form POST to ``/disconnect/`` and set the needed
password in your pipeline function. Check *Partial Pipeline* below.

In order to override the disconnection pipeline, just define the setting::

    SOCIAL_AUTH_DISCONNECT_PIPELINE = (
        # Verifies that the social association can be disconnected from the current
        # user (ensure that the user login mechanism is not compromised by this
        # disconnection).
        'social_core.pipeline.disconnect.allowed_to_disconnect',

        # Collects the social associations to disconnect.
        'social_core.pipeline.disconnect.get_entries',

        # Revoke any access_token when possible.
        'social_core.pipeline.disconnect.revoke_tokens',

        # Removes the social associations.
        'social_core.pipeline.disconnect.disconnect',
    )

Backend specific disconnection pipelines can also be defined with a setting such as
``SOCIAL_AUTH_TWITTER_DISCONNECT_PIPELINE``.


Partial Pipeline
----------------

It's possible to pause the pipeline to return to the user asking for
some action and resume it later.

To accomplish this decorate the function that will cut the process
with the ``@partial`` decorator located at ``social/pipeline/partial.py``.

When it's time to resume the process just redirect the user to ``/complete/<backend>/``
or ``/disconnect/<backend>/`` view. The pipeline will resume in the same
function that cut the process.

``@partial`` stores needed data into a database table name `social_auth_partial`.
This table holds the needed information to resume it later from any browsers and
drops the old dependency on browser sessions that made the move between browsers
impossible.

The partial data is identified by a UUID token that can be used to store in the
session or append to any URL using the `partial_token` parameter (default value).
The lib will pick this value from the request and load the needed partial data to
let the user continue the process.

The pipeline functions will get a `current_partial` instance that contains the
partial token and the needed data that will be saved in the database.

To get the backend in order to redirect to any social view, just do::

    backend = current_partial.backend

To override the default parameter name just define::

  SOCIAL_AUTH_PARTIAL_PIPELINE_TOKEN_NAME = '...'

Check the `example applications`_ to check a basic usage.


Email validation
----------------

There's a pipeline to validate email addresses, but it relies a lot on your
project.

The pipeline is at ``social_core.pipeline.mail.mail_validation`` and it's a partial
pipeline, it will return a redirect to the URL defined by the
`EMAIL_VALIDATION_URL` setting. For Django you can use a view name as the value
for this setting. You can use this redirect to tell the users that an email
validation was sent to them. If you want to mention the email address you can
get it from the session under the key ``email_validation_address``.

In order to send the validation python-social-auth_ needs a function that will
take care of it, this function is defined by the developer with the setting
``SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION``. It should be an import path. This
function should take four arguments ``strategy``, ``backend``, ``code`` and
``partial_token``.

``partial_token`` is the same token used on other partials functions
that can be used to restart a halted flow.

``code`` is a model instance used to validate the email address, it
contains three fields:

``code = '...'``
    Holds an ``uuid.uuid4()`` value and it's the code used to identify the
    validation process.

``email = '...'``
    Email address trying to be validate.

``verified = True / False``
    Flag marking if the email was verified or not.

You should use the code in this instance to build the link for email
validation which should go to ``/complete/email?verification_code=<code here>&partial_token=<token here>``.
If you are using Django, you can do it with::

    from django.core.urlresolvers import reverse
    url = strategy.build_absolute_uri(
        reverse('social:complete', args=(strategy.backend_name,))
    ) + '?verification_code=' + code.code + '&partial_token=' + partial_token
    

On Flask::

    from flask import url_for
    url = url_for('social.complete', backend=strategy.backend_name,
                  _external=True) + '?verification_code=' + code.code + '&partial_token=' + partial_token

This pipeline can be used globally with any backend if this setting is defined::

    SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True

Or individually by defining the setting per backend basis like
``SOCIAL_AUTH_TWITTER_FORCE_EMAIL_VALIDATION = True``.


Extending the Pipeline
======================

The main purpose of the pipeline (either creation or deletion pipelines) is to
allow extensibility for developers. You can jump in the middle of it, do
changes to the data, create other models instances, ask users for extra data,
or even halt the whole process.

Extending the pipeline implies:

    1. Writing a function
    2. Locating the function in an accessible path
       (accessible in the way that it can be imported)
    3. Overriding the default pipeline definition with one that includes
       newly created function.

The part of writing the function is quite simple. However please be careful
when placing your function in the pipeline definition, because order
does matter in this case! Ordering of functions in ``SOCIAL_AUTH_PIPELINE``
will determine the value of arguments that each function will receive.
For example, adding your function after ``social_core.pipeline.user.create_user``
ensures that your function will get the user instance (created or already existent)
instead of a ``None`` value.

The pipeline functions will get quite a lot of arguments, ranging from the
backend in use, different model instances, server requests and provider
responses. To enumerate a few:

``strategy``
    The current strategy instance.

``backend``
    The current backend instance.

``uid``
    User ID in the provider, this ``uid`` should identify the user in the
    current provider.

``response = {} or object()``
    The server user-details response, it depends on the protocol in use (and
    sometimes the provider implementation of such protocol), but usually it's
    just a ``dict`` with the user profile details from the provider. Lots of
    information related to the user is provided here, sometimes the ``scope``
    will increase the amount of information in this response on OAuth
    providers.

``details = {}``
    Basic user details generated by the backend, used to create/update the user
    model details (this ``dict`` will contain values like ``username``,
    ``email``, ``first_name``, ``last_name`` and ``fullname``).

``user = None``
    The user instance (or ``None`` if it wasn't created or retrieved from the
    database yet).

``social = None``
    This is the associated ``UserSocialAuth`` instance for the given user (or
    ``None`` if it wasn't created or retrieved from the DB yet).

Usually when writing your custom pipeline function, you just want to get some
values from the ``response`` parameter. But you can do even more, like call
other APIs endpoints to retrieve even more details about the user, store them
on some other place, etc.

Here's an example of a simple pipeline function that will create a ``Profile``
class instance, related to the current user. This profile will store some simple details
returned by the provider (``Facebook`` in this example). The usual Facebook
``response`` looks like this::

    {
        'username': 'foobar',
        'access_token': 'CAAD...',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'verified': True,
        'name': 'Foo Bar',
        'locale': 'en_US',
        'gender': 'male',
        'expires': '5183999',
        'email': 'foo@bar.com',
        'updated_time': '2014-01-14T15:58:35+0000',
        'link': 'https://www.facebook.com/foobar',
        'timezone': -3,
        'id': '100000126636010',
    }

Let's say we are interested in storing the user profile link, the gender and
the timezone in our ``Profile`` model::

    def save_profile(backend, user, response, *args, **kwargs):
        if backend.name == 'facebook':
            profile = user.get_profile()
            if profile is None:
                profile = Profile(user_id=user.id)
            profile.gender = response.get('gender')
            profile.link = response.get('link')
            profile.timezone = response.get('timezone')
            profile.save()

Now all that's needed is to tell ``python-social-auth`` to use our function in
the pipeline. Since the function uses user instance, we need to put it after
``social_core.pipeline.user.create_user``::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'path.to.save_profile',  # <--- set the path to the function
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

So far the function we created returns ``None``, which is taken as if ``{}`` was returned.
If you want the ``profile`` object to be available to the next function in the
pipeline, all you need to do is return ``{'profile': profile}``.

.. _python-social-auth: https://github.com/python-social-auth
.. _example applications: https://github.com/python-social-auth/social-examples
