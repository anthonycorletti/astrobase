from typing import Dict


def str_to_dict(
    input_str: str, input_sep: str = ",", pair_sep: str = "="
) -> Dict[str, str]:
    result = {}
    print(input_str)
    for pair in input_str.split(input_sep):
        print(pair)
        k, v = pair.split(pair_sep)
        result[k] = v
    return result
