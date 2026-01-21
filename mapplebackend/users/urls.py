from django.urls import path
from .views import RegisterApiView, LoginApiView, MeAPIView, AdminUserListView, AdminUserDetailsList, AdminUserBlockView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    # path('login/', LoginApiView.as_view()),
    path('login/', LoginApiView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeAPIView.as_view()),
    
    path('admin/users/', AdminUserListView.as_view()),
    path('admin/users/<int:pk>/', AdminUserDetailsList.as_view()),
    path('admin/users/<int:pk>/block/', AdminUserBlockView.as_view()),
]
