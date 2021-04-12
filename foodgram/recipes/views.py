from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from recipes.models import Recipe, User


def index(request):
    recipes_list = Recipe.objects.all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'paginator': paginator,
        }
    )

def recipe_view(request, username, slug):
    recipe = get_object_or_404(Recipe, slug=slug, author__username=username)
    return render(
        request,
        'recipes/recipe.html',
        {
            'recipe': recipe,
        }
    )

@login_required
def new_recipe(request):
    new_post_form = PostForm(request.POST or None)
    if not new_post_form.is_valid():
        return render(request, 'posts/new_post.html', {'form': new_post_form})

    post = new_post_form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect(reverse('index'))

