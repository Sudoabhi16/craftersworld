from rest_framework import serializers
from .models import Organisation, User


# -----------------------------
# Base Organisation Serializer
# -----------------------------
class OrganisationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["id", "name", "type"]


class OrganisationDetailSerializer(OrganisationBaseSerializer):
    class Meta(OrganisationBaseSerializer.Meta):
        fields = OrganisationBaseSerializer.Meta.fields + [
            "address",
            "contact_email",
            "contact_phone",
            "created_at",
        ]


# -----------------------------
# Base User Serializer
# -----------------------------
class UserBaseSerializer(serializers.ModelSerializer):
    organisation = OrganisationBaseSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "organisation"]


class UserDetailSerializer(UserBaseSerializer):
    organisation = OrganisationDetailSerializer(read_only=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + [
            "first_name",
            "last_name",
            "is_verified",
            "profile_picture",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    organisation_id = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        source="organisation",
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "organisation_id",
            "role",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user
