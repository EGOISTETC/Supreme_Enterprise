from django.urls import path
from analyticapi.views import *

urlpatterns = [
    path('', allviews.redirect_main),
    path('go_to_reg', allviews.redirect_registration),
    path('go_to_auth', allviews.redirect_authorization, name='go_to_auth'),
    path('reg', register.reg, name='register'),
    path('auth', LoginView.auth, name='auth'),
    path('redirect_services', allviews.redirect_services),
    path('pay', allviews.redirect_pay),
    path('cabinet', allviews.redirect_cabinet,name='cabinet'),
    path('analytics/', AnalyticsView.get_analytics, name='analytics'),
    path('update_analytics/', allviews.update_analytics, name='update_analytics'),
    path('stat', allviews.redirect_stat, name='stat'),
    path('logout', allviews.logout, name='logout'),
]



