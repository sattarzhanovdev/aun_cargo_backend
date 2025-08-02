from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # если это PUT-запрос — делаем pickUpPoint необязательным
        request = self.context.get('request')
        if request and request.method == 'PUT':
            self.fields['pickUpPoint'].required = False