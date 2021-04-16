from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin, CreateView

from recipes.forms import RecipeForm
from recipes.models import Recipe, User, Ingredient, RecipeComposition


class RecipeList(ListView):
    model = Recipe
    paginate_by = 6


class RecipeDetail(DetailView):
    model = Recipe


@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    print(request.POST or None)
    recipe = None
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe,
                                   author__username=username,
                                   slug=slug)

    recipe_form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)


    if recipe_form.is_valid():
        recipe = recipe_form.save(request.user, commit=False)
        return redirect(reverse('recipe', args=(recipe.author, recipe.slug)))


    return render(request,
                  'recipes/new_recipe.html',
                  {
                      'form': recipe_form,
                      'recipe': recipe,
                  })


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

# def recipe_view(request, username, slug):
#     recipe = get_object_or_404(Recipe, slug=slug, author__username=username)
#     return render(
#         request,
#         'recipes/recipe_detail.html',
#         {
#             'recipe': recipe,
#         }
#     )

# class RecipeView(CreateView, LoginRequiredMixin):
#     form_class = RecipeForm
#     template_name = 'recipes/new_recipe.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.slug = slugify(form.cleaned_data['title'])
#         return super().form_valid(form)


