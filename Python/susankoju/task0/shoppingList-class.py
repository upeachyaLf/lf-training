from datetime import date


price = {'biscuits': 12.50, 'noodles': 15}

class ShoppingItems:
    def __init__(self, name, items):
        self.items = items
        self.name = name
        self.date = date.today()

    def showAll(self):
        print(f"{(self.name)}\n")
        items = ""
        prices = ""
        count = ""
        cost = ""
        for item in self.items:
            items += item if not items else ", " + item
            prices += "    " + item + ': ' + str(price[item]) + '\n'
            count += "    " + item + ": " + str(self.items[item]) + "\n"
            cost += "    " + item + ": " + str(self.items[item] * price[item]) + "\n"
        print(f"  Items: {items}\n")
        print(f"  Price: \n{prices}")
        print(f"  Item Count: \n{count}")
        print(f"  Cost: \n{cost}")
        print("Date: {month} {date}, {year}".format(month=self.date.strftime("%B"), date=self.date.day, year=self.date.year))


myShoppingItems = ShoppingItems("Sagar Chalise", {"biscuits": 10, "noodles": 20})

myShoppingItems.showAll()
