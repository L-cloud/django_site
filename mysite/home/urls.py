from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('', views.MainView.as_view(), name = 'homepage'),
    path('report/<int:pk>', views.Pdfview.as_view(), name = 'pdf'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/$', views.Certification.as_view(), name='activate'),
    path('accounts/signup/registration/success_sigh_up/<email>',views.SuccessSignUp.as_view(),name='success_sigh_up'),
    path('activate/emailvalidation', views.EmailvalidationView.as_view(), name = 'emailvalidation'),
    path('AddFavoriteView/<int:pk>', views.AddFavoriteView.as_view(), name = 'addFavorite'),
    path('DeleteFavoriteView/<int:pk>', views.DeleteFavoriteView.as_view(), name = 'deleteFavorite'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.Certification.as_view(), name='activate'),
]
    # ... the rest of your URLconf goes here ...


