from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import IngredientSerializer
from recipes.models import Ingredient


@api_view(['GET'])
@permission_classes([AllowAny])
def api_get_ingredients(request):
    query = request.GET.get('query', None)
    if query:
        ingredients = Ingredient.objects.all().filter(name__startswith=query)
        serializer = IngredientSerializer(ingredients, many=True)
        return JsonResponse(serializer.data, safe=False)
    return Response({'error': 'Something went wrong'})
