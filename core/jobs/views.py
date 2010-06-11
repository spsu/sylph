from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from sylph.utils.jobs import process_n_messages, process_n_messages_pool

from datetime import datetime
import hashlib


# ============ Jobs Index =================================

def index(request):
	# TODO
	pass


# ============ Run Jobs: VIA CRON! ========================

def run_jobs(request):

	process_n_messages_pool()

	return HttpResponse("Jobs Run", mimetype='text/plain')


# ============ Edit Job ===================================

def edit_job(request, job_id):
	# TODO
	pass


# ============ View Job ===================================

def view_job(request, job_id):
	# TODO
	pass

