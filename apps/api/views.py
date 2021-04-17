from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.api.models import Favorite
from apps.api.serializers import IngredientSerializer, FavoriteSerializer
from apps.recipes.models import Ingredient


class FavoritesView(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer



@api_view(['GET'])
@permission_classes([AllowAny])
def api_get_ingredients(request):
    query = request.GET.get('query', None)
    if query is not None:
        ingredients = Ingredient.objects.all().filter(name__startswith=query)
        serializer = IngredientSerializer(ingredients, many=True)
        return JsonResponse(serializer.data, safe=False)
    return Response({'error': 'Something went wrong'})


