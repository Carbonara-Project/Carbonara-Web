import requests
import json
import asyncio
import os
import logging

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from pubnub.pubnub import PubNub

from .serializers import *
from .models import *
from .client import upload_binary, SECRET, FILES_SRV
from .amqp_sender import SenderAMQP
from .decoders import parse_report_file
from .simprocs import insert, query_id

from users.models import VoteNotification
from users.serializers import VoteNotificationSerializer

logger = logging.getLogger('django')

# Constants
ANALYSIS_SERVERS_NUM = 8
COMMENTS_PER_PAGE = 10

class Index(APIView):
    permission_classes = ()

    def get(self, req):
        return render(req, 'index.html')

class ReportView(APIView):
    """
    Endpoint responsible for the handling of an upload of a Binary-Report couple
    This action is carried out by the CLI (Guanciale)
    """
    parser_classes = (MultiPartParser, )

    def post(self, req):
        # TODO: Forward CodeBytes to ML Server
        binary = req.data.get('binary', None)
        if binary is None:
            return Response('Binary must not be null', status=HTTP_400_BAD_REQUEST)
        md5 = upload_binary(binary)
        #TODO check that md5 == report["program"]["md5"]
        
        context = {
            "insert_dict": {},
            "update_dict": {}
        }

        report_file = req.data.get("report", None)
        report = parse_report_file(report_file)
        report_serializer = ReportSerializer(data=report, context=context)
        
        if report_serializer.is_valid():
            
            report_serializer.save(user=req.user)
            
            insert(context["insert_dict"], context["update_dict"])
            
            return Response(report_serializer.errors, status=HTTP_200_OK)
        # insert report in db and delete transaction
        return Response(report_serializer.errors, status=HTTP_400_BAD_REQUEST)

class HiddenReportView(APIView):
    """
    Endpoint responsible for the handling of an upload of a Report from the Cluster Analysis
    """
    parser_classes = (MultiPartParser, )
    permission_classes = tuple()

    def post(self, req):
        logger.info(str(req.data))
        if req.query_params.get("key", None) != SECRET:
            return Response('Not found', status=HTTP_404_NOT_FOUND)

        transaction_id = req.data.get('transaction-id', None)
        # TODO: Consider if putting this in a try/catch but it's pretty impossible 
        # an invalid id is returned
        transaction_id = int(transaction_id)
        transaction = AnalysisTransaction.objects.filter(id=transaction_id).first()
        # TODO: if transaction is null this must be logged and an error response should
        # be returned

        error = req.data.get("error", None)
        if error is not None:
            transaction.completed = True
            transaction.failed = True
            transaction.save()
        else:
            context = {
                "insert_dict": {},
                "update_dict": {}
            }
            
            report_file = req.data.get("report", None)
            report = parse_report_file(report_file)
            report_serializer = ReportSerializer(data=report, context=context)

            if report_serializer.is_valid():
                # TODO: Send error to frontend, however this should be higly unlikely
                report_serializer.save(user=transaction.user)
                
                insert(context["insert_dict"], context["update_dict"])
                
                transaction.completed = True
                transaction.failed = False
                transaction.save()
            else:
                transaction.completed = True
                transaction.failed = True
                transaction.save()
        
        # pubnub = PubNub(settings.PNCONFIG)
        # envelope = pubnub.publish().channel('fanti').message('Transaction finished').sync()
        # print(envelope)

        return Response('', status=HTTP_204_NO_CONTENT)

class ProcsReportView(APIView):
    """
    Endpoint responsible for the handling of an upload of a Report couple
    This action is carried out by the CLI (Guanciale)
    """
    parser_classes = (MultiPartParser, )
    
    def post(self, req):
        context = {
            "insert_dict": {},
            "update_dict": {}
        }

        report_file = req.data.get("report", None)
        report = parse_report_file(report_file)
        report_serializer = ProcsReportSerializer(data=report, context=context)
        
        if report_serializer.is_valid():
            
            report_serializer.save(user=req.user)
            
            insert(context["insert_dict"], context["update_dict"])
            
            return Response(report_serializer.errors, status=HTTP_200_OK)
        # insert report in db and delete transaction
        return Response(report_serializer.errors, status=HTTP_400_BAD_REQUEST)

class HiddenProcsReportView(APIView):
    """
    Endpoint responsible for the handling of an upload of a Report couple
    This action is carried out by the Analysis Server
    """
    parser_classes = (MultiPartParser, )
    permission_classes = tuple()
    
    def post(self, req):
        if req.query_params.get("key", None) != SECRET:
            return Response('Not found', status=HTTP_404_NOT_FOUND)
        
        context = {
            "insert_dict": {},
            "update_dict": {}
        }
        
        transaction_id = req.data.get('transaction-id', None)
        # TODO: Consider if putting this in a try/catch but it's pretty impossible 
        # an invalid id is returned
        transaction_id = int(transaction_id)
        transaction = AnalysisTransaction.objects.filter(id=transaction_id).first()
        # TODO: if transaction is null this must be logged and an error response should
        # be returned
        
        report_file = req.data.get("report", None)
        report = parse_report_file(report_file)
        report_serializer = ProcsReportSerializer(data=report, context=context)
        
        if report_serializer.is_valid():
            
            report_serializer.save(user=transaction.user)
            
            insert(context["insert_dict"], context["update_dict"])
            
            return Response(report_serializer.errors, status=HTTP_200_OK)
        # insert report in db and delete transaction
        return Response(report_serializer.errors, status=HTTP_400_BAD_REQUEST)

# TODO: Better struct Program endpoints
class ProgramView(APIView):
    """
    View of the Program model
    PUT: in charge of the submission of files through website
    """
    # FIXME: Remove zero-permission classes
    parser_classes = (MultiPartParser, FormParser)
    
    def head(self, req):
        md5 = req.query_params.get('md5', None)
        if md5 is None:
            return Response('You must provide md5 for the search', status=HTTP_400_BAD_REQUEST)
        get_object_or_404(Program, md5=md5.lower())
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, req):
        binary = req.data.get('binary', None)
        if binary is None:
            return Response('Binary must not be null', status=HTTP_400_BAD_REQUEST)
        # TODO: Check if there is a more correct way to get the name of the file 
        # and if the name is never None (so at least an empty string)

        db = req.data.get("db", None)
        # TODO: Consider to put the upload of the file to the fileserver in bg
        md5 = upload_binary(binary)
        
        filename = binary._name if binary is not None else md5
        print(filename)
        
        # FIXME: Replace with req.user
        # TODO rollback transaction when something go wrong
        transaction = AnalysisTransaction.objects.create(
            user=req.user,
            filename=filename,
            md5=md5
        )
        
        ######## wake up analysis cluster ########
        def analysis_head(i):
            try:
                requests.head("https://carbonara-analysis-" + str(i) + ".herokuapp.com/", timeout=10)
            except:
                pass
        
        loop = asyncio.new_event_loop()
        async def wakeup():
            futures = [
                loop.run_in_executor(
                    None, 
                    analysis_head, 
                    i
                )
                for i in range(ANALYSIS_SERVERS_NUM)
            ]
            for response in await asyncio.gather(*futures):
                pass
        loop.run_until_complete(wakeup())
        ###########################################
        
        snd = SenderAMQP()
        furl = FILES_SRV + "/file/" + md5 + "?key=" + SECRET
        if db:
            snd.send_task(transaction.id, filename, furl, "", "", db.file.read(), db._name)
        else:
            snd.send_task(transaction.id, filename, furl)
        
        return Response('Binary uploaded', status=HTTP_200_OK)

    def get(self, req):
        # TODO: Every feature should be divided under different URLs
        type = req.query_params.get('type', None)
        if type is None:
            return Response('You must specify the the type of the request', status=HTTP_400_BAD_REQUEST)

        if type == 'info':
            md5 = req.query_params.get('md5', None)
            if md5 is None:
                return Response('You must specify the md5 of the program', status=HTTP_400_BAD_REQUEST)
            program = get_object_or_404(Program, md5=md5)
            # TODO: Paginate the results
            progInfo = ProgramInfo.objects.filter(program=program).all()
            progProcs = Procedure.objects.filter(program=program).all()
            res = {
                'info': ProgramInfoSerializer(progInfo, many=True).data,
                'procs': ProcedureSerializer(progProcs, many=True).data,
            }
            return Response(res, status=HTTP_200_OK)
        
        if type == 'search':
            # TODO: Different query by method should be supported
            query = req.query_params.get('query', None)
            by = req.query_params.get('by', None)
            # TODO: Handle error in case it's none as above
            if by == 'md5':
                progs = Program.objects.filter(md5__startswith=query.lower()).all()
                res = ProgramSerializer(progs[:4], many=True).data
            elif by == 'name':
                progs = ProgramInfo.objects.filter(filename__startswith=query).all()
                progs = progs[:4]
                res = []
                for i in enumerate(progs):
                    md5 = i[1].program.md5
                    name = i[1].filename
                    #res['md5'] = md5
                    #res['filename'] = name
                    res.append({'md5': md5, 'filename': name})
            return Response(res, status=HTTP_200_OK)

class ProgramCommentView(APIView):

    def post(self, req, md5):
        text =  req.data.get('text', None)
        # TODO: return error if none
        program = get_object_or_404(Program, md5=md5)
        comment = ProgramComment.objects.filter(program=program, user=req.user).first()
        if comment is None:
            comment = ProgramComment.objects.create(
                program=program,
                user=req.user,
                text=text
            )
        else:
            comment.text = text
            comment.save()
        
        return Response('', status=HTTP_204_NO_CONTENT)


    def get(self, req, md5):
        program = get_object_or_404(Program, md5=md5)
        comments = ProgramComment.objects.filter(program=program).all()
        res = {
            'comments': ProgramCommentSerializer(comments, many=True).data
        }
        return Response(res, status=HTTP_200_OK)

    def delete(self, req, md5):
        program = get_object_or_404(Program, md5=md5)
        comment = get_object_or_404(ProgramComment, program=program, user=req.user)
        comment.delete()
        return Response('', status=HTTP_200_OK)

class BlobView(APIView):
     # FIXME: Remove zero-permission classes
    parser_classes = (MultiPartParser, FormParser)

    def put(self, req):
        arch = req.query_params.get('arch', None)
        bits = req.query_params.get('bits', None)
        if arch == None or bits == None:
            return Response('Arch and bits must be specifed', status=HTTP_400_BAD_REQUEST)
        
        binary = req.data.get('binary', None)
        if binary is None:
            return Response('Binary must not be null', status=HTTP_400_BAD_REQUEST)
        # TODO: Check if there is a more correct way to get the name of the file 
        # and if the name is never None (so at least an empty string)
        
        md5 = upload_binary(binary)
        
        filename = binary._name if binary is not None else md5
        print(filename)
        
        # FIXME: Replace with req.user
        transaction = AnalysisTransaction.objects.create(
            user=req.user,
            filename=filename,
            md5=md5
        )
        
        ######## wake up analysis cluster ########
        def analysis_head(i):
            try:
                requests.head("https://carbonara-analysis-" + str(i) + ".herokuapp.com/", timeout=10)
            except:
                pass
        
        loop = asyncio.new_event_loop()
        async def wakeup():
            futures = [
                loop.run_in_executor(
                    None, 
                    analysis_head, 
                    i
                )
                for i in range(ANALYSIS_SERVERS_NUM)
            ]
            for response in await asyncio.gather(*futures):
                pass
        loop.run_until_complete(wakeup())
        ###########################################
        
        snd = SenderAMQP()
        furl = FILES_SRV + "/file/" + md5 + "?key=" + SECRET
        snd.send_task(transaction.id, filename, furl, arch, bits)
        
        return Response('Binary uploaded', status=HTTP_200_OK)

class ProcedureView(APIView):
    # FIXME: Remove zero-permission classes
    permission_classes = ()

    def patch(self, req):
        program_md5 = req.query_params.get('md5', None)
        offset = req.query_params.get('offset', None)
        report_file = req.query_params.get('report', None)
        params = (program_md5, offset, report_file)
        if None in params:
            return Response('Missing parameters', status=HTTP_400_BAD_REQUEST)
        report = parse_report_file(report_file)
        
        program = get_object_or_404(Program, md5=program_md5)
        procedure = get_object_or_404(Procedure, program=program, offset=offset)
        procedure_serializer = ProcedureSerializer(procedure, data=report)
        if not procedure_serializer.is_valid():
            return Response(procedure_serializer.errors, status=HTTP_400_BAD_REQUEST)
        procedure_serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)

    def get(self, req):
        md5 = req.query_params.get('md5', None)
        offset = req.query_params.get('offset', None)

        if md5 is None or offset is None:
            return Response("MD5 or offset not valid", status=HTTP_400_BAD_REQUEST)

        program = get_object_or_404(Program, md5=md5)
        procedure = get_object_or_404(Procedure, program=program, offset=offset)
        procDescs = ProcedureDesc.objects.filter(procedure=procedure).all()
        res = ProcedureDescSerializer(procDescs, many=True, context={'req_user': req.user}).data
        return Response(res, status=HTTP_200_OK)

class ProcedureDescVoteView(APIView):
    
    def get(self, req, procedure_desc_id):
        """
        Given a ProcedureDesc return its number of upvotes and downvotes
        """
        procedure_desc = get_object_or_404(ProcedureDesc, id=procedure_desc_id)

        res = {
            'upvote' : ProcedureDescUpvote.objects.filter(procedure_desc=procedure_desc).count(),
            'downvote' : ProcedureDescDownvote.objects.filter(procedure_desc=procedure_desc).count()
        }
        return Response(res, status=HTTP_200_OK)

    def post(self, req, procedure_desc_id):
        votes_class = {'upvote': ProcedureDescUpvote, 'downvote': ProcedureDescDownvote}
        vote_type = req.data.get('vote_type', None)
        procedure_desc = get_object_or_404(ProcedureDesc, id=procedure_desc_id)

        if vote_type not in votes_class:
            # TODO: Return error and report incident
            pass
        
        # Check if vote is already present and the same request has been issued
        upvote = ProcedureDescUpvote.objects.filter(
            user=req.user,
            procedure_desc=procedure_desc
            ).first()
        if votes_class[vote_type] == ProcedureDescUpvote and upvote is not None:
            # TODO: This should not happen since a user cannot give more than one vote, report incident
            res = {
                'vote_error' : 'User cannot give more than one Upvote'
            }
            #FIXED: is 204 response correct in this case?
            return Response(res, status=HTTP_204_NO_CONTENT)

        downvote = ProcedureDescDownvote.objects.filter(
            user=req.user,
            procedure_desc=procedure_desc
            ).first()
        if votes_class[vote_type] == ProcedureDescDownvote and downvote is not None:
            # TODO: This should not happen since a user cannot give more than one vote, report incident
            res = {
                'vote_error' : 'User cannot give more than one Downvote'
            }
            #FIXED: is 204 response correct in this case?
            return Response(res, status=HTTP_204_NO_CONTENT)
        # If the request is different, but a vote from the user already exists, the previous vote, which 
        # must be different, should be deleted
        if upvote is not None:
            upvote.delete()
        if downvote is not None:
            downvote.delete()
        
        votes_class[vote_type].objects.create(
            user=req.user,
            procedure_desc=procedure_desc
        )
        
        # Send a notification to the owner of the ProcedureDesc of the upvote
        # TODO: Link the notification to the vote object
        notification = VoteNotification.objects.create(
            user=procedure_desc.user,
            category='vote',
            action=vote_type,
            procedure_desc=procedure_desc,
            by=req.user
        )
        msg = VoteNotificationSerializer(notification).data
        pubnub = PubNub(settings.PNCONFIG)
        channel = str(procedure_desc.user)
        envelope = pubnub.publish().channel(channel).message(msg).sync()

        return Response('', status=HTTP_204_NO_CONTENT)

    def delete(self, req, procedure_desc_id):
        # TODO: Check that user is self
        votes_class = {'upvote': ProcedureDescUpvote, 'downvote': ProcedureDescDownvote}
        vote_type = req.data.get('vote_type', None)
        procedure_desc = get_object_or_404(ProcedureDesc, id=procedure_desc_id)

        if vote_type not in votes_class:
            # TODO: Return error and report incident
            pass
        
        vote = get_object_or_404(votes_class[vote_type], 
                                                        procedure_desc=procedure_desc,
                                                        user=req.user
                                )
        vote.delete()
        return Response('', status=HTTP_204_NO_CONTENT)

# TODO: Decide which of the two to keep
class SimilarView(APIView):
    permission_classes = ()

    def get(self,req):
        md5 = req.query_params.get('md5', None)
        offset = req.query_params.get('offset', None)
        try:
            offset = int(offset)
        except:
            return Response('Offset not an integer', status=HTTP_400_BAD_REQUEST)
        
        program = get_object_or_404(Program, md5=md5)
        procedure = get_object_or_404(Procedure, program=program, offset=offset)
        proc_desc = ProcedureDesc.objects.filter(procedure=procedure).values("id").first()
        if proc_desc == None:
            return Response('Not found', status=HTTP_404_NOT_FOUND)
        
        dic = {proc_desc["id"]: 3}
        out = query_id(dic)
        
        resp = []
        for r, o, i in out[proc_desc["id"]]:
            proc = o.procedure
            prog = o.procedure.program
            resp.append({
                "md5": prog.md5,
                "name_bin" : ProgramInfo.objects.filter(program=prog, user=o.user).values("filename").first()["filename"],
                "offset": proc.offset,
                "name_proc": o.name,
                "match": int(i)              
            })
        return Response(resp,status=HTTP_200_OK)

class SimProcsView(APIView):
    permission_classes = ()

    def post(self, req):
        dic = {}
        id_md5off = {}
        
        for md5_off in req.data:
            a = md5_off.split(":")
            md5 = a[0]
            off = int(a[1])
            program = get_object_or_404(Program, md5=md5)
            try:
                procedure = Procedure.objects.filter(program=program, offset=off).first()
                proc_desc = ProcedureDesc.objects.filter(procedure=procedure).values("id").first()
                
                dic[proc_desc["id"]] = req.data[md5_off]
                id_md5off[proc_desc["id"]] = md5_off
            except: pass
        
        out = query_id(dic)
        
        res = {}
        for key in out:
            md5_off = id_md5off[key]
            res[md5_off] = []
            for r, o, i in out[key]:
                proc = o.procedure
                prog = o.procedure.program
                res[md5_off].append({
                    "md5": prog.md5,
                    "offset": proc.offset,
                    "name": o.name,
                    "match": int(i)
                })
        return Response(res, status=HTTP_200_OK)

# Social
class ProcedureDescCommentView(APIView):
    """
    View responsible for the CRUD of the ProcedureDescComment
    """
    def get(self, req):
        # TODO: Return 400 if any of the fields are empty
        procedure_desc_id = req.query_params.get('procedure_desc', None)
        page_num = req.query_params.get('page', 1)
        
        procedure_desc = get_object_or_404(ProcedureDesc, id=procedure_desc_id)

        # TODO: Order this query since it needs to be paginated
        comments = ProcedureDescComment.objects.filter(procedure_desc=procedure_desc).all()
        pager = Paginator(comments, COMMENTS_PER_PAGE)
        if page_num not in pager.page_range:
            # TODO: Return error since an unexisting page has been asked
            pass
    
        res = {
            'comments': ProcedureDescCommentSerializer(
                            pager.page(page_num).object_list, many=True
                        ).data
        }
        return Response(res, status=HTTP_200_OK)
    
    def post(self, req):
        # TODO: Return 400 if any of the fields are empty
        procedure_desc_id = req.data.get('procedure_desc', None)
        user = req.user
        comment = req.data.get('comment', None)

        procedure_desc = get_object_or_404(ProcedureDesc, id=procedure_desc_id)
        procedure_desc_comment = ProcedureDescComment.objects.filter(
                                    procedure_desc=procedure_desc,
                                    user=user
                                 ).first()
        if procedure_desc_comment is not None:
            procedure_desc_comment.comment = comment
            procedure_desc_comment.save()
        else:
            ProcedureDescComment.objects.create(
                procedure_desc=procedure_desc,
                user=user,
                comment=comment
            )

        return Response('', status=HTTP_204_NO_CONTENT)
    
    def delete(self, req):
        # TODO: Return 400 if any of the fields are empty
        procedure_desc_comment_id = req.data.get('procedure_desc_comment', None)
        user = req.user

        procedure_desc_comment = get_object_or_404(ProcedureDescComment, id=procedure_desc_comment_id)
        if user != procedure_desc_comment.user:
            # TODO: This should not happen, report the incident
            pass
        
        procedure_desc_comment.delete()

        return Response('', status=HTTP_204_NO_CONTENT)

class ProcedureDescCommentVoteView(APIView):

    def get(self, req, procedure_desc_comment_id):
        """
        Given a ProcedureDescComment return its number of upvotes and downvotes
        """
        # TODO: Return an error if any of the fields is empty
        procedure_desc_comment = get_object_or_404(ProcedureDescComment, id=procedure_desc_comment_id)

        res = {
            'upvotes': ProcedureDescCommentUpvote.objects.filter(procedure_desc_comment=procedure_desc_comment).count(),
            'downvotes': ProcedureDescCommentDownvote.objects.filter(procedure_desc_comment=procedure_desc_comment).count()
        }

        return Response(res, status=HTTP_200_OK)

    def post(self, req, procedure_desc_comment_id):
        """
        Creates a vote of a user to a given ProcDescComment, if not already done
        """
        # TODO: Return error if any of the fields are empty
        votes_class = {'upvote': ProcedureDescCommentUpvote, 'downvote': ProcedureDescCommentDownvote}
        vote_type = req.data.get('vote_type', None)
        logger.info(procedure_desc_comment_id)
        procedure_desc_comment = get_object_or_404(ProcedureDescComment, id=procedure_desc_comment_id)

        if vote_type not in votes_class:
        # TODO: Return error and report incident
            pass
        
        # Check if vote is already present and the same request has been issued
        upvote = ProcedureDescCommentUpvote.objects.filter(
            user=req.user,
            procedure_desc_comment=procedure_desc_comment
            ).first()
        if votes_class[vote_type] == ProcedureDescCommentUpvote and upvote is not None:
            # TODO: This should not happen since a user cannot give more than one vote, report incident
            res = {
                'vote_error' : 'User cannot give more than one Upvote'
            }
            return Response(res, status=HTTP_204_NO_CONTENT)

        downvote = ProcedureDescCommentDownvote.objects.filter(
            user=req.user,
            procedure_desc_comment=procedure_desc_comment
            ).first()
        if votes_class[vote_type] == ProcedureDescCommentDownvote and downvote is not None:
            # TODO: This should not happen since a user cannot give more than one vote, report incident
            res = {
                'vote_error' : 'User cannot give more than one Downvote'
            }
            #FIXED: is 204 response correct in this case?
            return Response(res, status=HTTP_204_NO_CONTENT)
            
        # If the request is different, but a vote from the user already exists, the previous vote, which 
        # must be different, should be deleted
        if upvote is not None:
            upvote.delete()
        if downvote is not None:
            downvote.delete()
        
        votes_class[vote_type].objects.create(
            user=req.user,
            procedure_desc_comment=procedure_desc_comment
        )

        return Response('', status=HTTP_204_NO_CONTENT)
