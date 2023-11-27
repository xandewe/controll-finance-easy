from rest_framework import serializers
from .models import Transaction
from tags.models import Tag
from tags.serializers import TagSerializer


class TransactionSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "name",
            "surname",
            "value",
            "status",
            "credit_card",
            "category",
            "created_at",
            "tag",
        ]

    def create(self, validated_data: dict):
        tag_data = validated_data.pop("tag")["tag_name"]
        tag, _ = Tag.objects.get_or_create(tag_name=tag_data.title())

        transaction = Transaction.objects.create(**validated_data, tag=tag)

        return transaction
