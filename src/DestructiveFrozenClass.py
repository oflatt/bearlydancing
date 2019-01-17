
from DestructiveBox import DestructiveBox

# a class like FrozenClass but packages the object in a DestructiveBox
class DestructiveFrozenClass(object):
    __isfrozen = False
    
    def __new__(*args):
        # create it using new
        o = super(DestructiveFrozenClass, args[0]).__new__(args[0])
        
        # initiate the object (self is the first arg, do not include it)
        o.__init__(*args[1:])
        
        # wrap the item in a destructive box
        return DestructiveBox(o)
    
    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is from a frozen class" % self + " so new attribute " + str(key) + " cannot be set")
        
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True

