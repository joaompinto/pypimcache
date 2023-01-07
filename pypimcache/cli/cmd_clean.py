from ..cache import Cache


def clean():
    """clean the current serial mark"""
    cache = Cache()
    cache.clean()
