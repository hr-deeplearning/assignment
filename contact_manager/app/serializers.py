from rest_framework import serializers
from .models import Contact, ContactPhone, CustomUser
from django.db.models import Prefetch


class ContactPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPhone
        fields = ["id", "number"]


class ContactSerializer(serializers.ModelSerializer):
    phones = ContactPhoneSerializer(many=True)

    class Meta:
        model = Contact
        fields = ["id", "fullname", "description", "phones"]



    def create(self, validated_data):

        phones_data = validated_data.pop("phones")
        user = self.context["request"].user
        contact = Contact.objects.create(**validated_data, created_user=user)
        for phone_data in phones_data:
            ContactPhone.objects.create(
                contact=contact, created_user=user, **phone_data
            )
        return contact

    def update(self, instance, validated_data):
        print(validated_data)
        user = self.context["request"].user
        phones_data = validated_data.pop("phones")
        instance.fullname = validated_data.get("fullname", instance.fullname)
        instance.is_deleted = validated_data.get("is_deleted", instance.is_deleted)

        instance.save()

        # Update phones
        input_phones = set(
            [
                ContactPhone(number=phone_data.get("number"))
                for phone_data in phones_data
            ]
        )

        print(input_phones)
        exist_phones = set(
            ContactPhone.objects.filter(is_deleted=False, contact=instance)
        )
        print(exist_phones)

        should_insert_phones = input_phones - exist_phones

        for phone in should_insert_phones:
            phone.contact = instance
            phone.created_user = user
            phone.save()

        should_remove_phones = exist_phones - input_phones
        for phone in should_remove_phones:
            phone.is_deleted = True
            phone.save()

        instance = (
            Contact.objects.filter(pk=instance.id)
            .prefetch_related(
                Prefetch(
                    "phones", queryset=ContactPhone.objects.filter(is_deleted=False)
                )
            )
            .first()
        )
        return instance


class UserSignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_deleted",
        ]
