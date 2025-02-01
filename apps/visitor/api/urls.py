from django.urls import path
from .views import CustomTokenObtainPairView, SignupStep1, SignupStep2
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupStep1.as_view(), name='signup'),
    path('signup/education/', SignupStep2.as_view(), name='signup_education'),
]
