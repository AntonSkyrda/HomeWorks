class Url:
    def __init__(
        self,
        scheme: str,
        authority: str,
        path: str | list | None = None,
        query: dict | None = None,
        fragment: str | None = None,
    ):
        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment

    def __str__(self):
        base_url = f"{self.scheme}://{self.authority}"

        if self.path:
            if isinstance(self.path, str):
                base_url += f"/{self.path}"
            elif isinstance(self.path, list):
                base_url += "/" + "/".join(self.path)

        if self.query:
            query_str = "&".join(f"{key}={value}" for key, value in self.query.items())
            base_url += f"?{query_str}"

        if self.fragment:
            base_url += f"#{self.fragment}"

        return base_url

    def __eq__(self, other):
        if isinstance(other, Url):
            return (
                self.scheme == other.scheme
                and self.authority == other.authority
                and self.path == other.path
                and self.query == other.query
                and self.fragment == other.fragment
            )
        elif isinstance(other, str):
            return str(self) == other
        return NotImplemented


class HttpsUrl(Url):
    def __init__(self, authority, path=None, query=None, fragment=None):
        super().__init__("https", authority, path, query, fragment)


class HttpUrl(Url):
    def __init__(self, authority, path=None, query=None, fragment=None):
        super().__init__("http", authority, path, query, fragment)


class GoogleUrl(Url):
    def __init__(self, path=None, query=None, fragment=None):
        super().__init__("https", "google.com", path, query, fragment)


class WikiUrl(Url):
    def __init__(self, path=None, query=None, fragment=None):
        super().__init__("https", "wikipedia.org", path, query, fragment)


class UrlCreator:
    def __init__(self, scheme: str, authority: str, path=None, query=None):
        self.scheme = scheme
        self.authority = authority
        self.path = path or []
        self.query = query or {}

    def __getattr__(self, name: str):
        new_path = self.path + [name]
        return UrlCreator(self.scheme, self.authority, path=new_path, query=self.query)

    def __call__(self, *args, **kwargs):
        new_path = self.path + list(args)
        new_query = {**self.query, **kwargs}
        return UrlCreator(self.scheme, self.authority, path=new_path, query=new_query)

    def _create(self):
        return Url(
            scheme=self.scheme,
            authority=self.authority,
            path=self.path,
            query=self.query,
        )

    def __str__(self):
        return str(self._create())

    def __eq__(self, other):
        return str(self) == other if isinstance(other, (str, Url)) else NotImplemented
