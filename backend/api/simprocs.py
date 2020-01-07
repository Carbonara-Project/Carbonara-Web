import math
from django.shortcuts import get_object_or_404

from .minhash import LeanMinHash
from .models import ProcedureDesc
from .lshforest import ProcsLSHForest

def insert(insert_dict, update_dict):
    ProcsLSHForest("procs_lshforest").manager(insert_dict, update_dict)


def query_id(dic):

    forest = ProcsLSHForest("procs_lshforest")
    output = {}
    
    for key in dic:
        k = dic[key]
        
        keydesc = ProcedureDesc.objects.get(id=key)
        
        #get procdescs associated to the same procedure
        descs = ProcedureDesc.objects.filter(procedure=keydesc.procedure).values("id")
        descs_list = []
        for row in descs:
            descs_list.append(row["id"])
        
        key_vex = LeanMinHash.deserialize(bytes.fromhex(keydesc.vex_hash))
        key_flow = LeanMinHash.deserialize(bytes.fromhex(keydesc.flow_hash))
        key_len = keydesc.raw_len
        
        res = forest.query(key_vex, k + len(descs_list))
        match = {}
        query_objs = {}
        
        for r in res:
            if r in descs_list:
                continue
            
            pdesc = get_object_or_404(ProcedureDesc, id=r)
            # pdesc = ProcedureDesc.objects.get(id=r)
            
            vex_hash = LeanMinHash.deserialize(bytes.fromhex(pdesc.vex_hash))
            flow_hash = LeanMinHash.deserialize(bytes.fromhex(pdesc.flow_hash))
            
            vex_j = key_vex.jaccard(vex_hash)
            flow_j = key_flow.jaccard(flow_hash)
            
            match[r] = vex_j * 100 + (math.atan(key_len/1000.0) / (math.pi/2) * flow_j**2 * 20)
            query_objs[r] = pdesc
        
        found = sorted(match, key=match.get, reverse=True)[:k]
        
        output[key] = []
        for r in found:
            i = match[r] if match[r] < 100 else 100
            output[key].append((r, query_objs[r], i))
    
    return output 
    

