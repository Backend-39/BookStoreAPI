from rest_framework import serializers
from main.models import Account, Book, Image

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)    

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'username', 'first_name', 'last_name', 'email'
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = "__all__"

class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'account': {
                'read_only': True
            }
        }

        
