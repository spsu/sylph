from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.jobs.views',
	(r'^/$', 'index'),
	(r'run/$', 'run_jobs'),
	(r'view/(?P<job_id>\d+)/$', 'view_job'),
)
