Django Quickstart Guide
=======================

This quickstart guide will help you add Python Social Auth to a fresh Django project quickly and with minimal friction. It walks through setting up social authentication with Google OAuth2 as an example, but the steps apply to other providers with minor modifications.

Prerequisites
-------------

- Python 3.6 or higher
- Basic knowledge of Django
- A Google account (for creating OAuth2 credentials)


Step 1: Create a New Django Project
------------------------------------

First, let's create a fresh Django project::

    $ pip install django
    $ django-admin startproject mysite
    $ cd mysite


Step 2: Install Python Social Auth
-----------------------------------

Install the Django integration for Python Social Auth::

    $ pip install social-auth-app-django


Step 3: Configure Database
---------------------------

.. important::
   **Database Considerations**: SQLite has limitations with the default schema that can cause issues with Python Social Auth, particularly with the ``uid`` field length. We recommend using PostgreSQL or MySQL for production deployments.

To use **PostgreSQL** (recommended)::

    $ pip install psycopg2-binary

Then update ``DATABASES`` in ``settings.py``::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mysite_db',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

To use **MySQL**::

    $ pip install mysqlclient

Then update ``DATABASES`` in ``settings.py``::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mysite_db',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

    # MySQL InnoDB has a 767 byte limit on index columns
    # This setting prevents errors with the uid field
    SOCIAL_AUTH_UID_LENGTH = 223

.. note::
   If you must use SQLite for development, add this setting to avoid field length issues::

       SOCIAL_AUTH_UID_LENGTH = 223


Step 4: Register the Application
---------------------------------

Add ``social_django`` to ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'social_django',  # Add this
    ]


Step 5: Configure Authentication Backends
------------------------------------------

Add the authentication backends to ``settings.py``. Here's an example for Google OAuth2::

    AUTHENTICATION_BACKENDS = [
        'social_core.backends.google.GoogleOAuth2',  # Google OAuth2
        'django.contrib.auth.backends.ModelBackend',  # Django default
    ]

.. note::
   Keep ``django.contrib.auth.backends.ModelBackend`` so users can still log in with username/password.

For other providers, check the :doc:`/backends/index` section. Common backends include:

- ``'social_core.backends.github.GithubOAuth2'`` - GitHub
- ``'social_core.backends.facebook.FacebookOAuth2'`` - Facebook
- ``'social_core.backends.twitter.TwitterOAuth'`` - Twitter


Step 6: Get OAuth2 Credentials
-------------------------------

Before configuring your application, you need to obtain OAuth2 credentials from Google:

1. Go to the `Google Cloud Console <https://console.cloud.google.com/>`_
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth client ID**
5. Choose **Web application**
6. Add authorized redirect URIs::

       http://localhost:8000/complete/google-oauth2/

7. Save and copy your **Client ID** and **Client Secret**

.. tip::
   For production, add your production domain to authorized redirect URIs::

       https://yourdomain.com/complete/google-oauth2/


Step 7: Configure OAuth Keys and Settings
------------------------------------------

.. important::
   **This is where you configure the** ``client_id``, ``client_secret``, **and** ``scope`` **for your social login provider.**

Add these settings to ``settings.py`` (replace with your actual credentials)::

    # Google OAuth2 Configuration
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-client-id.apps.googleusercontent.com'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-client-secret'
    
    # Optional: Define the scope (what information you want to access)
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]

.. warning::
   **Never commit credentials to version control!** Consider using environment variables::

       import os
       
       SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_KEY')
       SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_OAUTH2_SECRET')

**For other providers**, the pattern is similar::

    # GitHub
    SOCIAL_AUTH_GITHUB_KEY = 'your-github-client-id'
    SOCIAL_AUTH_GITHUB_SECRET = 'your-github-client-secret'
    SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']
    
    # Facebook
    SOCIAL_AUTH_FACEBOOK_KEY = 'your-facebook-app-id'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'your-facebook-app-secret'
    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile']

The general pattern is ``SOCIAL_AUTH_<BACKEND_NAME>_KEY`` and ``SOCIAL_AUTH_<BACKEND_NAME>_SECRET``.


Step 8: Configure URL Settings
-------------------------------

Add common URL configuration settings to ``settings.py``::

    # Where to redirect after successful login
    LOGIN_REDIRECT_URL = '/'
    
    # Where to redirect after logout
    LOGOUT_REDIRECT_URL = '/'
    
    # Where to redirect if login fails
    SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
    
    # Standard Django login URL
    LOGIN_URL = '/login/'


Step 9: Configure URLs
-----------------------

Add social auth URLs to your project's ``urls.py``::

    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('social_django.urls', namespace='social')),
    ]


Step 10: Add Context Processors (Optional)
-------------------------------------------

To access social auth data in templates, add the context processors to ``settings.py``::

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    # Add these:
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                ],
            },
        },
    ]


Step 11: Run Migrations
------------------------

Create the database tables for social auth::

    $ python manage.py migrate


Step 12: Create a Login Page
-----------------------------

Create a simple template to test the login. First, add a view in your app's ``views.py``::

    from django.shortcuts import render
    from django.contrib.auth.decorators import login_required
    
    def login_page(view):
        return render(request, 'login.html')
    
    @login_required
    def home(request):
        return render(request, 'home.html')

Create a ``templates/login.html`` file::

    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h1>Login with Social Auth</h1>
        <a href="{% url 'social:begin' 'google-oauth2' %}">Login with Google</a>
    </body>
    </html>

Create a ``templates/home.html`` file::

    <!DOCTYPE html>
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome, {{ user.username }}!</h1>
        <p>Email: {{ user.email }}</p>
        <a href="{% url 'logout' %}">Logout</a>
    </body>
    </html>

Add the views to your ``urls.py``::

    from django.contrib.auth.views import LogoutView
    from myapp import views
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.home, name='home'),
        path('login/', views.login_page, name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('', include('social_django.urls', namespace='social')),
    ]


Step 13: Test the Setup
------------------------

Start the development server::

    $ python manage.py runserver

Visit ``http://localhost:8000/login/`` and click the "Login with Google" link. You should be redirected to Google's authentication page.


Common Settings You'll Want to Customize
-----------------------------------------

Here are additional settings you may want to add to ``settings.py`` based on your needs:

**Force profile information update on every login**::

    SOCIAL_AUTH_GOOGLE_OAUTH2_ALWAYS_UPDATE_USER_DATA = True

**Request additional permissions** (e.g., access to Google Drive)::

    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/drive.readonly',
    ]

**Use the full email as the username**::

    SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

**Store extra data from the provider**::

    SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['id', 'name', 'email']

**Restrict authentication to specific email domains**::

    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['example.com', 'mycompany.com']

**Restrict to specific email addresses**::

    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = ['user@example.com']

**Enable PostgreSQL JSON field for extra_data** (recommended for PostgreSQL)::

    SOCIAL_AUTH_JSONFIELD_ENABLED = True

**Sanitize redirects for security**::

    SOCIAL_AUTH_SANITIZE_REDIRECTS = True

**Force HTTPS redirects** (for production behind a reverse proxy)::

    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


Troubleshooting
---------------

**"Invalid redirect_uri" error**
    Make sure the redirect URI in your Google Console matches exactly: ``http://localhost:8000/complete/google-oauth2/``

**"The uid field is too long" database error**
    Add ``SOCIAL_AUTH_UID_LENGTH = 223`` to your settings, especially when using MySQL/InnoDB.

**Users can't log in with username/password**
    Make sure ``'django.contrib.auth.backends.ModelBackend'`` is in your ``AUTHENTICATION_BACKENDS``.

**Can't find where to set client_id and secret**
    They go directly in your Django ``settings.py`` file as ``SOCIAL_AUTH_<PROVIDER>_KEY`` and ``SOCIAL_AUTH_<PROVIDER>_SECRET``.


Next Steps
----------

- Read the full :doc:`django` configuration guide for advanced options
- Check the :doc:`/backends/index` for provider-specific documentation
- Learn about customizing the :doc:`/pipeline` to modify user creation behavior
- See :doc:`/configuration/settings` for all available configuration options


Complete Example settings.py
-----------------------------

Here's a complete example of what your ``settings.py`` might look like::

    import os
    from pathlib import Path
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = 'your-secret-key'
    DEBUG = True
    ALLOWED_HOSTS = []
    
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'social_django',
    ]
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    ROOT_URLCONF = 'mysite.urls'
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                ],
            },
        },
    ]
    
    WSGI_APPLICATION = 'mysite.wsgi.application'
    
    # Database - Using PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mysite_db',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    
    # Authentication
    AUTHENTICATION_BACKENDS = [
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    ]
    
    # Python Social Auth - Google OAuth2
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_KEY')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_OAUTH2_SECRET')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]
    
    # Social Auth URLs
    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'
    
    # Optional: Additional Social Auth settings
    SOCIAL_AUTH_JSONFIELD_ENABLED = True
    SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = False
    SOCIAL_AUTH_SANITIZE_REDIRECTS = True
    
    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]
    
    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True
    
    # Static files
    STATIC_URL = 'static/'
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
