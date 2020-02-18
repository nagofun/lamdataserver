import hashlib

def md5(srclist):
    m2 = hashlib.md5()
    map(m2.update,srclist)
    return m2.hexdigest()