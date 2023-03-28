from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Tag, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, TagSerializer, CommentSerializer
from .permissions import IsAuthor


"""  
@api_view - вьюшки на функциях

rest_framework.views.APIView - вьюшки на классах без функционала

rest_framework.generics - вьюшки на готовых классах

rest_framework.viewsets - класс для обработки всех операций CRUD
"""
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.filter(status='OPEN')
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['tag', 'status']
    search_fields = ['title', 'tag__title']


    def get_queryset(self):
        if self.request.user.is_staff:
            self.queryset = Article.objects.all()
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'comment':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    @action(methods=['POST', 'DELETE', 'PATCH'], detail=True)
    def comment(self, request: Request, pk=None):
        article = self.get_object()
        if self.request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.action == 'comment':
            return CommentSerializer
        return super().get_serializer_class()
    

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
action - действия пользователя
list
retrieve
create
update  
destroy
"""


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# TODO: наполнить сайт контентом
