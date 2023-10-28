from . import models

def product_categories(request):

    return {
        'categories': models.Category.objects.all()
    }