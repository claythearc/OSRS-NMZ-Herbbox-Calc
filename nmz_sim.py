from dataclasses import dataclass
import requests as re
import json
import numpy

# constants
vial_of_water = 3
itemID = json.load(open("itemID.json", 'r'))
num_simulations = 100
boxes_per_day = 15
osrs_api = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='
end_xp = 13034431

# globals
total_cost = 0
start_xp = 11544
temp_xp = 11544


@dataclass
class HerbBox:
    def __init__(self, chance: float, cleaning_exp: float, potion_exp: float, secondary: str, potion: str):
        self.chance = chance
        self.cleaning_exp = cleaning_exp
        self.potion_exp = potion_exp
        self.secondary = secondary
        self.potion = potion
        self.potion_price = int(self.secondarycost(self.potion))
        self.secondary_cost = self.secondarycost(self.secondary)

    def secondarycost(self, item: str):
        content = re.get(osrs_api + str(self.findid(item))).json()
        price = content['item']['current']['price']
        price = str(price).replace(',', '')
        if 'k' in price:
            return int(float(price[:-1]) * 1000)
        return int(price)

    def findid(self, name: str):
        name = name.strip()
        try:
            temp = [obj for obj in itemID if obj['name'].lower() == name.lower()]
        except:
            print(name)
            exit()
        return temp[0]['id']

    def add_herb(self, name: str):
        self.herb = name
        self.herb_price = int(self.secondarycost(self.herb))

    def __str__(self):
        return f"""The selected Herb {self.herb} uses {self.secondary} to create {self.potion}"""


herbs = {
    "Guam leaf": HerbBox(25.5, 2.5, 25, "Eye of Newt", "Attack potion(3)"),
    "Marrentill": HerbBox(18.5, 3.8, 37.5, "Unicorn horn dust", "Antipoison(3)"),
    "Tarromin": HerbBox(13.5, 5, 50, "Ashes", "Serum 207 (3)"),
    "Harralander": HerbBox(11.5, 6.3, 84, "Goat Horn Dust", "combat potion(3)"),
    "Ranarr Weed": HerbBox(8.5, 7.5, 87.5, "Snape Grass", "Prayer potion(3)"),
    "Irit Leaf": HerbBox(6, 8.8, 100, "Eye of newt", "Super attack(3)"),
    "Avantoe": HerbBox(4.5, 10, 117.5, "Mort myre fungus", "super energy(3)"),
    "Kwuarm": HerbBox(4.5, 11.3, 125, "Limpwurt root", "Super strength(3)"),
    "Cadantine": HerbBox(3, 12.5, 150, "white berries", 'super defence(3)'),
    "Lantadyme": HerbBox(2.5, 13.1, 172.5, 'potato cactus', 'magic potion(3)'),
    'Dwarf Weed': HerbBox(2, 13.8, 162.5, 'Wine of zamorak', 'ranging potion(3)')
}

for k, v in herbs.items():
    try:
        v.add_herb(k)
    except:
        print(k)
        exit()

results = []
for sim in range(num_simulations):
    boxes = 0
    temp_xp = start_xp
    total_cost = 0
    while temp_xp <= end_xp:
        boxes += 1
        box = numpy.random.choice(a=list(herbs), size=10, replace=True, p=[x.chance/100 for x in herbs.values()])
        for herb in box:
            temp_xp += herbs[herb].potion_exp + herbs[herb].cleaning_exp
            total_cost += herbs[herb].potion_price - herbs[herb].secondary_cost + vial_of_water
    results.append((boxes, total_cost))


temp_box = 0
temp_cost = 0
for x, y in results:
    temp_box += x
    temp_cost += y

temp_cost = temp_cost / num_simulations
temp_box = temp_box / num_simulations

print(f"After averaging {num_simulations:,} attempts it will take {temp_box:,} boxes over {int(temp_box / boxes_per_day):,}"
      f"days at a cost of {int(temp_cost):,}")




