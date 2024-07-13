import json
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor


def load_entities(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def is_unique_combination(entities, attributes):
    seen = set()
    for entity in entities:
        identifier = tuple(entity.get(attr, None) for attr in attributes)
        if identifier in seen:
            return False
        seen.add(identifier)
    return True


def calculate_information_gain(entities, attribute):
    unique_values = set(entity.get(attribute, None) for entity in entities)
    return len(unique_values)


def check_combination(entities, combination):
    return combination if is_unique_combination(entities, combination) else None


def find_minimal_unique_combination(entities):
    if not entities:
        return []

    attributes = list(entities[0].keys())

    # Calculate information gain for each attribute
    info_gain = {attr: calculate_information_gain(entities, attr) for attr in attributes}

    # Sort attributes by their information gain
    sorted_attributes = sorted(attributes, key=lambda x: info_gain[x], reverse=True)

    for r in range(1, len(sorted_attributes) + 1):
        combinations_list = list(combinations(sorted_attributes, r))
        with ThreadPoolExecutor() as executor:
            results = executor.map(lambda combo: check_combination(entities, combo), combinations_list)
            minimal_combination = next((result for result in results if result is not None), None)
            if minimal_combination:
                return list(minimal_combination)

    return []


if __name__ == "__main__":
    entities = load_entities("test/json_data/income.json")
    minimal_combination = find_minimal_unique_combination(entities)
    print("Minimal unique combination of attributes:", minimal_combination)
