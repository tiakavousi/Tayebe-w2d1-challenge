import copy

import pytest

from src import data, routes


@pytest.fixture(autouse=True)
def reset_recipes():
    data.recipes[:] = copy.deepcopy(data.INITIAL_RECIPES)


VALID_PAYLOAD = {
    "name": "Test Recipe",
    "ingredients": ["Flour", "Water", "Salt"],
    "instructions": "Mix and bake.",
    "created_by": "Tester",
    "rate": 4,
}

UPDATE_PAYLOAD = {
    "name": "Tomato Pasta",
    "ingredients": ["Pasta", "Tomato sauce", "Garlic", "Salt"],
    "instructions": "Boil the pasta, prepare the sauce, then combine them.",
    "created_by": "Tia",
    "rate": 5,
}

REQUIRED_FIELDS = {
    "id",
    "name",
    "ingredients",
    "instructions",
    "created_by",
    "creation_date",
    "rate",
}

INVALID_PAYLOADS = [
    {},
    {"name": "only name"},
    {**VALID_PAYLOAD, "ingredients": "should be a list"},
    {**VALID_PAYLOAD, "rate": "five"},
]


# get_recipe

def test_get_recipe_returns_existing():
    status, body = routes.get_recipe(1)
    assert status == 200
    assert body["id"] == 1
    assert REQUIRED_FIELDS.issubset(body)


def test_get_recipe_returns_404_when_missing():
    status, body = routes.get_recipe(9999)
    assert status == 404
    assert body is None


# get_all_recipes

def test_get_all_recipes_returns_five_initially():
    status, body = routes.get_all_recipes()
    assert status == 200
    assert isinstance(body, list)
    assert len(body) == 5


def test_get_all_recipes_have_required_fields_and_unique_ids():
    _, body = routes.get_all_recipes()
    ids = [r["id"] for r in body]
    assert len(set(ids)) == len(ids)
    for recipe in body:
        assert REQUIRED_FIELDS.issubset(recipe)


# create_recipe

def test_create_recipe_returns_201_with_full_body():
    status, body = routes.create_recipe(VALID_PAYLOAD)
    assert status == 201
    for field in ("name", "ingredients", "instructions", "created_by", "rate"):
        assert body[field] == VALID_PAYLOAD[field]


def test_create_recipe_generates_id_and_creation_date():
    _, body = routes.create_recipe(VALID_PAYLOAD)
    assert isinstance(body["id"], int)
    assert body["id"] not in {1, 2, 3, 4, 5}
    assert isinstance(body["creation_date"], str)
    assert body["creation_date"]


def test_create_recipe_ignores_client_supplied_id():
    _, body = routes.create_recipe({**VALID_PAYLOAD, "id": 999})
    assert body["id"] != 999


def test_create_recipe_appends_and_is_retrievable():
    before = len(routes.get_all_recipes()[1])
    _, created = routes.create_recipe(VALID_PAYLOAD)
    _, after = routes.get_all_recipes()
    assert len(after) == before + 1
    status, fetched = routes.get_recipe(created["id"])
    assert status == 200
    assert fetched["name"] == VALID_PAYLOAD["name"]


@pytest.mark.parametrize("payload", INVALID_PAYLOADS)
def test_create_recipe_rejects_invalid(payload):
    status, body = routes.create_recipe(payload)
    assert status == 400
    assert body is None


# update_recipe

def test_update_recipe_returns_200_and_preserves_id():
    status, body = routes.update_recipe(1, UPDATE_PAYLOAD)
    assert status == 200
    assert body["id"] == 1
    for field in ("name", "ingredients", "instructions", "created_by", "rate"):
        assert body[field] == UPDATE_PAYLOAD[field]


def test_update_recipe_persists_changes():
    routes.update_recipe(1, UPDATE_PAYLOAD)
    _, fetched = routes.get_recipe(1)
    assert fetched["name"] == UPDATE_PAYLOAD["name"]
    assert fetched["ingredients"] == UPDATE_PAYLOAD["ingredients"]


def test_update_recipe_does_not_change_count():
    before = len(routes.get_all_recipes()[1])
    routes.update_recipe(1, UPDATE_PAYLOAD)
    after = len(routes.get_all_recipes()[1])
    assert after == before


def test_update_recipe_returns_404_for_missing_id():
    status, body = routes.update_recipe(9999, UPDATE_PAYLOAD)
    assert status == 404
    assert body is None


@pytest.mark.parametrize("payload", INVALID_PAYLOADS)
def test_update_recipe_rejects_invalid(payload):
    status, body = routes.update_recipe(1, payload)
    assert status == 400
    assert body is None


# remove_recipe

def test_remove_recipe_returns_204_and_removes_from_list():
    status, body = routes.remove_recipe(1)
    assert status == 204
    assert body is None
    fetch_status, _ = routes.get_recipe(1)
    assert fetch_status == 404


def test_remove_recipe_shrinks_list_and_leaves_others():
    routes.remove_recipe(1)
    _, remaining = routes.get_all_recipes()
    assert len(remaining) == 4
    remaining_ids = {r["id"] for r in remaining}
    assert 1 not in remaining_ids
    assert remaining_ids == {2, 3, 4, 5}


def test_remove_recipe_returns_404_for_missing_id():
    status, body = routes.remove_recipe(9999)
    assert status == 404
    assert body is None


def test_remove_recipe_second_delete_returns_404():
    routes.remove_recipe(1)
    status, _ = routes.remove_recipe(1)
    assert status == 404
