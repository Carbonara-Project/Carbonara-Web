from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from .views import *

urlpatterns = [
  url(r'^report/$', ReportView.as_view(), name='report'),
  url(r'^procs-report/$', ProcsReportView.as_view(), name='procs-report'),
  url(r'^hidden-report', HiddenReportView.as_view(), name='hidden-report'),
  url(r'^hidden-procs-report/$', HiddenProcsReportView.as_view(), name='hidden-procs-report'),
  
  url(r'^program/$', ProgramView.as_view(), name='program-view'),
  url(r'^program/(?P<md5>[a-fA-f\d]{32})/comments/$', ProgramCommentView.as_view(), name='program-comment-views'),
  url(r'^blob/$', BlobView.as_view(), name='blob-view'),
  url(r'^procedure/$', ProcedureView.as_view(), name='procedure-view'),
  url(r'^procedure/(?P<procedure_desc_id>[0-9]+)/vote/$', ProcedureDescVoteView.as_view(), name='procdesc-vote-view'),
  url(r'^proc-similar/$',SimilarView.as_view(),name='proc-similar'),
  url(r'^simprocs/$',SimProcsView.as_view(),name='simprocs'),

  url(r'^comment/$', ProcedureDescCommentView.as_view(), name='comment-view'),
  url(r'^comment/(?P<procedure_desc_comment_id>[0-9]+)/vote/$', ProcedureDescCommentVoteView.as_view(), name='comment-vote-view')  
]
