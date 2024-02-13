import pandas as pd

def name_changer_append(d2json, append_string, item_codes, language: str = "enUS", sep=" ", inplace=False):
    return _name_changer_pender(d2json, append_string, item_codes, language, append=True, sep=sep, inplace=inplace)

def name_changer_prepend(d2json, preprend_string, item_codes, language: str = "enUS", sep=" ", inplace=False):
    return _name_changer_pender(d2json, preprend_string, item_codes, language, append=False, sep=sep, inplace=inplace)

def _name_changer_pender(d2json, string, item_codes, language: str = "enUS", append=False, sep=" ", inplace=False):

    item_codes = list(dict.fromkeys(item_codes))
    change_recipes = list()
    for i, d in enumerate(d2json):
        if d.get("Key") in item_codes:
            item_name = d.get(language)
            if item_name is None:
                raise ValueError(f"Something went wrong for {d.get('Key')}")
            item_name_new = f"{string}{sep}{item_name}" if append else f"{item_name}{sep}{string}"
            print(f"Changing the name of {item_name} to {item_name_new}")
            if inplace:
                d[language] = item_name_new
            change_recipes.append((i, language, item_name_new))

    return change_recipes
def name_changer_replace(d2json, replace_dict, language: str = "enUS", inplace=False):
    change_recipes = list()
    for pattern, replace in replace_dict.items():
        change_recipe = _name_changer_replace(d2json, pattern, replace, language, inplace=inplace)
        if change_recipe is not None:
            change_recipes.extend(change_recipe)
    return change_recipes

def _name_changer_replace(d2json, pattern: str, replace: str, language: str = "enUS", inplace=False):
    change_recipes = list()
    for i, d in enumerate(d2json):
        if d.get(language) is not None:
            if pattern in d.get(language):
                old_name = d.get(language)
                new_name = old_name.replace(pattern, replace)
                print(f"Changing the name of {old_name} to {new_name}")
                if inplace:
                    d[language] = d.get(language).replace(pattern, replace)
                change_recipes.append((i, language, new_name))
    return change_recipes

def name_changer(d2json, name_dict: dict, language: str = "enUS", inplace=False):
    change_recipes = list()
    for key, name in name_dict.items():
        for i, d in enumerate(d2json):
            if d.get("Key") == key:
                print(f"Changing the name of {key} to {name}")
                if inplace:
                    d[language] = name
                change_recipes.append((i, language, name))
                break
    return change_recipes

def color_changer(d2json, items: str, color: str = "white", language: str = "enUS", inplace=False):

    # build list of item to changs
    items_to_change = list()
    change_recipes = list()

    for item in items:
        items_to_change.extend(item_code_magic_fetcher(item))

    items_to_change = list(dict.fromkeys(items_to_change))

    print(f"items to change: {items_to_change}")

    # change the color of the items
    for item_key in items_to_change:
        change_recipe = _change_item_color(d2json, item_key, color, language, inplace=inplace)
        if change_recipe is not None:
            change_recipes.append(change_recipe)

    #print(f"change recipes: {json.dumps(change_recipes, indent=2)}")
    #print(f"type of change recipes: {type(change_recipes[0])}")

    return change_recipes

def _change_item_color(d2json, item_key, color, language, inplace=False):
    #print(f"Looking for {item_key}")
    color_code = color_map.get(color)
    if color_code is None:
        raise ValueError(f"Invalid color: {color}")
    for i, d in enumerate(d2json):
        if d.get("Key") == item_key:
            item_name = d.get(language)
            if item_name is None:
                raise ValueError(f"Item not found: {item_key}")
            print(f"Changing the color of {item_name} to {color} ({color_code})")
            new_value = f"{color_code}{item_name}"
            if inplace:
                d[language] = new_value
            return (i, language, new_value)

    print(f"No matches found for {item_key}")
    return None


default_colors = {
    "normal": "white",
    "ethereal": "grey",
    "magic": "blue",
    "rare": "yellow-rich",
    "set": "green-light",
    "unique": "gold-rich",
    "crafted": "orange",
    "runes": "orange",
    "gold": "white",
    "tempered": "green-dark",
    "potions": "white"
}

color_map = {
    "black": "ÿc6",
    "blue": "ÿc3",
    "blue-light": "ÿcN",
    "blue-sky": "ÿcT",
    "gold": "ÿc7",
    "gold-rich": "ÿc4",
    "gold-light": "ÿcM",
    "green": "ÿc<",
    "green-bright": "ÿcQ",
    "green-dark": "ÿc:",
    "green-light": "ÿc2",
    "grey": "ÿc5",
    "orange": "ÿc8",
    "pink": "ÿcO",
    "purple": "ÿc;",
    "red": "ÿc1",
    "red-dark": "ÿcS",
    "red-rich": "ÿcU",
    "violet-pale": "ÿcP",
    "white": "ÿc0",
    "yellow": "ÿcR",
    "yellow-rich": "ÿc9",
    "blue-dark": "ÿcF",
    "blue-teal": "ÿcD",
    "purple-dark": "ÿcG",
    "red-ruby": "ÿcE",
}

# note: these colors might not work.
color_map_extra = {
    "blue-dark": "ÿcF",
    "blue-teal": "ÿcD",
    "purple-dark": "ÿcG",
    "red-ruby": "ÿcE",
}


# mapping of group names to key (id).
item_groups = {
    "health-potions": ["hp1", "hp2", "hp3", "hp4", "hp5"],
    "mana-potions": ["mp1", "mp2", "mp3", "mp4", "mp5"],
    "rejuvenation-potions": ["rvs", "rvl"],
    "charms": ["cm1", "cm2", "cm3"],
    "jewel": ["jew"],
    "runes-low": ["r01", "r02", "r03", "r04", "r05", "r06"],
    "runes-midlow": ["r07", "r08", "r09", "r10", "r11", "r12", "r13", "r14"],
    "runes-mid": ["r15", "r16", "r17", "r18", "r19"],
    "runes-midhigh": ["r20", "r21", "r22", "r23", "r24", "r25"],
    "runes-high": ["r26", "r27", "r28", "r29", "r30", "r31", "r32", "r33"],
}

def item_code_fetcher(group: list[str] = None,
                      name: list[str] = None,
                      item_type: list[str] = None,
                      subtype: list[str] = None,
                      difficulty: list[str] = None,
                      treasure_class: list[str] = None,
                      return_first=False
                      ):

    df = pd.read_csv("item-codes.csv", sep=";", dtype=str)

    item_codes = list()
    if isinstance(group, list):
        for g in group:
            codes_from_groups = item_groups.get(g)
            if codes_from_groups is not None:
                if return_first:
                    return codes_from_groups
                else:
                    item_codes.extend(codes_from_groups)

    if isinstance(treasure_class, list):
        for tc in treasure_class:
            codes_from_tc = df[df["treasure-class"] == tc]["code"].to_list()
            if len(codes_from_tc) > 0:
                if return_first:
                    return codes_from_tc
                else:
                    item_codes.extend(codes_from_tc)

    if isinstance(subtype, list):
        for st in subtype:
            codes_from_subtypes = df[df["sub-type"] == st]["code"].to_list()
            if len(codes_from_subtypes) > 0:
                if return_first:
                    return codes_from_subtypes
                else:
                    item_codes.extend(codes_from_subtypes)

    if isinstance(item_type, list):
        for t in item_type:
            codes_from_types = df[df["type"] == t]["code"].to_list()
            if len(codes_from_types) > 0:
                if return_first:
                    return codes_from_types
                else:
                    item_codes.extend(codes_from_types)

    if isinstance(difficulty, list):
        for d in difficulty:
            codes_from_difficulty = df[df["difficulty"] == d]["code"].to_list()
            if len(codes_from_difficulty) > 0:
                if return_first:
                    return codes_from_difficulty
                else:
                    item_codes.extend(codes_from_difficulty)

    if isinstance(name, list):
        for n in name:
            codes_from_names = df[df["name"] == n]["code"].to_list()
            if len(codes_from_names) > 0:
                if return_first:
                    return codes_from_names
                else:
                    item_codes.extend(codes_from_names)

    item_codes = list(dict.fromkeys(item_codes))
    return item_codes


def item_code_magic_fetcher(string):
    print(f"looking for items codes to fetch using magic: {string}")
    item_codes = item_code_fetcher(
        group=[string],
        name=[string],
        item_type=[string],
        subtype=[string],
        difficulty=[string],
        treasure_class=[string],
        return_first=True
    )
    print(f"item codes found: {item_codes}")
    if item_codes is not None:
        if len(item_codes) > 0:
            return item_codes
    return [string]

