Pipeline
========

python-social-auth_ uses an extendible pipeline mechanism where developers can
introduce their functions during the authentication, association and
disconnection flows.

Pipeline Overview
-----------------

The pipeline is a sequence of functions that are executed in order during the
authentication process. Each function receives data from the previous steps and
can pass data to the next steps.

**Key Concepts:**

* **Pipeline functions** are called sequentially in the order they are defined
* **Each function** receives arguments from the authentication process and previous pipeline steps
* **Functions can pass data forward** by returning a dictionary
* **Functions can interrupt the flow** by returning an HTTP response (e.g., redirect)
* **All functions should accept** ``**kwargs`` to handle unexpected arguments gracefully

Understanding Return Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipeline functions can return three types of values, each with different behavior:

1. **Return** ``None`` **or nothing**: The pipeline continues to the next function. This is 
   equivalent to returning an empty dict ``{}``.

2. **Return a** ``dict``: The values in the dictionary are merged into the ``kwargs`` for 
   all subsequent pipeline functions. This is how you pass data forward in the pipeline.
   
   Example::
   
       def my_pipeline_function(backend, user, **kwargs):
           # Calculate something
           custom_value = "some data"
           # Pass it to next functions
           return {'custom_value': custom_value}

3. **Return any other value** (HTTP response, redirect, etc.): The pipeline is interrupted 
   and the value is returned directly to the client. This is useful for partial pipelines 
   where you need user input.
   
   Example::
   
       def my_pipeline_function(backend, user, **kwargs):
           if some_condition:
               # Interrupt pipeline and redirect user
               return redirect('/some-form/')

Common Function Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The functions will receive a variable set of arguments related to the current
process. Common arguments include:

* ``strategy`` - The current strategy instance (provides access to storage, settings, and request)
* ``backend`` - The current backend instance (the social authentication provider)
* ``user`` - The user instance (``None`` if not yet created or retrieved)
* ``request`` - The current HTTP request object
* ``social`` - The ``UserSocialAuth`` instance (``None`` until created)
* ``uid`` - The unique user ID from the provider
* ``response`` - The raw response from the authentication provider
* ``details`` - Processed user details (username, email, etc.)
* ``is_new`` - Boolean indicating if a user was just created
* Any values returned as dicts by previous pipeline functions

**Important:** Always include ``**kwargs`` in your function signature to handle additional 
arguments that may be passed from other pipeline functions or future versions::

    def my_custom_pipeline(strategy, backend, user, **kwargs):
        # Your code here
        pass


Authentication Pipeline
-----------------------

The authentication workflow is handled by a pipeline where custom functions can 
be added or default items can be removed to provide custom behavior. The default 
pipeline creates user instances and gathers basic data from providers.

Understanding the Default Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pipeline executes in order, with each step depending on data from previous steps.
Here's what happens at each stage:

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

**What Data is Available When?**

Understanding which data is available at each stage is crucial for placing your 
custom functions correctly:

* **After** ``social_details``: ``details`` dict is populated with user info
* **After** ``social_uid``: ``uid`` contains the provider's user ID
* **After** ``social_user``: ``social`` may contain the UserSocialAuth instance (if user was previously authenticated)
* **After** ``get_username``: ``username`` is available
* **After** ``create_user``: ``user`` contains the User instance (new or existing)
* **After** ``associate_user``: ``social`` contains the UserSocialAuth instance
* **After** ``load_extra_data``: ``social.extra_data`` contains access tokens and additional provider data

Customizing the Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~

You can override the default pipeline by defining the setting ``SOCIAL_AUTH_PIPELINE``.

**Example 1: Preventing New User Creation**

A pipeline that won't create users, just accepts already registered ones would look like this::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

**Note:** This example removes ``get_username`` and ``create_user`` steps, so only 
users who have previously authenticated can log in.

**Example 2: Custom User Loading**

When authentication is purely external, you need a custom pipeline function that 
populates the ``user`` key. This function should load or identify the user before 
the ``social_user`` step::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'myapp.pipeline.load_user',  # Custom function to load the user
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

Your ``load_user`` function might look like::

    def load_user(strategy, backend, uid, user=None, **kwargs):
        if user:
            return {'user': user}
        # Load user from your custom authentication system
        user = MyUserModel.get_by_external_id(uid)
        return {'user': user}

Per-Backend Pipelines
~~~~~~~~~~~~~~~~~~~~~

It is also possible to define pipelines on a per backend basis by defining a setting
such as ``SOCIAL_AUTH_TWITTER_PIPELINE``. Backend-specific pipelines will override
the default and ``SOCIAL_AUTH_PIPELINE`` settings.


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

The partial pipeline feature allows you to pause the authentication process to 
request additional information from the user, then resume where you left off.

How Partial Pipelines Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Pause the pipeline**: Use the ``@partial`` decorator on your function
2. **Return an HTTP response**: Redirect the user to a form or page
3. **User completes the action**: User fills out a form and submits it
4. **Resume the pipeline**: User is redirected back to ``/complete/<backend>/`` and 
   the pipeline resumes from the same function

Basic Example
~~~~~~~~~~~~~

Here's a simple example of collecting additional user information::

    from social_core.pipeline.partial import partial

    @partial
    def require_email(strategy, backend, details, user=None, **kwargs):
        if user and user.email:
            # User already has email, continue
            return
        
        # Check if email was submitted in this request
        email = strategy.request_data().get('email')
        if email:
            # Email was provided, pass it forward
            return {'details': {'email': email}}
        
        # No email yet - interrupt pipeline and show form
        return strategy.render_html('email_form.html')

In your template, the form should POST to ``/complete/<backend>/``::

    <form method="post" action="{% url 'social:complete' backend %}">
        {% csrf_token %}
        <input type="email" name="email" required>
        <button type="submit">Continue</button>
    </form>

How Partial Data is Stored
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``@partial`` stores the pipeline state in a database table named ``social_auth_partial``.
This allows:

* **Cross-browser support**: The process can resume from any browser
* **No session dependency**: More reliable than session-based approaches
* **UUID tokens**: Each partial process is identified by a unique token

The partial token is passed via the ``partial_token`` parameter (by default). The library
automatically picks this value from the request to resume the process.

Accessing Partial Data
~~~~~~~~~~~~~~~~~~~~~~~

Pipeline functions receive a ``current_partial`` instance containing:

* ``current_partial.token`` - The unique token for this partial process
* ``current_partial.backend`` - The backend name
* Other saved data from the pipeline

Example of using the partial token in a redirect::

    from urllib.parse import urlencode
    
    @partial
    def my_partial_function(strategy, backend, current_partial=None, **kwargs):
        # Check if user needs to provide additional information
        if not kwargs.get('phone_number'):
            # Include partial_token in the URL
            params = urlencode({'partial_token': current_partial.token})
            url = f'/my-form/?{params}'
            return redirect(url)

Configuration
~~~~~~~~~~~~~

To override the default parameter name::

    SOCIAL_AUTH_PARTIAL_PIPELINE_TOKEN_NAME = 'my_token_name'

Check the `example applications`_ for more detailed usage examples.


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

The pipeline system is designed for extensibility. You can add custom functions to:

* Modify authentication data
* Create or update related model instances  
* Request additional user information
* Implement custom authorization logic
* Integrate with external systems

Steps to Add a Custom Pipeline Function
----------------------------------------

1. **Write your function** with the appropriate signature
2. **Place it in an importable location** in your project
3. **Add it to the pipeline** in your settings at the appropriate position

**Important:** Function placement matters! The order determines what data is available.
For example, placing your function after ``create_user`` ensures you receive a ``user`` 
instance rather than ``None``.

Writing Custom Pipeline Functions
----------------------------------

Function Signature
~~~~~~~~~~~~~~~~~~

Your function should accept the common parameters and ``**kwargs``::

    def my_pipeline_function(strategy, backend, user=None, **kwargs):
        # Your code here
        pass

**Tip:** Always include ``**kwargs`` to handle additional parameters from other 
pipeline functions or future versions.

Common Parameters Available
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Depending on where you place your function in the pipeline, these parameters may be available:

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
    The user instance (or ``None`` if not yet created or retrieved).

``social = None``
    The ``UserSocialAuth`` instance for the user (or ``None`` if not yet created).

``is_new``
    Boolean flag indicating if the user was just created (``True``) or already existed (``False``).

``request``
    The current HTTP request object.

Practical Example: Saving User Profile Data
--------------------------------------------

This example creates a ``Profile`` instance to store additional user information from Facebook.

**Understanding the Facebook Response**

The ``response`` parameter from Facebook typically looks like::

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

**Passing Data Forward**

The function above returns ``None``, which is fine if subsequent functions don't need 
the profile. To make the ``profile`` available to later pipeline functions, return a dict::

    def save_profile(backend, user, response, *args, **kwargs):
        if backend.name == 'facebook':
            profile = user.get_profile()
            if profile is None:
                profile = Profile(user_id=user.id)
            profile.gender = response.get('gender')
            profile.link = response.get('link')
            profile.timezone = response.get('timezone')
            profile.save()
            return {'profile': profile}  # Make profile available to next functions

Common Patterns and Tips
------------------------

**Conditional Execution**

Check the backend name to run logic for specific providers::

    def my_function(backend, **kwargs):
        if backend.name == 'google-oauth2':
            # Google-specific logic
            pass
        elif backend.name == 'facebook':
            # Facebook-specific logic
            pass

**Accessing Settings**

Use the strategy to access settings::

    def my_function(strategy, **kwargs):
        custom_setting = strategy.setting('MY_CUSTOM_SETTING')
        
**Making API Calls**

Use the access token from ``response`` to call provider APIs::

    def fetch_additional_data(backend, response, **kwargs):
        access_token = response.get('access_token')
        # Make API call using the token
        import requests
        api_response = requests.get(
            'https://provider-api.com/endpoint',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        return {'additional_data': api_response.json()}

**Debugging**

Log pipeline execution to understand the flow::

    import logging
    logger = logging.getLogger(__name__)
    
    def my_function(user, **kwargs):
        logger.debug(f'Pipeline function called for user: {user}')
        logger.debug(f'Available kwargs: {kwargs.keys()}')
        # Your logic here

.. _python-social-auth: https://github.com/python-social-auth
.. _example applications: https://github.com/python-social-auth/social-examples
