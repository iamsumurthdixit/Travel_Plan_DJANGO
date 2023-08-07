from rest_framework import serializers
from .models import *
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and start_date <= datetime.date.today():
            raise serializers.ValidationError('invalid start date')

        if end_date and start_date and start_date >= end_date:
            raise serializers.ValidationError('invalid end date')

        if self.instance:
            plan_start_date = self.instance.start_date
            plan_end_date = self.instance.end_date

            if start_date and start_date < plan_start_date:
                raise serializers.ValidationError('start date cannot be preponed')
            if end_date and end_date < plan_end_date:
                raise serializers.ValidationError('end date cannot be preponed')
            if start_date and end_date and start_date >= end_date:
                raise serializers.ValidationError('conflicting dates')
            if start_date and start_date >= plan_end_date and not end_date:
                raise serializers.ValidationError('start date after end date')

        return data

    def create(self, validated_data):
        return Plan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class PlanWithUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanWithUserRegistration
        fields = '__all__'

