from rest_framework import serializers

from apps.equipments.models import Category, Equipment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"




class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = "__all__"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = instance.category.name
        data["location"] = instance.location.name

        return data



