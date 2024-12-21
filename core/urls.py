"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', RegistrationApiView.as_view()),
    path('auth', AuthApiView.as_view()),
    path('profile', ProfileApiView.as_view()),
    path('area', AreaApiView.as_view()),
    path('lot', LotApiView.as_view()),
    path('part', ParticipantApiView.as_view()),
    path('bid', BidApiView.as_view()),
    path('lot_search', LotSearchApiView.as_view()),
    path('lot_order', LotOrderApiView.as_view()),
    path('currency_rates/', CurrencyRatesView.as_view(), name='currency-rates'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
