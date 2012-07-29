from django.test import TestCase

from iprestrict import models
from iprestrict import restrictor

from datetime import datetime

class MiddlewareRestrictsTest(TestCase):
    '''
    When the middleware is enabled it should restrict all IPs(but localhost)/URLs by default.
    '''
    def setUp(self):
        models.ReloadRulesRequest.request_reload()

    def assert_url_is_restricted(self, url):
        response = self.client.get(url, REMOTE_ADDR = '192.168.1.1')
        self.assertEqual(response.status_code, 403)

    def assert_ip_is_restricted(self, ip):
        response = self.client.get('', REMOTE_ADDR = ip)
        self.assertEqual(response.status_code, 403)

    def test_middleware_restricts_every_url(self):
        self.assert_url_is_restricted('')
        self.assert_url_is_restricted('/every')
        self.assert_url_is_restricted('/url')
        self.assert_url_is_restricted('/is_restricted')
        self.assert_url_is_restricted('/every/url/is_restricted')

    def test_middleware_restricts_ips(self):
        #self.assert_ip_is_restricted('127.0.0.1')
        self.assert_ip_is_restricted('192.168.1.1')
        self.assert_ip_is_restricted('10.10.10.1')
        self.assert_ip_is_restricted('169.254.0.1')

LOCAL_IP = '192.168.1.1'
def create_ip_allow_rule(ip=LOCAL_IP):
    localip = models.IPGroup.objects.create(name='localip')
    models.IPRange.objects.create(ip_group=localip, first_ip='192.168.1.1')
    models.Rule.objects.create(url_pattern='ALL', ip_group = localip, action='A')

class MiddlewareAllowsTest(TestCase):
    def setUp(self):
        create_ip_allow_rule()
        models.ReloadRulesRequest.request_reload()

    def test_middleware_allows_localhost(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 404)

    def test_middleware_allows_ip_just_added(self):
        response = self.client.get('', REMOTE_ADDR = LOCAL_IP)
        self.assertEqual(response.status_code, 404)

    def test_middleware_restricts_other_ip(self):
        response = self.client.get('', REMOTE_ADDR = '10.1.1.1')
        self.assertEqual(response.status_code, 403)

class ReloadRulesTest(TestCase):
    def setUp(self):
        create_ip_allow_rule()

    def test_reload_with_custom_command(self):
        from django.core.management import call_command
        call_command('reloadrules', verbosity=0)

        response = self.client.get('', REMOTE_ADDR = LOCAL_IP)
        self.assertEqual(response.status_code, 404)

