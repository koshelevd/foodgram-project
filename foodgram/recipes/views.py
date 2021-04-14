from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from recipes.forms import RecipeForm
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

def get_ingredients(request):
    for key in request.POST:
        print(key)

@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe, author__username=username,
                                   slug=slug)
        print(recipe)
        form = RecipeForm(instance=recipe)
        return render(request, 'recipes/new_recipe.html', {'form': form})

    print(request.POST or None)
    new_recipe_form = RecipeForm(request.POST or None, request.FILES or None)
    get_ingredients(request)
    if not new_recipe_form.is_valid():
        return render(request, 'recipes/new_recipe.html', {'form':
                                                               new_recipe_form})
    #
    recipe = new_recipe_form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    new_recipe_form.save_m2m()
    return redirect(reverse('recipe', args=(recipe.author, recipe.slug)))

    # return render(request, 'recipes/new_recipe.html', {})
