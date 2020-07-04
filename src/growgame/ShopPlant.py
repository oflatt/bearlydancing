from DestructiveFrozenClass import DestructiveFrozenClass

class ShopPlant(DestructiveFrozenClass):

    def __init__(self, name, headnode, cost):
        self.name = name
        self.headnode = headnode
        self.cost = cost
        self._freeze()
