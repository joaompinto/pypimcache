import json
import os
import shutil
import time
from pathlib import Path

from platformdirs import user_cache_dir

appname = "pypimcache"
appauthor = "joaompinto"


class Cache:
    def __init__(self):
        cache_dir = self.cache_dir = Path(user_cache_dir(appname, appauthor))
        if not Path(cache_dir).exists():
            os.makedirs(cache_dir)
        last_fname = Path(cache_dir).joinpath("last_download")
        try:
            with open(last_fname) as last_file:
                data = json.load(last_file)
                if data:
                    last_download_time = float(data)
        except FileNotFoundError:
            last_download_time = 0
        self.last_download_time = last_download_time
        self.last_serial_fname = Path(self.cache_dir).joinpath("last_serial")

    def is_older_than(self, age: int) -> bool:
        current = time.time()
        return current - self.last_download_time > age

    @property
    def last_serial(self) -> int:
        try:
            with open(self.last_serial_fname) as last_serial_file:
                last_serial_txt = last_serial_file.read()
        except FileNotFoundError:
            return 0
        try:
            last_serial_int = int(last_serial_txt)
        except ValueError:
            return 0
        return last_serial_int

    @property
    def last_serial_path(self) -> str:
        last_serial = self.last_serial
        return Path(self.cache_dir).joinpath(f"{last_serial}.json")

    @property
    def serial_list(self) -> list:
        all_serials = [x.stem for x in Path(self.cache_dir).glob("*.json")]
        all_serials.remove("index")
        return all_serials

    @property
    def project_list(self) -> list:
        try:
            with open(self.last_serial_path) as index_file:
                data = json.load(index_file)
        except FileNotFoundError:
            return []
        return data["projects"]

    def update(self, data: dict) -> None:
        last_serial = str(data["meta"]["_last-serial"])
        tmp_index_path = Path(self.cache_dir).joinpath("index.json.tmp")
        with open(tmp_index_path, "w") as index_file:
            index_file.write(json.dumps(data, indent=4))
        final_path = Path(self.cache_dir).joinpath("index.json")
        if final_path.exists():
            os.unlink(final_path)
        os.rename(tmp_index_path, final_path)

        with open(self.last_serial_fname, "w") as last_serial_file:
            last_serial_file.write(last_serial)

    def clean(self) -> None:
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        print("Cache cleared")
