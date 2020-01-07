from django.contrib import admin

from .models import Program, Procedure, ProcedureDesc, AnalysisTransaction, ProgramComment

admin.site.register(Program)
admin.site.register(ProgramComment)
admin.site.register(Procedure)
admin.site.register(ProcedureDesc)


admin.site.register(AnalysisTransaction)
