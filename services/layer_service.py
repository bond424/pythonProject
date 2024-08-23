from fastapi import Depends

from .repository.layer_repository import Layer_Repository


class Layer_Services:
    def __init__(self, repository: Layer_Repository = Depends()) -> None:
        self.repository = repository

    def get_test_layer(self):
        get_list = []
        for i in self.repository.get_test_layer():
            get_list.append(i)
        return get_list
