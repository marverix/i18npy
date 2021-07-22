from typing import Union, List, Tuple


def apply_numbers(text: str, num: int) -> str:
    return text.replace("-%n", str(-num)).replace("%n", str(num))


def apply_formatting(text: str, num: Union[int, None], formatting: Union[dict, None]) -> str:
    if isinstance(num, int):
        text = apply_numbers(text, num)
    if formatting:
        for k, v in formatting.items():
            text = text.replace("%{" + k + "}", v)
    return text


def does_index_exist(arr: Union[List, Tuple], index: int) -> bool:
    return len(arr) > index
