from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Tag, Comment, Like
from .serializers import ArticleSerializer, TagSerializer, CommentSerializer, RatingSerializer
from .permissions import IsAuthor


"""  
@api_view - вьюшки на функциях

rest_framework.views.APIView - вьюшки на классах без функционала

rest_framework.generics - вьюшки на готовых классах

rest_framework.viewsets - класс для обработки всех операций CRUD
https://www.django-rest-framework.org/api-guide/viewsets/
"""

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all() # запрос отправляемый в базу данных
    serializer_class = ArticleSerializer # сериалайзер используемый для выдачи/запроса данных
    filter_backends = [filters.SearchFilter, DjangoFilterBackend] # классы используемые для фильтрации
    filterset_fields = ['tag', 'status'] # поля модели Article по которым будет фильтрация
    search_fields = ['title', 'tag__title'] # поля модели по которым будет идти поиск


    def get_serializer_context(self):
        """  
        Метод для добавления дополнительных данных в сериалайзеры
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_permissions(self):
        """  
        Метод отвечающий за выдачу прав различным пользователям
        https://www.django-rest-framework.org/api-guide/permissions/
        """
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_class(self):
        """  
        Выдача разных сериализаторов в зависимости от вызываемой функции
        """
        if self.action == 'comment':
            return CommentSerializer
        elif self.action == 'rate_article':
            return RatingSerializer
        return super().get_serializer_class()
    
    @action(methods=['POST', 'DELETE'], detail=True)
    def comment(self, request, pk=None):
        """  
        декоратор action позволяет добавить новую функцию в качестве действия для ViewSetов
        https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
        """
        article = self.get_object()
        # self.get_object() -> Article.objects.get(pk=pk)
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
        return Response({'TODO': 'ДОБАВИТЬ УДАЛЕНИЕ КОММЕНТА'})
    
    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_article(self, request, pk=None) -> Response:
        article = self.get_object()
        serializer = RatingSerializer(data=request.data, context={'request': request, 'article': article})
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article)
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        article = self.get_object()
        like = Like.objects.filter(user=request.user, article=article)
        if like.exists():
            like.delete()
            return Response({'liked': False})
        else:
            Like.objects.create(user=request.user, article=article).save()
            return Response({'liked': True})
        



class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

"""
actions - действия пользователя
list
retrieve
create
update  
destroy
"""


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# TODO: переопределить метод get_permission_classes в TagViewSet, так чтобы только залогинненные пользователи могли создавать теги
# TODO: наполнить сайт контентом
