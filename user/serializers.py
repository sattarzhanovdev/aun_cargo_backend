from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'surname',
            'phone_number',
            'password',
            'pickUpPoint',
            'client_id',
            'warehouse'
        ]
        read_only_fields = ['client_id', 'warehouse']