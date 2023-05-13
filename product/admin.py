from django.contrib import admin

# Register your models here.
from .models import Product,Category,PlanDates,Month,PlanName



@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="p")


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","status"]
    ordering = ["name"]
    actions = [make_published]

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(PlanDates)
admin.site.register(Month)
admin.site.register(PlanName)