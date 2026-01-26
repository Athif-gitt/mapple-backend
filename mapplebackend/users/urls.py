from django.urls import path
from .views import RegisterApiView, LoginApiView, MeAPIView, AdminUserListView, AdminUserDetailsList, AdminUserBlockView, ProfileDashboardView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import google_login_success

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    # path('login/', LoginApiView.as_view()),
    path('login/', LoginApiView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeAPIView.as_view()),
    
    path('admin/users/', AdminUserListView.as_view()),
    path('admin/users/<int:pk>/', AdminUserDetailsList.as_view()),
    path('admin/users/<int:pk>/block/', AdminUserBlockView.as_view()),
    path("google/success/", google_login_success),

    
    path("profile/dashboard/", ProfileDashboardView.as_view())
]
