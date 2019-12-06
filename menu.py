def askUser(path):
    file = open(path, encoding='utf8')
    txt = file.read()
    print(txt)
    return input()
