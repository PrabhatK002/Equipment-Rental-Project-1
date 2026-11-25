from rest_framework import serializers
from apps.maintenances.models import Maintenance


class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["equipment"] = instance.equipment.name
