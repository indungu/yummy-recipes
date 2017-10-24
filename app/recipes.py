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
        self.recipes = []

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
        return CATEGORIES[self.name]

    def get_category(self, name):
        """Returns the named category or error message"""
        if name in CATEGORIES:
            return CATEGORIES[name]
        return "Category does not exist."

    def set_category(self, name, description=None, recipes=None):
        """Returns the updated category or error message"""
        if name in CATEGORIES:
            CATEGORIES[name] = {"name": name, "description": description, "recipes": recipes}
            return CATEGORIES[name]
        return "Category does not exist."

    def delete_category(self, name):
        """Deletes a category and returns confirmation or error"""
        if name in CATEGORIES:
            CATEGORIES.pop(name)
            return "Removed successfully."
        return "Category does not exist."
