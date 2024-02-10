
class Quantity():
    def __init__(self, f, ncomp):
        self.f = f
        self.ncomp = ncomp

    def __call__(self, dst):
        return self.f(dst)
    
def isquantity(q):
    return callable(q) and hasattr(q, "ncomp")