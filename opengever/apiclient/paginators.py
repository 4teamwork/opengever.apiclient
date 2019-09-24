"""
There are different approaches to pagination. A backend implementation
like in RIS (`ris/gever/paginators.py`) seems unnecessary, as the frontend
is responsible to call the "next" URL provided by GEVER batching.
"""
from urllib.parse import quote

# maybe: add base class for documentation of required properties.


class VuetifyPaginator:
    """
    Querystrings as defined by Vue.
    """
    def __init__(self, params):
        self.params = params

    @property
    def search(self):
        return quote(self.params.get("search", ""))

    @property
    def sort_on(self):
        return self.params.get("sortBy", "title"),

    @property
    def sort_order(self):
        descending = self.params.get("descending", "")
        return "descending" if descending == "true" else "ascending"

    @property
    def b_start(self):
        return self._get_batch_start(
            page=self.params.get("page"),
            per_page=self.params.get("rowsPerPage")
        )

    @property
    def b_size(self):
        return self.params.get("rowsPerPage", 10)

    def _get_batch_start(self, page, per_page):
        try:
            return (int(page) - 1) * int(per_page)
        except (ValueError, TypeError):
            return 0
