from datetime import date

price = {"biscuits": 12.50, "noodles": 15}

def shopping(name, list):
    print(f"{name}")
    items = ""
    prices = ""
    count = ""
    cost = ""
    for item in list:
        items += item if not items else ", " + item
        prices += "    " + item + ': ' + str(price[item]) + '\n'
        count += "    " + item + ": " + str(list[item]) + "\n"
        cost += "    " + item + ": " + str(list[item] * price[item]) + "\n"
    print(f"  Items: {items}\n")
    print(f"  Price: \n{prices}")
    print(f"  Item Count: \n{count}")
    print(f"  Cost: \n{cost}")
    print("Date: {month} {date}, {year}".format(month=date.today().strftime("%B"), date=date.today().day, year=date.today().year))



shopping("Sagar Chalise", {"biscuits": 10, "noodles": 20})
