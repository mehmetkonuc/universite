from django.urls import path, include
from apps.marketplace.views import MarketPlaceAddView, MarketPlaceView, MarketPlaceDetailsView, MarketPlaceEditView, delete_marketplace, MyMarketPlaceView, DraftMarketPlaceView
urlpatterns = [
    path('', MarketPlaceView.as_view(), name='marketplace'),
    path('my/', MyMarketPlaceView.as_view(), name='my_marketplace'),
    path('draft/', DraftMarketPlaceView.as_view(), name='my_draft_marketplace'),
    path('add/', MarketPlaceAddView.as_view(), name='marketplace_add'),
    path('<slug:slug>/', MarketPlaceDetailsView.as_view(), name='marketplace_details'),
    path('edit/<slug:slug>/', MarketPlaceEditView.as_view(), name='marketplace_edit'),
    path('delete/<int:marketplace_id>/', delete_marketplace, name='marketplace_delete'),

]
