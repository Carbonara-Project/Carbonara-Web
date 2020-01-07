from rest_framework import serializers
from .models import *

import logging
import base64
import zlib

logger = logging.getLogger(__name__)

# TODO: Exclude models id field from all serializers

class MinHashSecurityViolation(RuntimeError):
    pass

# Analysis
class ProgramSerializer(serializers.ModelSerializer):
    """ 
    Serializer of the Program model

    Note:
    md5 ans sha256 are redifined otherwise if already
    in the DB, the unique constraint would return an error
    before returning the already existing instace
    """
    md5 = serializers.CharField()
    sha256 = serializers.CharField()

    class Meta:
        model = Program
        exclude = tuple()

    def create(self, validated_data):
        return Program.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Program's update deprecated
        return instance

class ProgramCommentSerializer(serializers.ModelSerializer):
    """
    Serializer of the ProgramComment model
    """
    user = serializers.CharField()

    class Meta:
        model = ProgramComment
        exclude = tuple()
    
    def create(self, validated_data):
        return ProgramComment.objects.create(**validated_data)

class ProgramInfoSerializer(serializers.ModelSerializer):
    """ Serializer of the Procedure model """

    class Meta:
        model = ProgramInfo
        exclude = ('id', 'program', 'user')
        #fields = ('filename', 'bits', 'arch', 'program_class', 'endian', 'entropy')

    def create(self, validated_data):
        """
        Returns the Info model
        """
        return ProgramInfo.objects.create(**validated_data)

class ImportSerializer(serializers.ModelSerializer):
    """ Serializer of the Import model """

    class Meta:
        model = Import
        exclude = ('programinfo',)

    def create(self, validated_data, *args, **kwargs):
        """
        Returns the Info model
        """
        return Import.objects.create(**validated_data)

class ProcedureDescSerializer(serializers.ModelSerializer):
    """ Serializer of the ProcedureDesc model """
    user = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    vex_hash = serializers.CharField(write_only=True)
    flow_hash = serializers.CharField(write_only=True)
    
    raw = serializers.CharField(write_only=True)

    class ASMField(serializers.Field):
        
        def to_representation(self, obj):
            # FIXME: Due to the error in the function below
            return obj.decode('utf-8')
            # return zlib.decompress(obj)

        def to_internal_value(self, data):
            # FIXME: zlib.error: Error -3 while decompressing data: incorrect header check
            # TODO: Nedded since the method is called twice, once with data received
            # from the report (string) and once with zlib encoded bytes
            if type(data) is bytes:
                return data
            return data.encode('utf-8')
            # return zlib.compress(data.encode('utf-8'))

    asm = ASMField()

    class Meta:
        model = ProcedureDesc
        # TODO: Removed apicalls for developing purpose only, needed to create model in DB for this
        exclude = ('procedure', 'apicalls') #apicalls = string
        read_only_fields = ('description', )

    def create(self, validated_data):
        raw = zlib.compress(base64.b64decode(validated_data.pop("raw")))
        
        # minhash security checks
        vex_hash = validated_data['vex_hash']
        if not vex_hash.startswith("010000000000000040000000"):
            raise MinHashSecurityViolation()
        flow_hash = validated_data['flow_hash']
        if not flow_hash.startswith("010000000000000020000000"):
            raise MinHashSecurityViolation()
        
        instance = ProcedureDesc.objects.create(**validated_data, raw=raw)
        
        self.context.get("insert_dict")[instance.id] = bytes.fromhex(vex_hash)
        
        return instance

    def update(self, instance, validated_data):
        # minhash security checks
        vex_hash = validated_data['vex_hash']
        if not vex_hash.startswith("010000000000000040000000"):
            raise MinHashSecurityViolation()
        flow_hash = validated_data['flow_hash']
        if not flow_hash.startswith("010000000000000020000000"):
            raise MinHashSecurityViolation()
        
        if instance.vex_hash != validated_data['vex_hash']:
            self.context.get("update_dict")[instance.id] = (bytes.fromhex(instance.vex_hash), bytes.fromhex(validated_data['vex_hash']))
        
        validated_data["raw"] = zlib.compress(base64.b64decode(validated_data["raw"]))
        
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        upvotes =  ProcedureDescUpvote.objects.filter(procedure_desc=instance)
        downvotes =  ProcedureDescDownvote.objects.filter(procedure_desc=instance)
        res['upvotes'] = upvotes.count()
        res['downvotes'] = downvotes.count()
        
        req_user = self.context['req_user']
        res['ownVote'] = ''
        if upvotes.filter(user=req_user).first() is not None:
            res['ownVote'] = 'upvote'
        elif downvotes.filter(user=req_user).first() is not None:
            res['ownVote'] = 'downvote'
        return res


class ProcedureSerializer(serializers.ModelSerializer):
    """ Serializer of the Procedure model """
    proc_desc = ProcedureDescSerializer(write_only=True)

    class Meta:
        model = Procedure
        exclude = ('id', 'program')

    def create(self, validated_data):
        """
        Create a Procedure model 
        """
        proc_desc_json = validated_data.pop('proc_desc')
        user = validated_data.pop('user')
        off = validated_data.pop('offset')
        prog = validated_data.pop('program')
        
        procedure = Procedure.objects.filter(
            offset=off,
            program=prog
        ).first()
        if procedure is None:
            procedure = Procedure.objects.create(
                program=prog,
                offset=off
            )
        # If a ProcedureDesc of a certain Procedure has been already uploaded by a user
        # it will be updated instead of creating a new one
        proc_desc = ProcedureDesc.objects.filter(procedure=procedure, user=user).first()
        proc_desc_serializer = ProcedureDescSerializer(
            proc_desc,
            data=proc_desc_json,
            context=self.context
        )
        if not proc_desc_serializer.is_valid():
            raise Exception('Invalid proc_desc_json {}'.format(proc_desc_serializer.errors))
            
        proc_desc_serializer.save(procedure=procedure, user=user)
        return procedure

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # TODO: The procedure desc selection should be implemented
        procedureDesc = instance.proceduredesc_set.first()
        # TODO: Could this happen ?
        if procedureDesc is None: 
            return None
        ret['name_proc'] = procedureDesc.name
        return ret
    
class ExportsSerializer(serializers.ModelSerializer):
    """
    Serializer for Exports model
    """
    class Meta:
        model = Exports
        exclude =  ('programinfo',)

class SectionsSerializer(serializers.ModelSerializer):
    """
    Serializer for Sections model
    """
    name = serializers.CharField(allow_blank=True)

    class Meta:
        model = Sections
        exclude =  ('programinfo',)

    def create(self, validated_data):
        return Sections.objects.create(**validated_data)

class LibsSerializer(serializers.ModelSerializer):
    """
    Serializer for Libs model
    """

    class Meta:
        model = Libs
        exclude = ('programinfo',)

class StringsSerializer(serializers.ModelSerializer):
    """
    Serializer for Strings model
    """
    class Meta:
        model =  Strings
        exclude = ('programinfo',)

    def create(self, validated_data):
        return Strings.objects.create(**validated_data)

class ProcsReportSerializer(serializers.Serializer):
    md5 = serializers.CharField()
    procs = ProcedureSerializer(many=True)
    
    def create(self, validated_data):
        """ Stores, models found in a procedures only report attaching it to a program """
        user = validated_data.pop('user')
        md5 = validated_data.pop('md5')
        program = Program.objects.get(md5=md5)
        
        # The Procedure json contains also the ProcedureDesc json
        procs_serializer = ProcedureSerializer(
            data=validated_data.pop('procs'),
            many=True,
            context=self.context
        )
        if procs_serializer.is_valid():
            procs_serializer.save(program=program, user=user)
        # print("[+] Procs parsed")

        return program
    
class ReportSerializer(serializers.Serializer):
    info = ProgramInfoSerializer()
    exports = ExportsSerializer(many=True)
    imports = ImportSerializer(many=True)
    program = ProgramSerializer()
    libs = LibsSerializer(many=True)
    sections = SectionsSerializer(many=True)
    strings = StringsSerializer(many=True)
    procs = ProcedureSerializer(many=True)

    def create(self, validated_data):
        """ Stores, models found in a full report attaching it to a program """
        user = validated_data.pop('user')

        program_json = validated_data.pop('program')
        program = Program.objects.filter(md5=program_json['md5']).first()
        program_serializer = ProgramSerializer(program, data=program_json)
        if program_serializer.is_valid():
            program = program_serializer.save()
        # print("[+] Program parsed")

        programinfo = ProgramInfo.objects.filter(program=program, user=user).first()
        program_info_serializer = ProgramInfoSerializer(programinfo, data=validated_data.pop('info'))
        if program_info_serializer.is_valid():
            programinfo = program_info_serializer.save(program=program, user=user)
        # print("[+] ProgramInfo parsed")
        
        imports_serializer = ImportSerializer(
            data=validated_data.pop('imports'), 
            many=True
        )
        if imports_serializer.is_valid():
            imports_serializer.save(programinfo=programinfo)
        # print("[+] Imports parsed")

        exports_serializer = ExportsSerializer(
            data=validated_data.pop('exports'), 
            many=True
        )
        if exports_serializer.is_valid():
            exports_serializer.save(programinfo=programinfo)
        # print("[+] Exports parsed")

        sections_serializer = SectionsSerializer(
            data=validated_data.pop("sections"),
            many=True
        )
        if sections_serializer.is_valid():
            sections_list = sections_serializer.save(programinfo=programinfo)
        # print("[+] Sections parsed")
        
        libs_serializer = LibsSerializer(
            data=validated_data.pop("libs"),
            many=True
        )
        if libs_serializer.is_valid():
            libs_serializer.save(programinfo=programinfo)
        # print("[+] Libs parsed")

        # print('[*] Parsing {} strings'.format(len(validated_data.get('strings'))))
        strings_serializer = StringsSerializer(
            data=validated_data.pop("strings"),
            many=True
        )
        if strings_serializer.is_valid():
            strings_serializer.save(programinfo=programinfo)
        # print("[+] Strings parsed")

        # The Procedure json contains also the ProcedureDesc json
        procs_serializer = ProcedureSerializer(
            data=validated_data.pop('procs'),
            many=True,
            context=self.context
        )
        if procs_serializer.is_valid():
            procs_serializer.save(program=program, user=user)
        # print("[+] Procs parsed")

        print('[+] Finished parsing report')
        return program

class AnalysisTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for AnalysisTransaction model
    """
    
    class Meta:
        model = AnalysisTransaction
        exclude = ('id', 'user')

# Social
class ProcedureDescCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = ProcedureDescComment
        exclude = ('id', )
