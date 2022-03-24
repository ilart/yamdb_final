from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Права доступа Администратора"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.is_admin
            )
        return False

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.is_authenticated
                and request.user.is_superuser
                or request.user.is_admin
            )
        return False


class IsAdminOrReadOnly(BasePermission):
    """Права доступа Администратора или доступ на чтение"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.is_admin
            )
        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.is_admin
            )
        return False


class IsAuthor(BasePermission):
    """Права доступа автора обьекта"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(BasePermission):
    """Права доступа модератора"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (
                request.user.is_authenticated
                and request.user.is_moderator
            )
        return False

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.is_authenticated
                and request.user.is_moderator
            )
        return False


class IsModeratorOrReadOnly(BasePermission):
    """Права доступа модератора или доступ на чтение"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_authenticated
                and request.user.is_moderator
            )
        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_authenticated
                and request.user.is_moderator
            )
        return False


class IsUser(BasePermission):
    """Права доступа Пользователя"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (
                request.user.is_user
            )
        return False

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_user
        return False


class IsUserOrReadOnly(BasePermission):
    """Права доступа Пользователя или доступ на чтение"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_user
            )
        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.is_user
        return False


class ReviewPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_moderator
                or request.user.is_admin
                or request.user.is_user
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user
            )
        return False


class CommentPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_moderator
                or request.user.is_admin
                or request.user.is_user
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (
                request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user
            )
        return False
