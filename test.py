index = int(input("Enter index: "))

shop = [
                {"name": "Watch", "price": 1000, "description": "Time"},
                {"name": "Laptop", "price": 5000, "description": "Work"},
                {"name": "PC", "price": 10000, "description": "Gaming"}
            ]

def find_index(index):
    for i, val in enumerate(shop, 1):
        if index == i:
            name = val["name"]
            price = val["price"]
            desc = val["description"]

            print(name)
            print(price)
            print(desc)


find_index(index=index)
