from django.db import models

UNIT_CHOICES = [
    ("g", "gram"),
    ("tbsp", "tablespoon"),
    ("tsp", "teaspoon"),
    ("l", "liter"),
    ("ea", "each"),
    ("cup", "cup"),
    ("oz", "ounces"),
    ("lbs", "pound"),
    ("", ""),
]

# Create your models here.
"""This model represents an ingredient that the restaurant has in 
its inventory.
"""


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name", unique=True)
    quantity = models.FloatField(default=0.0, verbose_name="Quantity")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="",
                            verbose_name="Unit of Measure")
    unit_price = models.FloatField(default=0.0, verbose_name="Unit Price")

    def __str__(self):
        return f"{self.name}: {self.unit_price} {self.unit}"

    def get_absolute_url(self):
        return "/ingredients"

    class Meta:
        ordering = ["name"]

"""
This model represents an item on the restaurant’s menu.
"""


class MenuItem(models.Model):
    name = models.CharField(max_length=200, unique=True,
                             verbose_name="Item Name")
    price = models.FloatField(default=0.00, verbose_name="Price")
    description = models.CharField(max_length=500, default="",
                                   verbose_name="Item Description")
    def __str__(self):
        return f"name={self.name}; price={self.price}"

    def get_absolute_url(self):
        return "/menu"

    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())

    class Meta:
        ordering = ["name"]

"""
This model represents a single ingredient and how much of it is required 
for an item off the menu.
"""


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE,
                                  verbose_name="Menu Item")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name="Ingredient")
    quantity = models.FloatField(default=0, verbose_name="Quantity")

    def __str__(self):
        return f"menu_item=[{self.menu_item.__str__()}]; " \
               f"ingredient={self.ingredient.name}; qty={self.quantity}"

    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        return self.quantity <= self.ingredient.quantity


class Purchase(models.Model):

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE,
                                  verbose_name="Menu Item")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="DateTime")

    def __str__(self):
        return f"menu_item=[{self.menu_item.__str__()}]; time={self.timestamp}"

    def get_absolute_url(self):
        return "/purchases"

    class Meta:
        ordering = ["timestamp"]
