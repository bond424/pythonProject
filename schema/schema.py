from pydantic import BaseModel
from typing import List

class SigutableModel(BaseModel):
    id_0: int
    geom: bytes