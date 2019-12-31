import python_freeipa
from python_freeipa import Client
from flask import abort, current_app, g, make_response, \
        redirect, url_for, request

__all__ = ['IPA']

class IPAException(RuntimeError):
    message = None

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class IPA(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        """
        Initialize the `app` for use with this :class:`~IPA`.
        This is called automatically if `app` is passed
        to :meth:`~IPA.__init__`.

        :param flask.Flask app: the application to configure
        for use with this :class:`~IPA`
        """

        app.config.setdefault('IPA_HOST', 'localhost')
        app.config.setdefault('IPA_USERNAME', None)
        app.config.setdefault('IPA_PASSWORD', None)

    @property
    def initialize(self):
        """Initialize a connection to the IPA server.

        :return: IPA connection object.
        """

        try:
            conn = Client(current_app.config['IPA_HOST'])
            conn.login(current_app.config['IPA_USERNAME'],
                    current_app.config['IPA_PASSWORD'])
            return conn
        except freeipa.exceptions as e:
            raise IPAException(self.error(e.args))


    def auth_user(self, username, password):
        try:
            conn = Client(current_app.config['IPA_HOST'])
            conn.login(username, password)
            return True
        except freeipa.exceptions:
            return


