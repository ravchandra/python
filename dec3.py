def decbold(f):
    def wrapper():
        return "<b>" + f() + "</b>"
    return wrapper

def decitalic(f):
    def wrapper():
        return "<i>" + f() + "</i>"
    return wrapper
def decunderline(f):
    def wrapper():
        return "<u>" + f() + "</u>"
    return wrapper

@decbold
@decitalic
@decunderline
def fun():
    return "text to be decorated"

print fun()
