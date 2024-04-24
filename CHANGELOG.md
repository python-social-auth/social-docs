# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased](https://github.com/python-social-auth/social-docs/commits/master)

### Added
- Added Facebook Limited Login backend documentation.
- Added Seznam OAuth2 backend documentation.
- Added Grafana OAuth2 backend documentation.
- Added note on using extra auth arguments in Coinbase backend.
- Added note on using tenants in Azure AD backend.
- Added note about Microsoft Graph support with AzureAD backend.
- Added Slack team limit setting
- Added Bungie OAuth2 backend documentation
- Added documentation about enabling PostgreSQL JSONB field type
- Added Eventbrite OAuth2 backend documentation
- Added note about `SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION` option
- Added note about `SOCIAL_AUTH_SHOPIFY_API_VERSION` setting
- Added SimpleLogin backend documentation.
- Added GithubApp backend documentation.
- Added Discourse backend documentation
- Added Okta backends documentation
- Added note about `SOCIAL_AUTH_UNTAPPD_USER_AGENT` setting
- Added `ACCESS_TOKEN_METHOD` backend attribute documentation
- Added Cognito backend documentation
- Added Flat backend documentation
- Added Patreon OAuth2 backend documentation
- Added details about ORCID `Member API` support
- Added use-case about improved unicode cleanup from usernames
- Added documentation for gitea backend
- Added Twitter API v2 backend documentation
- Added "OAuth2 with PKCE" instructions under "Adding a new backend"
- Added Bitbucket Data Center OAuth2 backend documentation
- Added Etsy OAuth2 backend documentation
- Added OpenStreetMap OAuth2 backend documentation.

### Changed
- Update partial-pipeline docs with the new storage solution details.
- Update django context-processors format
- Updated Steam documentation
- Updated LinkedIn documentation
- Updated NonceMixin documentation for the new `get` and `delete` class methods
- Fix `associated_by_email` position in `PIPELINE` documentation
- Several grammar changes
- Correct `OpenID` name
- Fixed typos on pipeline documentation
- Use gender-neutral pronouns (his -> their)
- Updated Twitter documentation detailing callback URL addition
- Updated details bout email validation setting
- Updated details about `partial_token` in email validation flow

## [0.1.0](https://github.com/python-social-auth/social-docs/releases/tag/0.1.0) - 2016-12-31

### Added
- Added GitLab OAuth2 backend documentation
- Added note about OAuth1 expected access_token format.
  Refs [#647](https://github.com/omab/python-social-auth/issues/647)
- Added reference to `SOCIAL_AUTH_USER_AGENT` setting.
- Added reference to Python3 SAML support
- Added details about Django `messages` app usage in the exception middleware.
  Refs [#873](https://github.com/omab/python-social-auth/issues/873)
- Document SOCIAL_AUTH_FACEBOOK_API_VERSION setting
- Added documentation about Django Admin `SOCIAL_AUTH_ADMIN_SEARCH_FIELDS` setting
- Added docs about Lyft backend (port from [#1036](https://github.com/omab/python-social-auth/pull/1036)
  by iampark)
- Added docs about per-backend pipeline (port from [#1019](https://github.com/omab/python-social-auth/pull/1019)
  by keattang)
- Added docs about Mailchimp backend (port from [#1037](https://github.com/omab/python-social-auth/pull/1037)
  by svvitale)
- Added docs about Shimmering backend (port from [#1054](https://github.com/omab/python-social-auth/pull/1054)
  by iamkhush)
- Added example of link usage for Django (port from [#1060](https://github.com/omab/python-social-auth/pull/1060)
  by vladimirnani)
- Added Quizlet backend (port from [#1012](https://github.com/omab/python-social-auth/pull/1012)
  by s-alexey)

### Changed
- Updated the documentation about installing the library
- Updated reference to username cleanup regular expressions.
  Refs [#732](https://github.com/omab/python-social-auth/issues/732)
- Updated backend example using `json.load(urlopen())` instead of `self.get_json()` helper.
  Refs [#767](https://github.com/omab/python-social-auth/issues/767)
- Removed entry about removed backend (port of [#1046](https://github.com/omab/python-social-auth/pull/1046)
  by browniebroke)
- Updated Flask documentation regarding the db session paramter (port fro [#1050](https://github.com/omab/python-social-auth/pull/1050)
  by duffn)
- Updated Dropbox backend (port from [#1018](https://github.com/omab/python-social-auth/pull/1018)
  by illing2005)
- Split from the monolitic [python-social-auth](https://github.com/omab/python-social-auth)
  codebase
