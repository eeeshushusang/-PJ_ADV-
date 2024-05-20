from rest_framework import serializers

from adv.models import Adv


class AdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adv
        fields = '__all__'
