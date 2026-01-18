def read_json(filename):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents