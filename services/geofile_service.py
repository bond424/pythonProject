from fastapi import Depends

from .repository.layer_repository import Geofile_Repository


class Geofile_Services:
    def __init__(self, repository: Geofile_Repository = Depends()) -> None:
        self.repository = repository

    def get_test_layer(self):
        return self.repository.get_test_def()

    def set_DB_ShpFiles(self, files_info):
        return self.repository.set_DB_ShpFiles(files_info)

    def get_DB_ShpFiles(self, filenm):
        return self.repository.get_DB_ShpFiles(filenm)

    def get_all_DBFiles(self):
        return self.repository.get_all_DBFiles()
