from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from recipes.forms import RecipeForm, IngredientFormset
from recipes.models import Recipe, User, Ingredient


# def index(request):
#     recipes_list = Recipe.objects.all()
#     paginator = Paginator(recipes_list, 6)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     return render(
#         request,
#         'recipes/recipe_list.html',
#         {
#             'page': page,
#             'paginator': paginator,
#         }
#     )

class RecipeList(ListView):
    model = Recipe
    paginate_by = 6


class RecipeDetail(DetailView):
    model = Recipe


# def recipe_view(request, username, slug):
#     recipe = get_object_or_404(Recipe, slug=slug, author__username=username)
#     return render(
#         request,
#         'recipes/recipe_detail.html',
#         {
#             'recipe': recipe,
#         }
#     )


@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    print(request.POST or None)
    recipe = None
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe, author__username=username,
                                   slug=slug)

        recipe_form = RecipeForm(instance=recipe)
    else:
        recipe_form = RecipeForm(request.POST or None, request.FILES or None)


    if recipe_form.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe_form.save_m2m()

        return redirect(reverse('recipe', args=(recipe.author, recipe.slug)))

    return render(request,
                  'recipes/new_recipe.html',
                  {
                      'form': recipe_form,
                  })
