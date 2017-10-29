"""
This modudle handles CRUD for Recipe Categories and Recipes
"""
CATEGORIES = {}

class Categories(object):
    """This class contains the CRUD features for Categories"""

    def __init__(self):
        """Initialize objects of this class with the following"""
        self.name = ''
        self.description = ''
        self.recipes = {}

    def add_category(self, name, description):
        """Add to categories list"""
        self.name = name
        self.description = description
        if self.name in CATEGORIES:
            return "Sorry. Category already exists"
        CATEGORIES[name] = {
            "name": self.name,
            "description": self.description,
            "recipes": self.recipes
        }
        return CATEGORIES[name]

    def get_category(self, name):
        """Returns the named category or error message"""
        if name in CATEGORIES:
            return CATEGORIES[name]
        return "Category does not exist."

    def set_category(self, name, description=None):
        """Returns the updated category or error message"""
        if name in CATEGORIES:
            CATEGORIES[name] = {
                "name": name, "description": description, 'recipes': CATEGORIES[name]['recipes']
            }
            return CATEGORIES[name]
        return "Category does not exist."

    def delete_category(self, name):
        """Deletes a category and returns confirmation or error"""
        if name in CATEGORIES:
            CATEGORIES.pop(name)
            return "Removed successfully."
        return "Category does not exist."

class Recipes(object):
    """
    This is subclass of the Categories class
    This class contains the CRUD features for recipes
    """

    def __init__(self):
        """Default constructor"""

    def add_recipe(self, category, recipe):
        """Add a new recipe only to existing categories"""
        if category in CATEGORIES:
            CATEGORIES[category]['recipes'][recipe['name']] = recipe
            return "Recipe added successfully."
        return "Category does not exist."

    def get_recipe(self, category, name):
        """Get the recipe from the spefied category"""
        if category not in CATEGORIES:
            return "Recipe does not exist"
        if name in CATEGORIES[category]['recipes']:
            recipe = CATEGORIES[category]['recipes'][name]
            return recipe

    def set_recipe(self, category, name, content):
        """Get the recipe from the spefied category"""
        if category not in CATEGORIES:
            return "Recipe does not exist"
        if name in CATEGORIES[category]['recipes']:
            CATEGORIES[category]['recipes'][name].update(content)
            temp_recipe = CATEGORIES[category]['recipes'].pop(name)
            CATEGORIES[category]['recipes'][temp_recipe['name']] = temp_recipe
            return CATEGORIES[category]['recipes']
        return "Recipe does not exist"

    def delete_recipe(self, category, name):
        """Removes the named recipe in the category provided"""
        if category in CATEGORIES and name in CATEGORIES[category]['recipes']:
            CATEGORIES[category]['recipes'].pop(name)
            return "Recipe deleted successfully!"
        return "Recipe does not exist!"
