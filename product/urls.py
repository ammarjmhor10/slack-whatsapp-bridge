from django.urls import path,include


from product import views

urlpatterns = [
    path('latest-products/',views.LatestProductsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/',views.ProductDetail.as_view()),
    path('categories/',views.CategoryList.as_view()),
    path('months/',views.MonthList.as_view())
]