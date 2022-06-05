import csv

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class GetCSVView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        shopping_cart = request.user.shopping_cart.all()
        response = HttpResponse(content_type='text/csv')
        filename = f'{request.user.username}_items.csv'
        response['Content-Disposition'] = ('attachment;'
                                           f'filename="{filename}"')

        writer = csv.writer(response)
        for item in shopping_cart:
            writer.writerow([item.name])

            writer.writerow(['Ингредиент', 'Количество', 'Единица измерения'])
            for ingredient in item.ingredientforrecipe_set.all():
                writer.writerow(
                    [ingredient.ingredient.name, ingredient.amount,
                     ingredient.ingredient.unit]
                )
            writer.writerow(['____________'])

        return response
