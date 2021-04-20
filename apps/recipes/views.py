from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from apps.recipes.forms import RecipeForm, TagForm
from apps.recipes.models import Recipe, Tag, User, Follow


class FollowList(ListView):
    model = Follow
    paginate_by = 3


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
    print(request.POST or None)
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
