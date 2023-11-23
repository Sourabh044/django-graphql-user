from rest_framework import serializers
from .models import User
import traceback
class UserCreateSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        try:
            user =  super().save(**kwargs)
        except Exception as e:
            print(traceback.format_exc())
            raise e
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user  
    
    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update not allowed on this mutation.')
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','password')


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    username = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data['password']
            instance.set_password(password)
        user_instance =  super().update(instance, validated_data)
        return user_instance
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','password')