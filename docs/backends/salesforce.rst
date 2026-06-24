Salesforce
==========

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``salesforce-oauth2``
     - ``social_core.backends.salesforce.SalesforceOAuth2``
   * - ``salesforce-oauth2-sandbox``
     - ``social_core.backends.salesforce.SalesforceOAuth2Sandbox``

Salesforce uses OAuth v2 for Authentication, check the `official docs`_.

- Create an app following the steps in the `Defining Connected Apps`_ docs.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

        SOCIAL_AUTH_SALESFORCE_OAUTH2_KEY = '<App UID>'
        SOCIAL_AUTH_SALESFORCE_OAUTH2_SECRET = '<App secret>'

- Add the backend to the ``AUTHENTICATION_BACKENDS`` setting::

        AUTHENTICATION_BACKENDS = (
            ...
            'social_core.backends.salesforce.SalesforceOAuth2',
            ...
        )

- Then you can start authentication from your templates with a POST form::

        <form method="post" action="{% url 'social:begin' 'salesforce-oauth2' %}">
            {% csrf_token %}
            <button type="submit">Sign in with Salesforce</button>
        </form>


If using the sandbox mode:

- Fill these settings instead::

        SOCIAL_AUTH_SALESFORCE_OAUTH2_SANDBOX_KEY = '<App UID>'
        SOCIAL_AUTH_SALESFORCE_OAUTH2_SANDBOX_SECRET = '<App secret>'

- And this backend::

        AUTHENTICATION_BACKENDS = (
            ...
            'social_core.backends.salesforce.SalesforceOAuth2Sandbox',
            ...
        )

- Then you can start authentication from your templates with a POST form::

        <form method="post" action="{% url 'social:begin' 'salesforce-oauth2-sandbox' %}">
            {% csrf_token %}
            <button type="submit">Sign in with Salesforce Sandbox</button>
        </form>

.. _official docs: https://www.salesforce.com/us/developer/docs/api_rest/Content/intro_understanding_web_server_oauth_flow.htm
.. _Defining Connected Apps: https://www.salesforce.com/us/developer/docs/api_rest/Content/intro_defining_remote_access_applications.htm
