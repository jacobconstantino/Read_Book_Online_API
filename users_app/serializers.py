from rest_framework import serializers

from .models import Users

class UserSerializers(serializers.ModelSerializer):

    def create(self,validated_data):
     
        new_users = Users.objects.create(**validated_data)

        return new_users

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.country = validated_data.get('country', instance.country)
        instance.agent = validated_data.get('agent', instance.agent)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.password = validated_data.get('password', instance.password)
        instance.is_user_verified = validated_data.get('is_user_verified', instance.is_user_verified)

       
        instance.save()

        return instance

    class Meta:
        model = Users
        fields = '__all__'
