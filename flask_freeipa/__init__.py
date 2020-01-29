import python_freeipa as freeipa
from python_freeipa import Client#, ClientMeta
import kerberos
from flask import abort, current_app, g, make_response, \
        redirect, url_for, request
from socket import gethostname
import requests
import requests_kerberos

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


    def init_kerberos(app, service='HTTP', hostname=gethostname()):
        '''
        Configure the GSSAPI service name, and validate the presence of the
        appropriate principal in the kerberos keytab.
        :param app: a flask application
        :type app: flask.Flask
        :param service: GSSAPI service name
        :type service: str
        :param hostname: hostname the service runs under
        :type hostname: str
        '''
        global _SERVICE_NAME
        _SERVICE_NAME = "%s@%s" % (service, hostname)

        if 'KRB5_KTNAME' not in environ:
            app.logger.warn("Kerberos: set KRB5_KTNAME to your keytab file")
        else:
            try:
                principal = kerberos.getServerPrincipalDetails(service, hostname)
            except kerberos.KrbError as exc:
                app.logger.warn("Kerberos: %s" % exc.message[0])
            else:
                app.logger.info("Kerberos: server is %s" % principal)

    def auth_user(self, username, password):
        try:
            conn = Client(current_app.config['IPA_HOST'])
            #conn.login(username, password)
            conn.login_kerberos()
            return True
        except freeipa.exceptions:
            return

    def get_user_info(self, username):
        try:
            conn = Client(current_app.config['IPA_HOST'])
            conn.login_kerberos()
            #query = ClientMeta(current_app.config['IPA_HOST'])
            info = conn.user_show(username)
            return info
        except freeipa.exceptions as e:
            raise IPAException(self.error(e.args))

    def member_of(self, username):
        try:
            info = self.get_user_info(username)
            return info['memberof_group']
        except freeipa.exceptions as e:
             raise IPAException(self.error(e.args))

    #def list_groups(self):
    #    try:
