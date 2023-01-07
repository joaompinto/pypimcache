import httpx

from ..cache import Cache

# from pypi_simple import ACCEPT_JSON_ONLY, PyPISimple


PYPI_SIMPLE_INDEX_URL = "https://pypi.org/simple/"
# "curl -H "Accept: application/vnd.pypi.simple.v1+json" https://pypi.org/simple/"

# https://peps.python.org/pep-0691/


def update():
    """update the cache from the current pypi index"""
    cache = Cache()
    PYPI_SIMPLE_INDEX_URL = "https://pypi.org/simple/"
    headers = {"Accept": "application/vnd.pypi.simple.v1+json"}
    with httpx.Client(headers=headers) as client:
        print(f"Checking x-pypi-last-serial from {PYPI_SIMPLE_INDEX_URL}")
        response = client.head(PYPI_SIMPLE_INDEX_URL)
        index_last_serial = int(response.headers["x-pypi-last-serial"])
        print(
            f"Got serial {index_last_serial}, last cached serial is {cache.last_serial}"
        )
        if cache.last_serial != index_last_serial:
            print("Downloading new package index")
            response = client.get(PYPI_SIMPLE_INDEX_URL)
            response.raise_for_status()
            data = response.json()
            cache.update(data)
            project_count = len(data["projects"])
            print(f"Saved index containing {project_count} projects")
        else:
            print("Nothing to update")
