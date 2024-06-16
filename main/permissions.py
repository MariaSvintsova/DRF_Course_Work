from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD"""

    def has_permission(self, request, view):
        if request.user == view.get_oblect().user:
            return request.method in ['PUT', 'PATCH', 'DELETE']
