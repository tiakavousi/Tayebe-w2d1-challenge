import datetime

from pydantic import BaseModel, ValidationError

from src import data


class RecipeInput(BaseModel):
    name: str
    ingredients: list[str]
    instructions: str
    created_by: str
    rate: int


def _validate(payload):
    try:
        return RecipeInput.model_validate(payload)
    except ValidationError:
        return None


def _find(recipe_id):
    return next((r for r in data.recipes if r["id"] == recipe_id), None)


def get_all_recipes():
    return 200, data.recipes


def get_recipe(recipe_id):
    recipe = _find(recipe_id)
    return (200, recipe) if recipe else (404, None)


def create_recipe(payload):
    valid = _validate(payload)
    if valid is None:
        return 400, None
    new_recipe = {
        "id": max((r["id"] for r in data.recipes), default=0) + 1,
        **valid.model_dump(),
        "creation_date": datetime.date.today().isoformat(),
    }
    data.recipes.append(new_recipe)
    return 201, new_recipe


def update_recipe(recipe_id, payload):
    valid = _validate(payload)
    if valid is None:
        return 400, None
    recipe = _find(recipe_id)
    if recipe is None:
        return 404, None
    recipe.update(valid.model_dump())
    return 200, recipe


def remove_recipe(recipe_id):
    recipe = _find(recipe_id)
    if recipe is None:
        return 404, None
    data.recipes.remove(recipe)
    return 204, None
