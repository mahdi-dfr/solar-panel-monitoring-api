from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        # فقط کاربران لاگین‌شده
        if not user or not user.is_authenticated:
            return False

        # ادمین اجازه انجام همه عملیات را دارد
        if user.is_staff:
            return True

        # کاربر عادی فقط اجازه مشاهده و ویرایش دارد
        if request.method in [
            'GET',
            'PUT',
            'PATCH',
        ]:
            return True

        # POST و DELETE برای کاربر عادی ممنوع
        return False

    def has_object_permission(self, request, view, obj):

        # ادمین روی همه کاربران دسترسی دارد
        if request.user.is_staff:
            return True

        # کاربر عادی فقط روی خودش
        return obj.id == request.user.id