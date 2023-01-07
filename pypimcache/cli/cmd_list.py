from typing import Optional

import typer

from ..cache import Cache


def list(match_name: Optional[str] = typer.Argument(None)):
    """List all packages in index"""
    cache = Cache()
    for project in cache.project_list:
        if match_name and match_name not in project["name"]:
            continue
        print(project["name"])
