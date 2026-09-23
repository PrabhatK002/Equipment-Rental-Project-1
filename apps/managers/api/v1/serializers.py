from rest_framework import serializers
from apps.accounts.models import RoleChoice
from apps.managers.models import Manager
from rest_framework.validators import ValidationError

class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager

        fields = [
            "id",
            "user",
            "employee_code",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.username

        return data

    def validate_user(self, user):
        logged_user = self.context['request'].user

        if logged_user.role == RoleChoice.ADMIN:
            return user

        elif logged_user.role == RoleChoice.MANAGER and logged_user == user:
            return user

        else:
            raise ValidationError("You don't have permission to access this part.")
