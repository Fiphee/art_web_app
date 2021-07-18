from artworks.models import Category


class CategoryUtils:
    
    @staticmethod
    def create_categories(categories):
        category_objects = []
        tags = [tag.lower() for tag in categories.replace(' ', '').split(',')]
        for tag in tags:
            category = Category.objects.filter(name=tag)
            if category.exists():
                category_objects.append(category.first())
            else:
                category = Category.objects.create(name=tag)
                # category.save()
                category_objects.append(category)
        return category_objects


    @staticmethod
    def add_categories_to_instance(categories, instance):
        for category in categories:
            instance.category.add(category)