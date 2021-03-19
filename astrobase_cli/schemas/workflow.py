from typing import List

from pydantic import BaseModel


class Workflow(BaseModel):  # TODO!
    name: str


class Workflows(BaseModel):
    workflows: List[Workflow] = []
