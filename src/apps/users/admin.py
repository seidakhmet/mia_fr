from typing import Any

from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import GroupExtra

User = get_user_model()


class UserAdmin(auth_admin.UserAdmin):
    """Админка пользователей"""

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "password",
                    "email",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_developer",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "changed_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_staff"),
            },
        ),
    )
    ordering = ("username",)
    readonly_fields = ("username", "last_login", "created_at", "changed_at")
    list_display = ("username", "email", "user_groups")
    search_fields = (
        "username",
        "email",
        "groups__name",
        "groups__extra__type",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )

    @admin.display(description=_("groups"))
    def user_groups(self, obj):
        """Получить группы, разделенные запятой, и отобразить пустую строку, если у пользователя нет групп."""
        user_groups = obj.groups.all()
        return ",".join([g.name for g in user_groups])

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("groups")
        return queryset


class GroupExtraInline(admin.TabularInline):
    model = GroupExtra


class GroupExtraAdmin(auth_admin.GroupAdmin):
    inlines = [GroupExtraInline]
    list_display = (
        "name",
        "extra",
    )
    list_select_related = ("extra",)


admin.site.register(User, UserAdmin)
admin.site.unregister(auth_admin.Group)
admin.site.register(auth_admin.Group, GroupExtraAdmin)
