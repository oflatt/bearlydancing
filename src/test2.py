from DestructiveBox import DestructiveBox

class GreenBean():

    def __init__(self, pizza):
        self.pizza = pizza

b = DestructiveBox(GreenBean("yellow"))
print(b.pizza)
a = b.set("pizza", "green")

print(a.pizza)

