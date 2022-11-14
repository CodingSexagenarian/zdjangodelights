from django.shortcuts import redirect

from django.db.models import Sum, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import SuspiciousOperation

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm

from heapq import nlargest


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientsView(LoginRequiredMixin, ListView):
    template_name = "inventory/ingredients_list.html"
    model = Ingredient


class NewIngredientView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_ingredient.html"
    model = Ingredient
    form_class = IngredientForm


class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    template_name = "inventory/update_ingredient.html"
    model = Ingredient
    form_class = IngredientForm


class DeleteIngredientView(LoginRequiredMixin, DeleteView):
    template_name = "inventory/delete_ingredient.html"
    model = Ingredient
    success_url = "/ingredients"


class MenuView(LoginRequiredMixin, ListView):
    template_name = "inventory/menu_list.html"
    model = MenuItem


class NewMenuItemView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm


class UpdateMenuItemView(LoginRequiredMixin, UpdateView):
    template_name = "inventory/update_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm


class DeleteMenuItemView(LoginRequiredMixin, DeleteView):
    template_name = "inventory/delete_menu_item.html"
    model = MenuItem
    success_url = "/menu"


class NewRecipeRequirementView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_recipe_requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class PurchasesView(LoginRequiredMixin, ListView):
    template_name = "inventory/purchase_list.html"
    model = Purchase


class NewPurchaseView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/add_purchase.html"
    model = Purchase

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


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.unit_price * \
                    recipe_requirement.quantity

        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost
        context["gross_profit"] = (revenue - total_cost) / total_cost * 100
        context["gross_margin_ratio"] = (revenue - total_cost) / revenue * 100
        context["list_of_purchases"] = Purchase.objects.values_list('menu_item', flat=True).distinct()

        return context

    def get_top_3(self, **kwargs):
        top_3 = nlargest(3, list_of_purchases)
        return top_3


def log_out(request):
    logout(request)
    return redirect("/")
