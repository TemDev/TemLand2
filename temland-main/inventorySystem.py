from ast import Try


class ItemStack:
    maxNum = 20  # maximum stacking number

    def __init__(self, name, num) -> None:
        self.name = name
        self.num = num  # actual number of the item "stack"


class Weapon(ItemStack):
    maxNum = 1

    def __init__(self, name, level) -> None:
        self.endurance = 5 * level
        self.ifBroken = False
        self.num = 1
        self.name = name
        self.level = level

    def useWeapon(self):
        if not self.ifBroken:  # can only use weapons that are not broken
            print(self.name, self.endurance)
            self.endurance -= 1
            self.ifBroken = True if self.endurance == 0 else False  # weapon is broken
        else:
            print("Broken")


class Inventory:

    def __init__(self):
        self.backpack = [None for _ in range(10)]  # A backpack with 10 space
        print(self.backpack)

    def addItem(self, item: ItemStack):
        for i in range(len(self.backpack)):
            try:
                # if the item existed in backpack and is not fully stacked
                if item.name == self.backpack[i].name and self.backpack[i].num < self.backpack[i].maxNum:

                    # total num of the item does not exceed 20
                    if self.backpack[i].num + item.num <= 20:
                        self.backpack[i].num += item.num
                        del item
                    # need extra space to store remaining item
                    else:
                        tmpNum = self.backpack[i].num
                        self.backpack[i].num = 20
                        self.addItem(ItemStack(item.name, (item.num + tmpNum) - 20))
                        print("please neglect the next line")
                        del item
                    break
            except AttributeError:
                pass
        # if there is not any same item
        else:
            for i in range(len(self.backpack)):
                if self.backpack[i] == None:
                    self.backpack[i] = item
                    del item
                    break
        self.printBackpack()

    def printBackpack(self):
        # output backpack state; for debugging
        lst2 = []
        for j in self.backpack:
            try:
                lst2.append(j.name + " " + str(j.num))
            except AttributeError:
                lst2.append("None")
        print(lst2)

    # delete item requires the index of the item in backpack
    def deleteItem(self, index):
        if index < len(self.backpack):
            if self.backpack[index] is not None:
                dropItem = ItemStack(self.backpack[index].name, self.backpack[index].num)
                self.backpack[index] = None
                print(dropItem.name, dropItem.num)
        self.printBackpack()


if __name__ == "__main__":
    pass
