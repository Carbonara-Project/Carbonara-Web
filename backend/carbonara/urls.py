from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view
#from rest_framework.documentation import include_docs_urls
from sqlapp.sqlapp import execute_sql
from api.views import Index

schema_view = get_swagger_view(title='Carbonara API')

urlpatterns = [
    url(r'^$', Index.as_view()),
    url(r'^admin/sqlapp/(?:sql/)?$', execute_sql, name='sql'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^users/', include('users.urls')),
    #url(r'^docs/', include_docs_urls(title='Carbonara API', public=False)),
    url(r'^documentation/', schema_view),
]
