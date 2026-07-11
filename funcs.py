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
def add_rule_in_list(a,b):
    new_roles=""
    rules=a.split("|")
    match re.search(". ",rules[-1]):
        case None:
            k=1
            for i in rules[:-1]:
                if re.search(". ",i)==None:
                    new_roles+=i+"|"
                else:
                    new_roles+=i+"|"
                    k+=1
            new_roles+=f"{k}. {b}|{rules[-1]}"
        case _:
            k=1
            for i in rules:
                if re.search(". ",i)==None:
                    pass
                else:
                    k+=1
            new_roles=a+"|"+f"{k}. {b}"
    return new_roles
def remove_rule_in_list(a,b):
    new_roles=""
    rules=a.split("|")
    k=0
    for i in rules:
        match re.search(f"{b}. ",i):
            case None:
                pass
                k+=1
            case _:
                rules[k]=""
    k=0
    for j in rules:
        match re.search(". ",j):
            case None:
                if len(j)==0:
                    pass
                else:
                    new_roles+=j+"|"
            case _:
                if int(j[0])-k==1:
                    k=int(j[0])
                    new_roles+=j+"|"
                else:
                    k=int(j[0])-1
                    new_roles+=f"{k}{j[1::]}"+"|"
    return new_roles