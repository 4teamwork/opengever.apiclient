from .. import Document
from ... import GEVERClient
from ...tests import TestCase


class TestDocumentModel(TestCase):

    def test_properties(self):
        document = GEVERClient(self.document_url, self.regular_user).fetch()
        self.assertIsInstance(document, Document)
        self.assertEqual('Verträgsentwurf', document.title)
        self.assertEqual('2016-08-31T14:07:33+00:00', document.created)
        self.assertEqual('Client1 1.1 / 1 / 14', document.reference_number)

    def test_raw(self):
        document = GEVERClient(self.document_url, self.regular_user).fetch()
        self.maxDiff = None
        self.assertDictContainsSubset(
            {
                'UID': 'createtreatydossiers000000000002',
                'allow_discussion': False,
                'archival_file_state': None,
                'bumblebee_checksum': '51d6317494eccc4a73154625a6820cb6b50dc1455eb4cf26399299d4f9ce77b2',
                'changeNote': '',
                'changed': '2016-08-31T14:07:33+00:00',
                'classification': 'unprotected',
                'created': '2016-08-31T14:07:33+00:00',
                'delivery_date': '2010-01-03T00:00:00',
                'description': 'Wichtige Verträge',
                'document_author': 'test_user_1_',
                'document_date': '2010-01-03T00:00:00',
                'document_type': 'contract',
                'file_extension': '.docx',
                'foreign_reference': None,
                'id': 'document-14',
                'is_folderish': False,
                'keywords': ['Wichtig'],
                'layout': 'tabbed_view',
                'modified': '2016-08-31T14:07:33+00:00',
                'preserved_as_paper': True,
                'preview': None,
                'privacy_layer': 'privacy_layer_no',
                'public_trial': 'unchecked',
                'public_trial_statement': None,
                'receipt_date': '2010-01-03T00:00:00',
                'reference_number': 'Client1 1.1 / 1 / 14',
                'relatedItems': [],
                'relative_path': 'ordnungssystem/fuehrung/vertraege-und-vereinbarungen/dossier-1/document-14',
                'review_state': 'document-state-draft',
                'thumbnail': None,
                'title': 'Verträgsentwurf',
            },
            document.raw)

    def test_url(self):
        document = GEVERClient(self.document_url, self.regular_user ).fetch()
        self.assertEqual(self.document_url, document.url)
