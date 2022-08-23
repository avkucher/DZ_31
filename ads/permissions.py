from ads.models import Ad, Selection
from django.http import Http404
from rest_framework.permissions import BasePermission
from users.models import User

"""Разрешение на редактирование объявления только для владельцев объявления, админа или модератора."""
class AdEditPermission(BasePermission):
    massage = 'only owner or admin (moderator) can edit ads'

    def has_permission(self, request, view):
        if request.user.role in [User.MODERATOR, User.ADMIN]:
            return True

        try:
            ad = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            return Http404

        if ad.author_id == request.user.id:
            return True
        return False

"""Разрешение на редактирование подборки объявлений только для ее владельца."""
class SelectionEditPermission(BasePermission):
    massage = 'You can only edit your own selections'

    def has_permission(self, request, view):
        try:
            selection = Selection.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            raise Http404

        if selection.owner_id == request.user.id:
            return True
        return False
