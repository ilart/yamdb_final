from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    ReviewViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)
from users.views import UsersViewSet, get_token, validate_token, get_me


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    'users', UsersViewSet, basename='users'
)

urlpatterns = [
    path('v1/users/me/', get_me, name='user_me'),
    path('v1/auth/signup/', validate_token, name='validation'),
    path('v1/auth/token/', get_token, name='request_token'),
    path('v1/', include(router_v1.urls)),
]
