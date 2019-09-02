from urllib.parse import urlsplit

from tornado import gen
from tornado.escape import url_escape
from tornado.httputil import url_concat

from traitlets import (
    Unicode, Integer, Dict, TraitError, List, Bool, Any,
    Type, Set, Instance, Bytes, Float,
    observe, default,
)

from jupyterhub.auth import Authenticator
from jupyterhub.handlers.login import LoginHandler, LogoutHandler

from oauthenticator.oauth2 import OAuthCallbackHandler
from oauthenticator.generic import GenericOAuthenticator, GenericLoginHandler
from firstuseauthenticator.firstuseauthenticator import FirstUseAuthenticator

import pdb

class MultiLoginHandler(LoginHandler):
    def _render(self, login_error=None, username=None):
        return self.render_template('login_multi.html',
                next=url_escape(self.get_argument('next', default='')),
                username=username,
                login_error=login_error,
                custom_html=self.authenticator.custom_html,
                login_url=self.settings['login_url'],
                authenticator_login_url=url_concat(
                    self.authenticator.login_url(self.hub.base_url),
                    {'next': self.get_argument('next', '')},
                ),
        )
        
class MultiLogoutHandler(LogoutHandler):
    def get(self):
        user = self.get_current_user()
        if user.spawner is not None and user.spawner.active:
            user.spawner.stop()
        if user:
            self.log.info("User logged out: %s", user.name)
            self.clear_login_cookie()
            self.statsd.incr('logout')
        if self.authenticator.auto_login:
            html = self.render_template('logout.html')
            self.finish(html)
        else:
            self.redirect(self.settings['login_url'], permanent=False)

class MultiAuthenticator(Authenticator):

    first_use_class = Type(FirstUseAuthenticator, Authenticator, help='Must be an authenticator').tag(config=True)
    oauth_class = Type(GenericOAuthenticator, Authenticator, help='Must be an authenticator').tag(config=True)

    first_use_auth = Instance(Authenticator)
    oauth_auth = Instance(Authenticator)

    login_service = "HBP"

    @default('first_use_auth')
    def _default_first_use_auth(self):
        return self.first_use_class()

    @default('oauth_auth')
    def _default_oauth_auth(self):
        return self.oauth_class()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__client_id = None
        self.__client_secret = None
        self.__scope = None
        self.log.info(self.oauth_auth.client_id)

    def _user_exists(self, user):
        return self.first_use_auth._user_exists(user)

    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def scope(self):
        return ["openid"]

    def set_oauth_tokens(self, subauth):
        """
        Caches configured information from the subauthenticator in properties
        """
        self.log.info(subauth.client_id)
        self.__client_id = subauth.client_id
        self.__client_secret = subauth.client_secret
        self.__scope = subauth.scope

    def get_callback_url(self, handler=None):
        """
        This is called by oauth2, it thinks that there will just be one 
        """
        self.set_oauth_tokens(self.oauth_auth)
        return self.oauth_auth.get_callback_url(handler)

    def validate_username(self, username):
        return self.first_use_auth.validate_username(username)

    def login_url(self, base_url):
        return self.oauth_auth.login_url(base_url)

    def get_handlers(self, app):
        h = [
            ('/login', MultiLoginHandler),
            ('/logout', MultiLogoutHandler),
        ]
        h.extend(self.oauth_auth.get_handlers(app))
        h.extend(self.first_use_auth.get_handlers(app))
        return h

    def authenticate(self, handler, data):
        """
        Delegate authentication to the appropriate authenticator
        """
        if isinstance(handler, OAuthCallbackHandler):
            return self.oauth_auth.authenticate(handler, data)
        else:
            return self.first_use_auth.authenticate(handler, data)
