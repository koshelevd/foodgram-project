from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from apps.api.serializers import IngredientSerializer, FavoriteSerializer, \
    FollowSerializer
from apps.recipes.models import Ingredient, Favorite, Follow


class CreateDestroyView(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={}, status=status.HTTP_200_OK)

class FavoritesView(CreateDestroyView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe'


class FollowView(CreateDestroyView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'author'



@api_view(['GET'])
@permission_classes([AllowAny])
def api_get_ingredients(request):
    query = request.GET.get('query', None)
    if query is not None:
        ingredients = Ingredient.objects.all().filter(name__startswith=query)
        serializer = IngredientSerializer(ingredients, many=True)
        return JsonResponse(serializer.data, safe=False)
    return Response({'error': 'Something went wrong'})


