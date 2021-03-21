import ast
from typing import Optional

from pydantic import BaseModel


class YamlParams(BaseModel):
    """
    Optional params to pass into your yamls.

    Format: key=value<space>key2=value2<space>key3=value3<space>...
    """

    params: Optional[str]

    def as_dict(self) -> dict:
        """
        Return an empty dict if we don't have params or pairs.

        If we have a pair (a=b), return a dict of the pairs {$a: b ...}
        for each (a=b) if b is not None
        """
        if not self.params:
            return {}
        pairs = self.params.split()
        if not pairs:
            return {}
        return {
            f"${pair.split('=')[0]}": pair.split("=")[1]
            for pair in pairs
            if pair.split("=")[1] is not None
        }

    def update_data_with_values(self, data: str) -> dict:
        """
        Given a string of data, replace env variables, notated as $NAME
        in the string with our params.
        """
        for k, v in self.as_dict().items():
            data = data.replace(k, v)
        return ast.literal_eval(data)
