"""View classes and functions of the 'recipes' app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from apps.recipes.forms import RecipeForm, TagForm
from apps.recipes.models import Follow, Purchase, Recipe, Tag, User
from apps.recipes.utils import create_pdf


class FollowList(LoginRequiredMixin, ListView):
    """ListView for following's page of the user."""
    model = Follow
    paginate_by = 6

    def get_queryset(self):
        """Filter queryset by current user."""
        return Follow.objects.filter(user=self.request.user)


class PurchaseList(LoginRequiredMixin, ListView):
    """ListView for recipes in shopping list."""
    model = Purchase


class RecipeList(ListView):
    """ListView for recipes."""
    model = Recipe
    paginate_by = 6

    def get_queryset(self):
        """Filter queryset by tags passed."""
        default_filter = Tag.objects.values_list('id')
        posted_filter = self.request.GET.getlist('tags', default_filter)
        queryset = Recipe.objects.filter(tags__in=posted_filter).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Pass additional form for filter."""
        context = super().get_context_data(**kwargs)
        context['form'] = TagForm(self.request.GET or None)
        return context


class FavoritesList(LoginRequiredMixin, RecipeList):
    """ListView for favorites page."""

    def get_queryset(self):
        """Filter only favorited recipes of the user."""
        queryset = super().get_queryset()
        all_favorites = self.request.user.favorites.all().values('recipe')
        return queryset.filter(id__in=all_favorites)

    def get_context_data(self, **kwargs):
        """Pass favorites=True to context."""
        context = super().get_context_data(**kwargs)
        context['favorites'] = True
        return context


class AuthorList(RecipeList):
    """List view for author's recipes."""

    def get_queryset(self):
        """Filter queryset by author."""
        queryset = super().get_queryset()
        author = get_object_or_404(User, username=self.kwargs['username'])
        return queryset.filter(author=author)

    def get_context_data(self, **kwargs):
        """Pass following=True to context if author is followed by user."""
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        context['author'] = author
        following = (Follow.objects.filter(author=author,
                                           user=self.request.user).exists()
                     if self.request.user.is_authenticated
                     else False)
        context['following'] = following
        return context


class RecipeDetail(DetailView):
    """DetailView for single recipe."""
    model = Recipe


@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    """Process add or update of the recipe."""
    recipe = None
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe,
                                   author__username=username,
                                   slug=slug)

    recipe_form = RecipeForm(request.POST or None, request.FILES or None,
                             instance=recipe)

    if recipe_form.is_valid():
        recipe = recipe_form.save(user=request.user)
        return redirect(reverse('recipe', args=(recipe.author, recipe.slug)))

    return render(request,
                  'recipes/recipe_form.html',
                  {
                      'form': recipe_form,
                      'recipe': recipe,
                  })


@login_required
def delete_confirm(request, username, slug):
    """Ask user to confirm if he wants to delete the recipe."""
    return render(request,
                  'recipes/recipe_delete.html',
                  {
                      'username': username,
                      'slug': slug,
                  })


@login_required
def delete_recipe(request, username, slug):
    """Delete the recipe."""
    recipe = get_object_or_404(Recipe,
                               author__username=username,
                               slug=slug)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def shoplist_pdf(request):
    """Select ingredients from shopping list and create pdf-document."""
    ingredients = request.user.purchases.select_related(
        'recipe'
    ).order_by(
        'recipe__ingredients__name'
    ).values(
        'recipe__ingredients__name', 'recipe__ingredients__unit'
    ).annotate(quantity=Sum('recipe__compositions__quantity')).all()

    return create_pdf(ingredients, 'shoplist.pdf')
