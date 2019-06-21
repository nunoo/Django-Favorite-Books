from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books$', views.books),
    url(r'^$', views.index),
    url(r'^register$', views.addUserToDB),
    url(r'^login$', views.loginUserToDB),
    url(r'^logout$', views.logout),
    url(r'^addbook$', views.addbook),
    url(r'^books/(?P<bookid>\d+)', views.book_click),
    url(r'^unlike/(?P<bookid>\d+)$', views.unlike_book),
    url(r'^like/(?P<bookid>\d+)$', views.like_book),
    url(r'^delete/(?P<bookid>\d+)$', views.delete_book),
    url(r'^editbook/(?P<bookid>\d+)$', views.edit_book),
   
    
]
