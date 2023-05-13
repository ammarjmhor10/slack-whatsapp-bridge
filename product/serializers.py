from rest_framework import serializers

from .models import Category, Product,Month,PlanDates,PlanName

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "products",
        )


class PlanDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDates
        fields = (
            'dates',
            'price'
        )

class PlanNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanName
        fields = (
            'plan',
        )
class MonthSerializer(serializers.ModelSerializer):
    plan_dates = PlanDatesSerializer(many=True)
    plan_name = PlanNameSerializer(plan_dates)

    class Meta:
        model = Month
        fields = (
            'plan_dates',
            'plan_name',
            'footer',
        )