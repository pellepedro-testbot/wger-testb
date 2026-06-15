# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

# Third Party
from rest_framework import (
    exceptions,
    viewsets,
)


def _check_owner_objects(owner_entries, request_data, request_user):
    """
    Verify that every referenced related object belongs to the requesting user.

    Iterates over *owner_entries* — a list of ``(Model, field_name)`` tuples —
    and raises :class:`rest_framework.exceptions.ValidationError` when
    *request_data* is not a plain dictionary, or
    :class:`rest_framework.exceptions.PermissionDenied` when the primary key
    stored in ``request_data[field_name]`` resolves to an object whose owner is
    not *request_user*.
    """
    for model_cls, field_name in owner_entries:
        if not isinstance(request_data, dict):
            raise exceptions.ValidationError('Request data is not a dictionary')

        pk = request_data.get(field_name)
        if pk:
            obj = model_cls.objects.get(pk=pk)
            if obj.get_owner_object().user != request_user:
                raise exceptions.PermissionDenied('You are not allowed to do this')


class WgerOwnerObjectModelViewSet(viewsets.ModelViewSet):
    """
    Custom viewset that makes sure the user can only create objects for himself
    """

    def create(self, request, *args, **kwargs):
        """
        Check for creation (PUT, POST)
        """
        _check_owner_objects(self.get_owner_objects(), request.data, request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Check for updates (PUT, PATCH)
        """
        _check_owner_objects(self.get_owner_objects(), request.data, request.user)
        return super().update(request, *args, **kwargs)
