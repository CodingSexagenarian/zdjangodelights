from django.shortcuts import render
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.core.exceptions import SuspiciousOperation

# Import the generic views below:
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.


class HomeView(TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientsView(ListView):
    template_name = "inventory/ingredients_list.html"
    model = Ingredient


class NewIngredientView(CreateView):
    template_name = "inventory/add_ingredient.html"
    model = Ingredient
    form_class = IngredientForm


class UpdateIngredientView(UpdateView):
    template_name = "inventory/update_ingredient.html"
    model = Ingredient
    form_class = IngredientForm


class DeleteIngredientView(DeleteView):
    template_name = "inventory/delete.html"
    model = Ingredient
    form_class = IngredientForm


class MenuView(ListView):
    template_name = "inventory/menu_list.html"
    model = MenuItem


class NewMenuItemView(CreateView):
    template_name = "inventory/add_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm


class UpdateMenuItemView(UpdateView):
    template_name = "inventory/update_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm


class DeleteMenuItemView(DeleteView):
    template_name = "inventory/delete.html"
    model = MenuItem
    form_class = MenuItemForm


class NewRecipeRequirementView(CreateView):
    template_name = "inventory/add_recipe_requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class UpdateRecipeRequirementView(UpdateView):
    template_name = "inventory/update_recipe_requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class DeleteRecipeRequirementView(DeleteView):
    template_name = "inventory/delete.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class PurchasesView(ListView):
    template_name = "inventory/purchase_list.html"
    model = Purchase


class NewPurchaseView(TemplateView):
    template_name = "inventory/add_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context

    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchases")


class UpdatePurchasesView(UpdateView):
    template_name = "inventory/update_purchase.html"
    model = Purchase


class DeletePurchasesView(DeleteView):
    template_name = "inventory/delete.html"
    model = Purchase
