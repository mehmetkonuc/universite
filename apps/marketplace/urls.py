from django.urls import path, include
from apps.marketplace.views import MarketPlaceAddView, MarketPlaceView
urlpatterns = [
    path('', MarketPlaceView.as_view(), name='marketplace'),
    path('add', MarketPlaceAddView.as_view(), name='marketplace_add'),
]
