from rest_framework.viewsets import ModelViewSet
from .models import Article, Tag
from .serializers import ArticleSerializer, ArticleListSerializer, TagSerializer


"""  
@api_view - вьюшки на функциях

rest_framework.views.APIView - вьюшки на классах без функционала

rest_framework.generics - вьюшки на готовых классах

rest_framework.viewsets - класс для обработки всех операций CRUD
"""
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer