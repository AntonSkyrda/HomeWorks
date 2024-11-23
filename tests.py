from main import (
    Url,
    HttpsUrl,
    GoogleUrl,
    WikiUrl,
    UrlCreator,
)


if __name__ == "__main__":
    assert GoogleUrl() == HttpsUrl(authority="google.com")
    assert GoogleUrl() == Url(scheme="https", authority="google.com")
    assert GoogleUrl() == "https://google.com"
    assert WikiUrl() == Url(scheme="https", authority="wikipedia.org")
    assert WikiUrl(path=["wiki", "python"]) == "https://wikipedia.org/wiki/python"
    assert (
        GoogleUrl(query={"q": "python", "result": "json"})
        == "https://google.com?q=python&result=json"
    )

    url_creator = UrlCreator(scheme="https", authority="docs.python.org")
    assert url_creator.docs.v1.api.list == "https://docs.python.org/docs/v1/api/list"
    assert url_creator("api", "v1", "list") == "https://docs.python.org/api/v1/list"
    assert (
        url_creator("api", "v1", "list", q="my_list")
        == "https://docs.python.org/api/v1/list?q=my_list"
    )
    assert (
        url_creator("3")
        .search(q="getattr", check_keywords="yes", area="default")
        ._create()
        == "https://docs.python.org/3/search?q=getattr&check_keywords=yes&area=default"
    )
