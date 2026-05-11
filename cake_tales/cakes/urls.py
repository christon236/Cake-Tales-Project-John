from django.urls import path

from . import views

urlpatterns = [path('',views.HomeView.as_view(),name='home'),
               
               path('add-a-cake/',views.AddACakeView.as_view(),name='add-a-cake'),

               path('cake-details/<str:uuid>/',views.CakeDetailsView.as_view(),name='cake-details'),
               
               path('cake-edit/<str:uuid>/',views.CakeEditView.as_view(),name='cake-edit'),

               path('cake-delete/<str:uuid>/',views.CakeDeleteView.as_view(),name='cake-delete'),

               path('add-to-wishlist/<str:uuid>/',views.AddtoWishList.as_view(),name='add-to-wishlist'),

               path('remove-from-wishlist/<str:uuid>/',views.RemovefromWishList.as_view(),name='remove-from-wishlist'),

               path('wishlist/',views.WishListView.as_view(),name='wishlist'),

               path('add-to-cart/<str:uuid>/',views.AddtoCart.as_view(),name='add-to-cart'),

               path('remove-from-cart/<str:uuid>/',views.RemovefromCart.as_view(),name='remove-from-cart'),

               path('checkout/',views.CheckoutView.as_view(),name='checkout'),
               
               path('place-order/<str:uuid>/',views.OrderPlacedView.as_view(),name='place-order'),

               path('orders/',views.OrdersView.as_view(),name='orders'),

               path('order-details/<str:uuid>/',views.OrderDetailsView.as_view(),name='order-details'),

               ]