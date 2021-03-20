from typing import List

from pydantic import BaseModel


class Workflow(BaseModel):
    name: str


class Workflows(BaseModel):
    workflows: List[Workflow] = []
