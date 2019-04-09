from django.shortcuts import render

from app import views as v
# Create your views here.

class DashBoard(v.LoginRequired, v.TemplateView):
	pass
