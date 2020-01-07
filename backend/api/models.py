import datetime

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from binaryfield import BinaryField

class PositiveBigIntegerField(models.BigIntegerField):
    description = "Positive Big integer"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': models.BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)

    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'bigint UNSIGNED'
        return super(PositiveBigIntegerField, self).db_type(connection)


class Program(models.Model):
    sha256 = models.CharField(unique=True, max_length=64, validators=[MinLengthValidator(64)], db_index=True)
    md5 = models.CharField(max_length=32, validators=[MinLengthValidator(32)], primary_key=True)

    def __str__(self):
        return 'md5: {}'\
                .format(self.md5)

class ProgramInfo(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    filename = models.TextField()

    bits = models.PositiveSmallIntegerField()
    arch = models.TextField()
    program_class = models.TextField(blank=True, null=True)
    endian = models.TextField()
    
    '''
    static properties about the file that cannot be defined by the user, like strings hash,
    must be placed in the Program model in order to save space in the db
    '''
    entropy = models.IntegerField() #consider moving to program
    
    def __str__(self):
        return 'Program: {}, \
                Name: {}, \
                Arch: {}, \
                Program_class: {}, \
                Endian: {}'\
                .format(self.program, self.filename, self.arch, self.program_class, self.endian)

class ProgramComment(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ('program', 'user')


class Procedure(models.Model):
    program = models.ForeignKey(Program)
    offset = PositiveBigIntegerField()

    class Meta:
        unique_together = ('offset','program')

class ProcedureDesc(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    # must start with "010000000000000040000000" (seed+num_perm)
    vex_hash = models.CharField(max_length=536, validators=[MinLengthValidator(536)]) #TODO use BinaryField
    # must start with "010000000000000020000000" (seed+num_perm)
    flow_hash = models.CharField(max_length=280, validators=[MinLengthValidator(280)]) #TODO use BinaryField
    
    raw = models.BinaryField()
    raw_len = models.IntegerField()
    name = models.TextField()  
    callconv = models.TextField(null=True) 
    apicalls = models.TextField() 
    asm = models.BinaryField()

    class Meta:
        unique_together = ('procedure', 'user')

class Exports(models.Model):
    programinfo = models.ForeignKey(ProgramInfo, on_delete=models.CASCADE)
    
    size = PositiveBigIntegerField() 
    name = models.TextField()
    offset = PositiveBigIntegerField()

class Import(models.Model):
    programinfo = models.ForeignKey(ProgramInfo, on_delete=models.CASCADE)
    
    name = models.TextField()
    addr = PositiveBigIntegerField()

class Libs(models.Model):
    programinfo = models.ForeignKey(ProgramInfo, on_delete=models.CASCADE)
    
    name = models.TextField()

class Sections(models.Model):
    programinfo = models.ForeignKey(ProgramInfo, on_delete=models.CASCADE)
    
    size = PositiveBigIntegerField() 
    name = models.TextField(null=True)
    md5 = models.CharField(max_length=32, validators=[MinLengthValidator(32)]) 
    offset = PositiveBigIntegerField()

class Strings(models.Model):
    programinfo = models.ForeignKey(ProgramInfo, on_delete=models.CASCADE)
     
    size = PositiveBigIntegerField()
    encoding = models.TextField()
    val = models.TextField()
    offset = PositiveBigIntegerField()

class ProcedureComment(models.Model):
    procedureDesc = models.ForeignKey(ProcedureDesc, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()

class AnalysisTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=256)
    md5 = models.CharField(max_length=32, validators=[MinLengthValidator(32)])

    completed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    def __str__(self):
        return '<User:{}, Id: {}'.format(self.user, self.id)
    
class ProcedureDescComment(models.Model):
    procedure_desc = models.ForeignKey(ProcedureDesc, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField()

class ProcedureDescCommentVote(models.Model):
    user = models.ForeignKey(User)
    procedure_desc_comment = models.ForeignKey(ProcedureDescComment)

    class Meta:
        abstract = True

class ProcedureDescCommentUpvote(ProcedureDescCommentVote):
    pass

class ProcedureDescCommentDownvote(ProcedureDescCommentVote):
    pass

class ProcedureDescVote(models.Model):
    user = models.ForeignKey(User)
    procedure_desc = models.ForeignKey(ProcedureDesc)
    
    class Meta:
        abstract = True

class ProcedureDescUpvote(ProcedureDescVote):
    pass

class ProcedureDescDownvote(ProcedureDescVote):
    pass
    
