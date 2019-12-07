def askUser(path):
    file = open(path, encoding='utf8')
    txt = file.read()
    print(txt)
    res = input()
    if res.isdigit():
        return int(res)
    else: return res.lower()
