import copy

# a wrapper around any object that makes setting attributes destroy the box and return a new box
class DestructiveBox(object):

    def __init__(self, item):
        
        super(DestructiveBox, self).__setattr__("item",item)
        

    
    def __setattr__(self, key, value):
        
        # set the attribute in the item
        i = object.__getattribute__(self, "item")
        
        i.__setattr__(key, value)
        
        # make a new box
        b = DestructiveBox(i)
        
        # destroy this box by setting the item to None
        super(DestructiveBox, self).__setattr__("item",None)

        # return new box
        return b
    
    def destructiveset(self, key, value):
        return self.__setattr__(key, value)

    # accessing accesses fields in the item
    def __getattr__(self, key):
        attr = object.__getattribute__(object.__getattribute__(self, "item"), key)

        # make functions take destructivebox as self
        if callable(attr):
            def hooked(*args, **kwargs):
                #check if it is a bound method
                if hasattr(attr, '__func__'):
                    # pass in self instead
                    return attr.__func__(self, *args, **kwargs)
                else:
                    return attr(*args, **kwargs)
            return hooked
        else:
            return object.__getattribute__(object.__getattribute__(self, "item"), key)

    # override copy to copy the item as well
    def __copy__(self):
        old = object.__getattribute__(self, "item")
        # don't call DestructiveFrozenClass' new, otherwise a new box is created
        newitem = object.__new__(old.__class__)
        newitem.__dict__.update(old.__dict__)
        return DestructiveBox(newitem)

    # override copy to copy the item as well
    def __deepcopy__(self, memo = {}):
        old = object.__getattribute__(self, "item")
        # don't call DestructiveFrozenClass' new, otherwise a new box is created
        newitem = object.__new__(old.__class__)
        newitem.__dict__.update(old.__dict__)
        d = newitem.__dict__
        for k in d:
            d[k] = copy.deepcopy(d[k])
        return DestructiveBox(newitem)
