from django.urls import path
from txs.api.views import CompanyView, abstract, monthAbstract

# register the urls
urlpatterns = [
    path('companies/', CompanyView.as_view(), name='companies-list'),
    path('companies/<id>/', CompanyView.as_view(), name='companies-detail'),
    path('abstract/', abstract, name='abstract'),
    path('month-abstract/', monthAbstract, name='month-abstract'),
]