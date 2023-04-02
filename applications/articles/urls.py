from rest_framework.routers import DefaultRouter 
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly

from .views import ArticleViewSet, TagViewSet, CommentViewSet


router = DefaultRouter() # Роутеры - специальный класс для автоматического создания путей/ссылок
router.register('article', ArticleViewSet, 'articles')
router.register('tags', TagViewSet, 'tags')
router.register('comment', CommentViewSet, 'comments')

urlpatterns = router.urls


