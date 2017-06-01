from collections import namedtuple
from django.test import TestCase

from jarbas.core.models import Reimbursement
from jarbas.dashboard.admin import ReimbursementModelAdmin


Request = namedtuple('Request', ('method',))
ReimbursementMock = namedtuple('Reimbursement', ('cnpj_cpf'))


class TestDashboardSite(TestCase):

    def setUp(self):
        self.requests = map(Request, ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'))
        self.ma = ReimbursementModelAdmin(Reimbursement, 'dashboard')

    def test_has_add_permission(self):
        permissions = map(self.ma.has_add_permission, self.requests)
        self.assertNotIn(True, tuple(permissions))

    def test_has_change_permission(self):
        permissions = map(self.ma.has_change_permission, self.requests)
        expected = (True, False, False, False, False)
        self.assertEqual(expected, tuple(permissions))

    def test_has_delete_permission(self):
        permissions = map(self.ma.has_delete_permission, self.requests)
        self.assertNotIn(True, tuple(permissions))

    def test_format_document(self):
        obj1 = ReimbursementMock('12345678901234')
        obj2 = ReimbursementMock('12345678901')
        obj3 = ReimbursementMock('2345678')
        self.assertEqual('12.345.678/9012-34', self.ma._format_document(obj1))
        self.assertEqual('123.456.789-01', self.ma._format_document(obj2))
        self.assertEqual('2345678', self.ma._format_document(obj3))
