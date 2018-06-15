from django.conf.urls import url
from bookportal import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^books/(?P<id>[0-9]+)/$', views.book_details, name='book_details'),
    # url(r'^my_gigs/$', views.my_gigs, name='my_gigs'),
    # url(r'^create_gig/$', views.create_gig, name='create_gig'),
    # url(r'^edit_gig/(?P<id>[0-9]+)/$', views.edit_gig, name='edit_gig'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^checkout/$', views.create_purchase, name='create_purchase'),
    url(r'^view_pdf/(?P<id>[0-9]+)/$', views.pdf_view, name='pdf_view'),
    # url(r'^my_sellings/$', views.my_sellings, name='my_sellings'),
    url(r'^my_buyings/$', views.my_buyings, name='my_buyings'),
    # url(r'^category/(?P<link>[\w|-]+)/$', views.category, name='category'),
    url(r'^search/$', views.search, name='search'),
]
