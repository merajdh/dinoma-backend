from django.urls import path
from userauths import views as userauths_views
from store import views as store_views


from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('user/token/' , userauths_views.MyTokenObtainView.as_view() , name="token_obtain_pair"),
    path('user/token/refresh/' , TokenRefreshView.as_view(), name="refresh_token"),
    path('user/register/' , userauths_views.RegisterView.as_view() , name="register"),
    path('user/password-reset/<email>/' , userauths_views.PasswordEmailVerify.as_view(), name="password_reset"),
    path('user/password-change/' , userauths_views.PasswordChangeView.as_view() , name="password_change"),

    #store endpoint 
    path("audience/" , store_views.AudienceListAPIView.as_view()),
    path("clothing-type/" , store_views.ClothingTypeListAPIView.as_view() ),
    path("product/" , store_views.ProductListAPIView.as_view() ),
    path("product/<slug>" , store_views.ProductDetailListAPIView.as_view() ),

]

