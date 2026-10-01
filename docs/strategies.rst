Strategies
==========

Different strategies are defined to encapsulate the different frameworks
capabilities under a common API to reuse as much code as possible.


Description
-----------

A strategy's responsibility is to provide access to:

* Request data and host information and URI building
* Session access
* Project settings
* Response types (HTML and redirects)
* HTML rendering

Different frameworks implement these features on different ways, thus the need
for these interfaces.


Implementing a new Strategy
---------------------------

The following methods must be defined on strategies sub-classes.

Request::

    def get_request_data(self, merge=True):
        """Return current framework request data (POST or GET)"""
        raise NotImplementedError('Implement in subclass')

    def request_host(self):
        """Return current host value"""
        raise NotImplementedError('Implement in subclass')

    def build_absolute_uri(self, path=None):
        """Build absolute URI with given (optional) path"""
        raise NotImplementedError('Implement in subclass')


Session::

    def session_get(self, name):
        """Return session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def session_set(self, name, value):
        """Set session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def session_pop(self, name):
        """Pop session value for given key"""
        raise NotImplementedError('Implement in subclass')


Settings::

    def get_setting(self, name):
        """Return value for given setting name"""
        raise NotImplementedError('Implement in subclass')


Responses::

    def html(self, content):
        """Return HTTP response with given content"""
        raise NotImplementedError('Implement in subclass')

    def redirect(self, url):
        """Return a response redirect to the given URL"""
        raise NotImplementedError('Implement in subclass')

    def render_html(self, tpl=None, html=None, context=None):
        """Render given template or raw html with given context"""
        raise NotImplementedError('Implement in subclass')


Effective pipeline request data
-------------------------------

``strategy.request`` holds the native framework request, when the integration
provides one. It is never replaced by saved partial-pipeline parameters.

``strategy.get_request_data(merge=True)`` reads the current framework request.
With ``merge=False``, it reads the data for the current request method, following
the framework integration's existing behavior. Custom strategies implement this
hook instead of overriding ``request_data()``.

``strategy.request_data(merge=True)`` returns the effective parameters for the
active pipeline. During a partial resume, this includes any confirmed data
replayed from an external validation link. Both values of ``merge`` return the
same effective mapping during replay, because saved data no longer has a
separate GET or POST origin. Use ``get_request_data()``, ``request_get()``, or
``request_post()`` when the current framework request is required.

The effective mapping is scoped to execution of the resumed authentication or
disconnect pipeline. The previous mapping is restored when execution completes,
returns a response, or raises an exception. Nested executions restore the outer
mapping. Integration code can establish the same scope with
``strategy.pipeline_request_data(data)`` as a context manager.

Migrating to social-auth-core 6 and social-auth-app-django 7
------------------------------------------------------------

* Rename custom ``request_data()`` overrides to ``get_request_data()``. Keep
  framework extraction, validation, and application-specific defaults in that
  hook; allow the inherited ``request_data()`` method to handle replay.
* Replace pipeline ``request`` parameters and ``kwargs['request']`` reads with
  ``strategy.request_data()`` for effective parameters, or ``strategy.request``
  for a native framework request. Pipeline steps no longer receive an automatic
  ``request`` argument.
* Upgrade framework adapters together with social-auth-core. Adapters that
  override the old hook must migrate before using core 6.

Partial request data is stored separately from pipeline arguments. Existing
partials with a request mapping in ``kwargs['request']`` are converted when
loaded, so upgrading does not require a database schema migration or discarding
pending authentication flows.

Partials are bound to their authentication or disconnect pipeline. Legacy
disconnect partials without a pipeline type must restart the disconnect flow
so its permission checks run.
