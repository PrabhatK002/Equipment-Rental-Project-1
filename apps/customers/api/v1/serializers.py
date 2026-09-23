from rest_framework import serializers

from apps.customers.models import CustomerProfile


class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = [
            "id",
            "date_of_birth",
            "address",
            "country",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_verified",
            "created_at",
            "updated_at",
        ]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        return data
