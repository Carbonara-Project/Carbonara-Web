import pickle
import logging

from django.db import connection
from .minhash import LeanMinHash

logger = logging.getLogger('django')

def create_lshforest_tables(**kwargs):
    tables = [
        "procs_lshforest",
    ]
    with connection.cursor() as cur:
        for table in tables:
            logger.info("create_lshforest_tables: %s setup..." % table)
            e = cur.execute("show tables like '%s'" % table)
            if e == 0:
                cur.execute('''
                    create table TABLE (
                        hp0 tinyblob,
                        hp1 tinyblob,
                        hp2 tinyblob,
                        hp3 tinyblob,
                        hp4 tinyblob,
                        hp5 tinyblob,
                        hp6 tinyblob,
                        hp7 tinyblob,
                        k mediumblob
                    )'''.replace("TABLE", table))
                #all hpN field are 64 bytes
                cur.execute('create index ix_hp0_TABLE on TABLE (hp0(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp1_TABLE on TABLE (hp1(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp2_TABLE on TABLE (hp2(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp3_TABLE on TABLE (hp3(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp4_TABLE on TABLE (hp4(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp5_TABLE on TABLE (hp5(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp6_TABLE on TABLE (hp6(64))'.replace("TABLE", table))
                cur.execute('create index ix_hp7_TABLE on TABLE (hp7(64))'.replace("TABLE", table))
                cur.execute('create index ix_allhps_TABLE on TABLE (hp0(64), hp1(64), hp2(64), hp3(64), hp4(64), hp5(64), hp6(64), hp7(64))'.replace("TABLE", table))
                
                logger.info("create_lshforest_tables: %s created" % table)
            else:
                logger.info("create_lshforest_tables: %s is in already in the db" % table)

def escape_sql_like(s):
    return s.replace(b'\\', b'\\\\').replace(b'%', b'\\%').replace(b'_', b'\\_')


class ProcsLSHForest(object):
    
    def __init__(self, table, num_perm=64):
        
        if num_perm <= 0:
            raise ValueError("num_perm must be positive")
        if num_perm < 8:
            raise ValueError("num_perm cannot be less than 8")
        
        self.table = table
        
        # Maximum depth of the prefix tree
        self.k = int(num_perm / 8)
        
        self.hashranges = [(i*self.k, (i+1)*self.k) for i in range(8)]
        
    
    
    def _add(self, key, Hs, cur):
    
        params = []
        for H in Hs:
            params.append(H)
        
        cur.execute('''select k
                       from ''' + self.table + '''
                       where hp0 = %s and hp1 = %s and hp2 = %s and hp3 = %s and hp4 = %s and hp5 = %s and hp6 = %s and hp7 = %s
                       ''', params)
        e = cur.fetchone()
        
        if e == None:
            t = pickle.dumps([key])
            cur.execute('''insert into ''' + self.table + ''' (hp0, hp1, hp2, hp3, hp4, hp5, hp6, hp7, k)
                           values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', params + [t])
        else:
            t = pickle.loads(e[0])
            t.append(key)
            t = pickle.dumps(t)
            cur.execute('''update ''' + self.table + '''
                           set k = %s
                           where hp0 = %s and hp1 = %s and hp2 = %s and hp3 = %s and hp4 = %s and hp5 = %s and hp6 = %s and hp7 = %s
                           ''', [t] + params)
    
    def add(self, key, minhash):
    
        if len(minhash) < self.k*8:
            raise ValueError("The num_perm of MinHash out of range")
        
        Hs = [self._H(minhash.hashvalues[start:end])
            for start, end in self.hashranges]
        
        with connection.cursor() as cur:
            self._add(key, Hs, cur)
    
    
    
    def _update(self, key, old_Hs, Hs, cur):
    
        old_params = []
        for H in old_Hs:
            old_params.append(H)
        
        cur.execute('''select k
                       from ''' + self.table + '''
                       where hp0 = %s and hp1 = %s and hp2 = %s and hp3 = %s and hp4 = %s and hp5 = %s and hp6 = %s and hp7 = %s
                       ''', old_params)
        e = cur.fetchone()
        
        if e != None:
            t = pickle.loads(e[0])
            t.remove(key)
            t = pickle.dumps(t)
            #TODO remove row if t is empty
            cur.execute('''update ''' + self.table + '''
                           set k = %s
                           where hp0 = %s and hp1 = %s and hp2 = %s and hp3 = %s and hp4 = %s and hp5 = %s and hp6 = %s and hp7 = %s
                           ''', [t] + old_params)
            
        self._add(key, Hs, cur)
    
    def update(self, key, old_minhash, minhash):
    
        if len(minhash) < self.k*8:
            raise ValueError("The num_perm of MinHash out of range")
        
        old_Hs = [self._H(old_minhash.hashvalues[start:end])
            for start, end in self.hashranges]
        
        Hs = [self._H(minhash.hashvalues[start:end])
            for start, end in self.hashranges]
        
        with connection.cursor() as cur:
            self._update(key, old_Hs, Hs, cur)
        
    
    
    def manager(self, insert_dict, upload_dict):
        with connection.cursor() as cur:
            for key in insert_dict:
                minhash = LeanMinHash.deserialize(insert_dict[key])
                
                Hs = [self._H(minhash.hashvalues[start:end])
                    for start, end in self.hashranges]
              
                self._add(key, Hs, cur)
            
            for key in upload_dict:
                old_minhash = LeanMinHash.deserialize(upload_dict[key][0])                
                minhash = LeanMinHash.deserialize(upload_dict[key][1])
                
                old_Hs = [self._H(old_minhash.hashvalues[start:end])
                    for start, end in self.hashranges]
                
                Hs = [self._H(minhash.hashvalues[start:end])
                    for start, end in self.hashranges]
                
                self._update(key, old_Hs, Hs, cur)
        
        
    

    def _query(self, minhash, r, cur):
        
        if r > self.k or r <=0:
            raise ValueError("parameter outside range")
        
        # Generate prefixes of concatenated hash values
        hps = [self._H(minhash.hashvalues[start:start+r])
                for start, _ in self.hashranges]
        
        for i, hp in enumerate(hps):
            cur.execute("select hp" + str(i) + ", k from " + self.table + " where hp" + str(i) + " like %s||'%%' order by hp" + str(i), (escape_sql_like(hp),))
            e = cur.fetchone()
            
            while e != None:
                yield e[1]
                e = cur.fetchone()

    def query(self, minhash, k):
        
        if k <= 0:
            raise ValueError("k must be positive")
        if len(minhash) < self.k*8:
            raise ValueError("The num_perm of MinHash out of range")
        results = set()
        r = self.k
        
        with connection.cursor() as cur:
            while r > 0:
                for key in self._query(minhash, r, cur):
                    ks = pickle.loads(key)
                    for i in ks:
                        results.add(i)
                        if len(results) >= k:
                            return list(results)
                r -= 1
            return list(results)


    def _H(self, hs):
        return bytes(hs.byteswap().data)



