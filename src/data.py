import copy


INITIAL_RECIPES = [
    {
        "id": 1,
        "name": "Pasta",
        "ingredients": ["Dry pasta", "Tomato sauce", "Salt"],
        "instructions": "Boil the pasta, drain it, then add tomato sauce and salt.",
        "created_by": "Tia",
        "creation_date": "2026-09-14",
        "rate": 5,
    },
    {
        "id": 2,
        "name": "Grilled Cheese",
        "ingredients": ["Bread", "Cheese", "Butter"],
        "instructions": "Butter the bread, add cheese, and grill until golden.",
        "created_by": "Alex",
        "creation_date": "2026-09-13",
        "rate": 4,
    },
    {
        "id": 3,
        "name": "Caesar Salad",
        "ingredients": ["Romaine lettuce", "Parmesan", "Croutons", "Caesar dressing"],
        "instructions": "Toss lettuce with dressing, top with parmesan and croutons.",
        "created_by": "Sam",
        "creation_date": "2026-09-12",
        "rate": 4,
    },
    {
        "id": 4,
        "name": "Pancakes",
        "ingredients": ["Flour", "Milk", "Eggs", "Sugar", "Baking powder"],
        "instructions": "Whisk the batter, then cook on a hot skillet until bubbles form.",
        "created_by": "Jordan",
        "creation_date": "2026-09-11",
        "rate": 5,
    },
    {
        "id": 5,
        "name": "Tomato Soup",
        "ingredients": ["Tomatoes", "Onion", "Garlic", "Cream", "Salt"],
        "instructions": "Simmer tomatoes with onion and garlic, blend, then stir in cream.",
        "created_by": "Riley",
        "creation_date": "2026-09-10",
        "rate": 4,
    },
]

recipes = copy.deepcopy(INITIAL_RECIPES)
