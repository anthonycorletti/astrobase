from enum import Enum, unique


@unique
class ProviderName(str, Enum):
    gcp = "gcp"
    aws = "aws"
    azure = "azure"
