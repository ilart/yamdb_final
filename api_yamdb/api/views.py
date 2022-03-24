from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import mixins, viewsets, serializers
from rest_framework.filters import SearchFilter

from api.filters import TitleFilterSet
from api.serializers import (
    CategorySerializer,
    TitleSerializer,
    TitleListSerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Category, Genre, Title, Review
from users.permissions import (
    IsAdminOrReadOnly,
    CommentPermission,
    ReviewPermission
)

SECOND_REVIEW_FORBIDDEN = (
    "Пользователь может оставить только один отзыв на произведение"
)


class CreateListDeployViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, )
    filterset_class = TitleFilterSet
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleListSerializer
        return TitleSerializer


class GenreViewSet(CreateListDeployViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )


class CategoryViewSet(CreateListDeployViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission, )

    def get_queryset(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        ).reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(
            title=self.kwargs.get('title_id'),
            author=self.request.user
        ):
            raise serializers.ValidationError(SECOND_REVIEW_FORBIDDEN)
        return serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission, )

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                     title=self.kwargs.get('title_id')),
        )
