from profiles_api import models
from rest_framework import serializers

class HelloAPISerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
                        'password' : {
                                    'write_only' : True,
                                    'style' : {'input_type':'password'}
                                    }
                        }

    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
        name = validated_data['name'],
        email = validated_data['email'],
        password = validated_data['password']
        )
        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = ['id', 'user_profile', 'status_text', 'created_at']
        extra_kwargs = {'user_profile':{'read_only':True}}
        
    