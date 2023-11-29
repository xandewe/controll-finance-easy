from rest_framework import serializers
from .models import Transaction
from tags.models import Tag
from tags.serializers import TagSerializer


class TransactionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(required=False)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "name",
            "description",
            "value",
            "status",
            "category",
            "created_at",
            "tag",
        ]

    def create(self, validated_data: dict):
        tag_data = validated_data.pop("tag", None)
        if tag_data:
            try:
                tag = Tag.objects.get(sub_tag_name=tag_data["sub_tag_name"].title())

            except Tag.DoesNotExist as _:
                tag = Tag.objects.create(
                    tag_name=tag_data["tag_name"],
                    sub_tag_name=tag_data["sub_tag_name"].title(),
                )

            transaction = Transaction.objects.create(**validated_data, tag=tag)

        else:
            transaction = Transaction.objects.create(**validated_data)

        return transaction
