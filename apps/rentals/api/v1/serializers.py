from apps.carts.models import Cart, CartItem
from apps.rentals.models import Rental, RentalItem
from rest_framework import serializers
from django.shortcuts import get_object_or_404



class RentalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rental
        fields = "__all__"



class RentalItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RentalItem
        fields = "__all__"



class CheckoutSerializer(serializers.Serializer):
    cart = serializers.IntegerField()

    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )

    pickup_location_id = serializers.IntegerField()
    return_location_id = serializers.IntegerField()


    def validate(self, attrs):
        cart_id = attrs["cart"]
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({
                "cart": "Cart does not exist."
            })
        cart_item_ids = attrs["cart_item_ids"]

        cart_items = list(
            CartItem.objects.filter(id__in=cart_item_ids, cart=cart)
        )

        found_ids = {item.id for item in cart_items}
        missing_ids = set(cart_item_ids) - found_ids
        
        if missing_ids:
            raise serializers.ValidationError({
                "cart_item_ids": f"Cart items {list(missing_ids)} do not exist or do not belong to cart #{cart.id}."
            })

       
        invalid_date_items = [
            item.id for item in cart_items 
            if item.start_date >= item.end_date
        ]
        
        if invalid_date_items:
            raise serializers.ValidationError({
                "cart_item_ids": f"Cart items {invalid_date_items} have end dates on or before start dates."
            })

        return attrs




class InitiatePaymentSerializer(serializers.Serializer):
    rental_id = serializers.IntegerField()

class InitiatePaymentResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    khalti_response = serializers.DictField()

class CheckoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    rental = RentalSerializer()