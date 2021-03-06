from django.conf.urls import url
from . import views

app_name = 'analyze'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^myfiles/$', views.my_files, name='myfiles'),
    url(r'^myfiles/(?P<slug>.*)/$', views.file_details, name='filedetails'),
    url(r'^myfiles/download/(?P<path>.*)/$', views.download, name='download'),
    url(r'^superuserden/$', views.superuser_den, name='superuser_den'),
    url(r'^edit/myfiles/(?P<slug>.*)', views.edit_file, name='edit_file'),
    url(r'^myfiles/(?P<filepath>.*)/printdoc/$', views.print_file, name='print_file'),
    url(r'^add-to-review/myfiles/(?P<slug>.*)/$', views.add_to_review, name='add_to_review'),
    url(r'^remove-from-review/myfiles/(?P<slug>.*)/', views.remove_from_review, name='remove_from_review'),
    url(r'^review-list/$', views.review_list, name='review_list'),
    url(r'^delete/myfiles/(?P<slug>.*)/$', views.delete_file, name='delete_file'),
    url(r'^create-compare-group/$', views.create_compare_group, name='create_compare_group'),
    url(r'^comparelist/$', views.comparelist, name='comparelist'),
    url(r'^getresults/(?P<id>\d+)/$', views.get_results, name='get_results'),
    url(r'^edit/comparelist/(?P<id>\d+)/$', views.edit_compare_list, name='edit_compare_list'),
    url(r'^delete/comparelist/(?P<id>\d+)/$', views.delete_compare_list, name='delete_compare_list'),
]
