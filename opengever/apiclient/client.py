from urllib.parse import quote

from .models import ModelRegistry
from .session import GEVERSession
from .utils import autowrap


class GEVERClient:
    """The GEVERClient is used for communicating with GEVER through the GEVER REST API.
    It is instantiated for a specific GEVER resource in the name of a specific user.
    """

    def __init__(self, url, username):
        """
        :param url: The base URL to a resource in GEVER without the view.
        :type url: string
        :param username: A GEVER username. All actions are performed in the name
          of this user.
        :type username: string
        """
        self.url = url.rstrip("/")  # Remove trailing slash(es).
        self.username = username
        self.session = GEVERSession(url, username)

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

    def listing(self, **params):
        """
        Listing of specific types for given URL (https://docs.onegovgever.ch/dev-manual/api/listings/)
        Results are casted into model objects.
        """
        # GEVER-team: why does this include elements of type 'ftw.mail.mail'?
        if "name" not in params:
            params["name"] = "documents"

        if "columns:list" in params:
            if not isinstance(params["columns:list"], list):
                raise AttributeError("A list of columns is expected.")
            params["columns:list"].append("@type")

        response = self.session().get(f"{self.url}/@listing", params=params).json()
        response["items"] = [self.wrap(item=item) for item in response["items"]]
        return response

    def paginated_listing(self, **params):
        """
        Brute implementation: refactor to contextmanager or such --> own module.
        """
        params.update({
            "search": quote(params.get("search", "")),
            "sort_on": params.get("sortBy", "title"),
            "sort_order": self._get_sort_order(descending=params.get("descending", "")),
            "b_start": self._get_batch_start(page=params.get("page"), per_page=params.get("rowsPerPage")),
            "b_size": params.get("rowsPerPage", 10),
        })
        response = self.listing(**params)
        return response

    def _get_sort_order(self, descending):
        return "descending" if descending == "true" else "ascending"

    def _get_batch_start(self, page, per_page):
        try:
            return (int(page) - 1) * int(per_page)
        except (ValueError, TypeError):
            return 0

    def update_object(self, **data):
        return self.session().patch(self.url, json=data).ok
