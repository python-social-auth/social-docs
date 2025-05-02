VK.com (former Vkontakte)
=========================

VK.com (former Vkontakte) auth service support.

OAuth2
------

VK.com uses OAuth2 for Authentication.

- Register a new application at the `VK.com API`_,

- fill ``Application Id`` and ``Application Secret`` values in the settings::

      SOCIAL_AUTH_VK_OAUTH2_KEY = ''
      SOCIAL_AUTH_VK_OAUTH2_SECRET = ''

- Add ``'social_core.backends.vk.VKOAuth2'`` into your ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

- Then you can start using ``/login/vk-oauth2`` in your link href.

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_VK_OAUTH2_SCOPE = [...]

  See the `VK.com list of permissions`_.


OAuth2 Application
------------------

To support OAuth2 authentication for VK.com applications:

- Create your IFrame application at VK.com.

- In application settings specify your IFrame URL ``https://mysite.com/complete/vk-app`` (current
  default).

- In application settings specify the first API request. For example::

    method=getProfiles&uids={viewer_id}&format=json&v=5.53&fields=id,first_name,last_name,screen_name,photo

  See the `documentation on available fields`_.

- Add ``'social_core.backends.vk.VKAppOAuth2'`` into your ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

- Fill ``Application ID`` and ``Application Secret`` settings::

    SOCIAL_AUTH_VK_APP_KEY = ''
    SOCIAL_AUTH_VK_APP_SECRET = ''

- Fill ``user_mode``::

    SOCIAL_AUTH_VK_APP_USER_MODE = 2

  Possible values:
    - ``0``: there will be no check whether a user connected to your
      application or not
    - ``1``: ``python-social-auth`` will check ``is_app_user`` parameter
      VK.com sends when user opens application page one time
    - ``2``: (safest) ``python-social-auth`` will check status of user
      interactively (useful when you have interactive authentication via AJAX)

- Add a snippet similar to this into your login template::

    <script src="http://vk.com/js/api/xd_connection.js?2" type="text/javascript"></script>
    <script type="text/javascript">
        VK.init(function() {
                VK.addCallback("onApplicationAdded", requestRights);
                VK.addCallback("onSettingsChanged", onSettingsChanged);
            }
        );

        function startConnect() {
            VK.callMethod('showInstallBox');
        }

        function requestRights() {
            VK.callMethod('showSettingsBox', 1 + 2); // 1+2 is just an example
        }

        function onSettingsChanged(settings) {
            window.location.reload();
        }
    </script>
    <a href="#" onclick="startConnect(); return false;">Click to authenticate</a>

To test, launch the server using ``sudo ./manage.py mysite.com:80`` for
browser to be able to load it when VK.com calls IFrame URL. Open your
VK.com application page via http://vk.com/app<app_id>. Now you are able to
connect to application and login automatically after connection when visiting
application page.

For more details see `authentication for VK.com applications`_


OpenAPI
-------

You can also use VK.com's own OpenAPI to log in, but you need to provide
HTML template with JavaScript code to authenticate, check below for an example.

- Get an OpenAPI App Id and add it to the settings::

    SOCIAL_AUTH_VK_OPENAPI_APP_ID = ''

  This app id will be passed to the template as ``VK_APP_ID``.

- Add ``'social_core.backends.vk.VKontakteOpenAPI'`` into your ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

Snippet example::

    <script src="http://vk.com/js/api/openapi.js" type="text/javascript"></script>
    <script type="text/javascript">
        var vkAppId = {{ VK_APP_ID|default:"null" }};
        if (vkAppId) {
            VK.init({ apiId: vkAppId });
        }
        function authVK () {
            if (!vkAppId) {
                alert ("Please specify VK.com APP ID in your local settings file");
                return false;
            }
            VK.Auth.login(function(response) {
                var params = "";
                if (response.session) {
                    params = "first_name=" + encodeURI(response.session.user.first_name) + "&last_name=" + encodeURI(response.session.user.last_name);
                    params += "&nickname=" + encodeURI(response.session.user.nickname) + "&id=" + encodeURI(response.session.user.id);
                }
                window.location = "{{ VK_COMPLETE_URL }}?" + params;
            });
            return false;
        }
    </script>
    <a href="javascript:void(0);" onclick="authVK();">Click to authorize</a>


.. _VK.com OAuth: https://vk.com/dev/authentication
.. _VK.com list of permissions: https://dev.vk.com/reference/access-rights
.. _VK.com API: https://dev.vk.com/method
.. _authentication for VK.com applications: http://www.ikrvss.ru/2011/11/08/django-social-auh-and-vkontakte-application/
.. _documentation on available fields: https://vk.com/pages?oid=-17680044&p=getProfiles
