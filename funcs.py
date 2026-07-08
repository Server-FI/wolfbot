import re
def check_items(items):
    orig_items=""
    for i in items.split(","):
        check=i.split(":")
        match re.search(check[0],orig_items):
            case None:
                orig_items+=f"{check[0]}:{check[1]},"
            case _:
                pass
    return orig_items