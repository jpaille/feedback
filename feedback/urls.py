from django.conf.urls import url
from django.contrib import admin
from stats.views import dashboard
from mail_reports.views import test_report_template

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^stats/', dashboard),
    url(r'^test_report_template/', test_report_template)
]
