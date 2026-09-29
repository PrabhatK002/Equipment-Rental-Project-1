from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

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

    def validate_daily_rate(self, daily_rate):
        if daily_rate < 0:
            raise ValidationError("The value of daily rate should be greater than 0.")
        return daily_rate

    def validate_weekly_rate(self, weekly_rate):
        if weekly_rate and weekly_rate < 0:
            raise ValidationError("The value of weekly rate should be greater than 0.")

        return weekly_rate


    def validate_security_deposit(self, security_deposit):
        if security_deposit < 0:
            raise ValidationError("The value of security deposit should be greater than 0.")

        return security_deposit


    def validate_replacement_value(self, replacement_value):
        if replacement_value < 0:
            raise ValidationError("The value of replacement value should be greater than 0.")

        return replacement_value

    



