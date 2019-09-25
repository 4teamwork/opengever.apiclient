from .models import ModelRegistry
from .paginators import VuetifyPaginator
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

    def listing(self, name="documents", *columns):
        """
        Listing of specific types for given URL (https://docs.onegovgever.ch/dev-manual/api/listings/)
        Results are casted into model objects.
        """
        # GEVER-team: why does this include elements of type 'ftw.mail.mail'?
        params = dict(name=name)
        # Always require the type so the element may be wrapped.
        params["columns:list"] = ["@type"]
        params["columns:list"].extend(*columns)

        response = self.session().get(f"{self.url}/@listing", params=params).json()
        response["items"] = [self.wrap(item=item) for item in response["items"]]
        return response

    def paginated_listing(self, **params):
        """
        Brute implementation: refactor to contextmanager or such --> own module.
        """
        # maybe: allow configuration of paginators. not required yet.
        paginator = VuetifyPaginator(params=params)
        params.update({
            "search": paginator.search,
            "sort_on": paginator.sort_on,
            "sort_order": paginator.sort_order,
            "b_start": paginator.b_start,
            "b_size": paginator.b_size,
        })
        response = self.listing(**params)
        return response

    def update_object(self, **data):
        return self.session().patch(self.url, json=data).ok
