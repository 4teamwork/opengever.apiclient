from .. import Dossier
from ... import GEVERClient
from ...tests import TestCase


class TestDossierModel(TestCase):

    def test_dossier_properties(self):
        dossier = GEVERClient(self.dossier_url, self.regular_user).fetch()
        self.assertIsInstance(dossier, Dossier)
        self.assertEqual('Verträge mit der kantonalen Finanzverwaltung', dossier.title)
        self.assertEqual('2016-08-31T14:01:33+00:00', dossier.created)

    def test_dossier_raw(self):
        dossier = GEVERClient(self.dossier_url, self.regular_user).fetch()
        self.maxDiff = None
        self.assertDictContainsSubset(
            {
                'UID': 'createtreatydossiers000000000001',
            },
            dossier.raw
        )

    def test_dossier_url(self):
        dossier = GEVERClient(self.dossier_url, self.regular_user).fetch()
        self.assertEqual(self.dossier_url, dossier.url)
