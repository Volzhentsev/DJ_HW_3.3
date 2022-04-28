from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement

from rest_framework.exceptions import ValidationError
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context["request"].user
        open_status = Advertisement.objects.filter(creator_id=user.id, status='OPEN').count()
        if open_status >= settings.MAX_OPEN_ADVERTISMENT_PER_USER:
            raise ValidationError('Too many advertisement per user!')

        return data
