"""
URL configuration for gamify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

from apps.cart.webhook import webhook
from apps.cart.views import cart_detail, success
from apps.core.views import frontpage, contact, about
from apps.store.views import product_detail, category_detail, search
from apps.store.api import api_add_to_cart, api_remove_from_cart, api_checkout, create_checkout_session, api_library_load, api_install_or_uninstall
from apps.userprofile.views import signup, myaccount, library

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart'),
    path('hooks/', webhook, name='webhook'),
    path('cart/success/', success, name='success'),
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),

    #Authentication
    path('library/', library, name='library'),
    path('myaccount/', myaccount, name='myaccount'),
    path('signup/', signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # API
    path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('api/api_add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/checkout/', api_checkout, name='api_checkout'),
    path('api/api_library_load/', api_library_load, name='api_library_load'),
    path('api/api_install_or_uninstall/', api_install_or_uninstall, name='api_install_or_uninstall'),

    #Store
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:slug>/', category_detail, name='category_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
