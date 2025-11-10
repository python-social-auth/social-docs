Telegram
========

Telegram uses a widget-based authentication method for login.

- Create a bot using `BotFather`_ on Telegram to get a bot token.

- Add Telegram backend to ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.telegram.TelegramAuth',
        ...
    )

- Fill ``Bot Token`` value in the settings::

    SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = ''

- Add the Telegram Login Widget to your login page. The widget should be configured
  to send authentication data to your callback URL, which should be something like
  ``http://example.com/complete/telegram/`` replacing ``example.com`` with your domain.

- The Telegram Login Widget can be added using the following HTML::

    <script async src="https://telegram.org/js/telegram-widget.js?22"
            data-telegram-login="YOUR_BOT_USERNAME"
            data-size="large"
            data-auth-url="http://example.com/complete/telegram/"
            data-request-access="write"></script>

  Replace ``YOUR_BOT_USERNAME`` with your bot's username (without the @ symbol)
  and update the ``data-auth-url`` to match your domain.

- The authentication process verifies the data integrity using HMAC-SHA256 with
  the bot token. Authentication data is considered valid for 24 hours from the
  ``auth_date`` timestamp.

- The backend extracts the following user information:
  - User ID (required)
  - Username
  - First name
  - Last name
  - Photo URL (if available)

.. _BotFather: https://t.me/botfather
