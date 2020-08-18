from base64 import b64encode

from .models import ModelRegistry
from .session import GEVERSession
from .utils import autowrap


class GEVERClient:
    """The GEVERClient is used for communicating with GEVER through the GEVER REST API.
    It is instantiated for a specific GEVER resource in the name of a specific user.
    """

    def __init__(self, url, username, headers={}):
        """
        :param url: The base URL to a resource in GEVER without the view.
        :type url: string
        :param username: A GEVER username. All actions are performed in the name
          of this user.
        :type username: string
        """
        self.url = url.rstrip("/")  # Remove trailing slash(es).
        self.username = username
        self.session = GEVERSession(url, username, headers)

    def adopt(self, url):
        """Create and return a new GEVERClient instance for the passed url.
        :param url: The base URL to a resource in GEVER without the view.
        :type url: string
        """
        return type(self)(url, self.username)

    def wrap(self, item):
        """Wrap an item into a API model object.
        """
        return ModelRegistry.wrap(item, self)

    @autowrap
    def fetch(self):
        """Fetch the full object with the configured URL and return the object
        representation.
        """
        return self.session().get(self.url).json()

    @autowrap
    def create_dossier(self, title, **data):
        data.setdefault('responsible', self.username)
        data.update({'@type': 'opengever.dossier.businesscasedossier',
                     'title': title})
        return self.session().post(self.url, json=data).json()

    def get_navigation(self, raw=False):
        if not raw:
            raise NotImplementedError(
                'get_navigation currently does not support autowrapping its items, please use raw=True.'
            )
        return self.session().get(f'{self.url}/@navigation').json()

    def listing(self, name, columns=[], raw=False, **kwargs):
        """
        Listing of specific types for given URL (https://docs.onegovgever.ch/dev-manual/api/listings/)
        Results are casted into model objects.
        """
        kwargs['name'] = name

        kwargs['columns:list'] = ['@type']
        kwargs['columns:list'].extend(columns)

        response = self.session().get(f'{self.url}/@listing', params=kwargs).json()
        if raw:
            return response

        response['items'] = [self.wrap(item=item) for item in response['items']]
        return response

    def update_object(self, **data):
        return self.session().patch(self.url, json=data).ok

    def get_office_connector_url(self):
        """
        Returns the Office Connector checkout url ("oc:....") for the GEVER document located at `self.url`.
        """
        return self.session().get(f"{self.url}/officeconnector_checkout_url").json()["url"]

    def allowed_roles_and_principals(self):
        """
        This feature was introduced in opengever.core 2020.3.0. To do: define testing setup for multiple GEVER versions.
        """
        return (
            self.session()
            .get(f'{self.url}/@allowed-roles-and-principals')
            .json()['allowed_roles_and_principals']
        )

    def user(self):
        """
        This feature was introduced in opengever.core 2020.3.0. To do: define testing setup for multiple GEVER versions.
        """
        return self.session().get(f'{self.url}/@users/{self.username}').json()

    @autowrap
    def create_document(self, title, file, content_type, filename, size=None):
        """
        :param title: The title of the document
        :param file: Readable IO which holds the content of the file
        :param content_type: The content type of the document
        :param filename: The filename of the document
        :param size: The size of the file, if omitted file.size is used
        """
        if size is None:
            size = file.size
        size = str(size)

        b64_filename = str(b64encode(filename.encode('utf-8')), 'utf-8')
        b64_content_type = str(b64encode(content_type.encode('utf-8')), 'utf-8')
        b64_portal_type = str(b64encode(b'opengever.document.document'), 'utf-8')
        tus = self.session().post(f'{self.url}/@tus-upload', headers={
            'Tus-Resumable': '1.0.0',
            'Upload-Length': size,
            'Upload-Metadata': f'filename {b64_filename},content-type {b64_content_type},@type {b64_portal_type}',
        })

        created_document = self.session().patch(
            tus.headers['Location'],
            headers={
                'Tus-Resumable': '1.0.0',
                'Upload-Offset': '0',
                'Content-Type': 'application/offset+octet-stream'
            },
            data=file,
        )

        return self.session().get(created_document.headers['Location']).json()
