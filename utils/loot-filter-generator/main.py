from functions import name_changer, name_changer_replace, color_changer, item_code_fetcher, color_map, name_changer_append, name_changer_prepend, item_code_magic_fetcher

import json

# ===== Settings =====
input_file = "item-names" # "item-runes"
output_file = f"{input_file}-out"
language = "enUS"
inplace = True

# name changes
name_changes_prepend = {
    "87": "<87>",
    "elite": "<E>"
}

name_changes_append = {
    #"elite": "<E>"
}

name_changes_replace = {
    "Potion": "Pot",
    "Charm": "ÿc:Charmÿc3",
    "> <": ""
}

name_changes_fixed = {
    "hp1": "HP1", "hp2": "HP2", "hp3": "HP3", "hp4": "HP4", "hp5": "HP5",
    "mp1": "MP1", "mp2": "MP2", "mp3": "MP3", "mp4": "MP4", "mp5": "MP5",
}

# color changes
coler_changes = {
    "red": ["health-potions"],
    "blue-light": ["mana-potions"],
    "purple": ["rejuvenation-potions"],
    "pink": ["runes-midhigh", "runes-high"],
    #"green-dark": ["charms"],
    "blue-sky": ["gems"]
}

# ===== Code =====


# load item-names.json using utf-8 with bom encoding
with open(f'{input_file}.json', 'r', encoding='utf-8-sig') as f:
    my_json = json.load(f)

all_change_recipes = list()

# names prepend
for key, value in name_changes_prepend.items():
    item_codes = item_code_magic_fetcher(key)
    change_recipe = name_changer_prepend(my_json, value, item_codes, language=language, inplace=inplace)
    all_change_recipes.append(change_recipe)

# names append
for key, value in name_changes_append.items():
    item_codes = item_code_magic_fetcher(key)
    change_recipe = name_changer_append(my_json, value, item_codes, language=language, inplace=inplace)
    all_change_recipes.append(change_recipe)

# names replace
change_recipes = name_changer_replace(my_json, name_changes_replace, language=language, inplace=inplace)
all_change_recipes.append(change_recipes)

# names fixed
change_recipes = name_changer(my_json, name_changes_fixed, language=language, inplace=inplace)
all_change_recipes.append(change_recipes)

# change the colors of the items
for color, items in coler_changes.items():
    change_recipes = color_changer(my_json, items=items, color=color, language=language, inplace=inplace)

# save file
with open(f'{output_file}.json', 'w', encoding='utf-8-sig') as f:
    json.dump(my_json, f, ensure_ascii=False, indent=2)