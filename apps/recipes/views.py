from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from apps.recipes.forms import RecipeForm, TagForm
from apps.recipes.models import Recipe, Tag, User, Follow, Purchase


class PurchaseList(ListView):
    model = Purchase


class FollowList(ListView):
    model = Follow
    paginate_by = 6


class RecipeList(ListView):
    model = Recipe
    paginate_by = 6

    def get_queryset(self):
        default_filter = [tag.pk for tag in Tag.objects.all()]
        filter = self.request.GET.getlist('tags', default_filter)
        print(filter)
        queryset = Recipe.objects.filter(tags__in=filter).distinct()
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['form'] = TagForm(self.request.GET or None)

        return context


class FavoritesList(RecipeList):
    def get_queryset(self):
        queryset = super().get_queryset()
        author = get_object_or_404(User, username=self.request.user)
        all_favorites = author.favorite.all().values('recipe')
        return queryset.filter(id__in=all_favorites)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = True
        return context


class AuthorList(RecipeList):
    def get_queryset(self):
        queryset = super().get_queryset()
        author = get_object_or_404(User, username=self.kwargs['username'])
        return queryset.filter(author=author)

    def get_context_data(self, **kwargs):
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
    model = Recipe


@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    recipe = None
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe,
                                   author__username=username,
                                   slug=slug)

    recipe_form = RecipeForm(request.POST or None, request.FILES or None,
                             instance=recipe)

    if recipe_form.is_valid():
        recipe = recipe_form.save(request.user, commit=False)
        return redirect(reverse('recipe', args=(recipe.author, recipe.slug)))

    return render(request,
                  'recipes/new_recipe.html',
                  {
                      'form': recipe_form,
                      'recipe': recipe,
                  })


@login_required
def shoplist_pdf(request):
    ingredients = request.user.purchase.select_related(
        'recipe'
    ).order_by(
        'recipe__ingredients__name'
    ).values(
        'recipe__ingredients__name', 'recipe__ingredients__unit'
    ).annotate(quantity=Sum('recipe__composition__quantity')).all()

    print(ingredients)

    return redirect(reverse('purchases'))
