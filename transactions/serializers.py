from rest_framework import serializers
from .models import Transaction
from tags.models import Tag
from tags.serializers import TagSerializer
from datetime import datetime


class TransactionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(required=False)
    year_month_reference = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "name",
            "description",
            "value",
            "status",
            "type",
            "created_at",
            "tag",
            "year_month_reference",
        ]

    def create(self, validated_data: dict):
        tag_data = validated_data.pop("tag", None)
        if tag_data:
            try:
                tag = Tag.objects.get(sub_tag_name=tag_data["sub_tag_name"].title())

            except Tag.DoesNotExist as _:
                tag = Tag.objects.create(
                    tag_name=tag_data["tag_name"].title(),
                    sub_tag_name=tag_data["sub_tag_name"].title(),
                )

            transaction = Transaction.objects.create(**validated_data, tag=tag)

        else:
            transaction = Transaction.objects.create(**validated_data)

        return transaction

    def update(self, instance: Transaction, validated_data: dict):
        for key, value in validated_data.items():
            if key == "tag":
                tag = Tag.objects.filter(
                    tag_name=value["tag_name"],
                    sub_tag_name=value["sub_tag_name"],
                ).first()
                if tag:
                    instance.tag = tag

                else:
                    tag = Tag.objects.create(
                        tag_name=value["tag_name"],
                        sub_tag_name=value["sub_tag_name"],
                    )
                    instance.tag = tag

                instance.save()

            else:
                setattr(instance, key, value)

        instance.save()
        return instance

    def validate_year_month_reference(self, value):
        try:
            datetime.strptime(value, "%Y-%m").date()
        except ValueError:
            raise serializers.ValidationError(
                f"Invalid date format ({value}) must have the following pattern YYYY-mm"
            )

        return value
