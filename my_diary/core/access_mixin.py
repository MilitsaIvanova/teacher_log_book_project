from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class GroupRequiredMixin(AccessMixin):
    allowed_groups = []

    def dispatch(self, request, *args, **kwargs):
        user_groups = set(request.user.groups.values_list('name', flat=True))

        if not user_groups.intersection(set(self.allowed_groups)) and not request.user.is_superuser and \
                not request.user.is_staff:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
