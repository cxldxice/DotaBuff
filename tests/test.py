num = ["100", "1.0k", "1.7k"]


def to_int(string: str):
    string = string.replace(" ", "")
    try:
        return int(string)
    except:
        pass
    
    string = string.replace("k", "").replace(".", "")
    string += "00"

    try:
        return int(string)
    except:
        return None


for n in num:
    print(to_int(n))