from rest_framework import serializers
from apps.accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name','phone']



class UserInfoSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        exclude = ['password']
