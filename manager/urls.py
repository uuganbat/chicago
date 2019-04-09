from app import Nurl

urlpatterns = [
	Nurl(r'^dashboard/$') > 'manager.views.DashBoard',
]