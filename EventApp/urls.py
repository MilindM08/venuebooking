from.import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('viewDetails/<int:vid>/', views.viewDetails, name='viewDetails'),
    path('viewVenue/', views.viewVenue, name='viewVenue'),
    path('book_venue/<int:vid>/', views.book_venue, name='book_venue'),
    path('makePayment/', views.makePayment, name='makePayment'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('rating/<int:vid>/',views.rating, name='rating'),
    
    


]
