from django.urls import path, include
from apps.marketplace.views import MarketPlaceAddView, MarketPlaceView, MarketPlaceDetailView
urlpatterns = [
    path('', MarketPlaceView.as_view(), name='marketplace'),
    path('add/', MarketPlaceAddView.as_view(), name='marketplace_add'),
    path('<slug:slug>/', MarketPlaceDetailView.as_view(), name='marketplace_detail'),

]
