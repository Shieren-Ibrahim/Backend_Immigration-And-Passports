from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('bookPassport',views.bookPassport ,name='bookPassport'),
	path('bookMovment',views.bookMovment ,name='bookMovment'),
	path('bookAccomodation',views.bookAccomodation ,name='bookAccomodation'),
	#path('four_page',views.four_page ,name='four_page'),
	#path('services',views.services ,name='services'),
	#path('profile',views.profile ,name='profile'),
	path('forgettenPassword',views.forgetten_password ,name='forgettenPassword'),
	path('confirmationOfReservation',views.confirmationOfReservation ,name='confirmationOfReservation'),
	path('confirmationOfReservationMR',views.confirmationOfReservationMR ,name='confirmationOfReservationMR'),
	path('confirmationOfReservationAB',views.confirmationOfReservationAB ,name='confirmationOfReservationAB'),
	path('cancellationOFResevation',views.cancellationOFResevation ,name='cancellationOFResevation'),
	path('cancellationOFResevationMR',views.cancellationOFResevationMR ,name='cancellationOFResevationMR'),
	#path('notification',views.notification ,name='notification'),
	path('cancellationOFResevationAB',views.cancellationOFResevationAB ,name='cancellationOFResevationAB'),
 	path('confirm_staying',views.confirm_staying ,name='confirm_staying'),
	path('confirm_moving',views.confirm_moving ,name='confirm_moving'),
	path('confirm_passport',views.confirm_passport ,name='confirm_passport'),
 	path('paper',views.paper ,name='paper'),
 	#path('paperMoving',views.paperMoving ,name='paperMoving'),
 	#path('paperStaying',views.paperStaying ,name='paperStaying'),
	
]

