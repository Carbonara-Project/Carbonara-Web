import pika

AMQP_URL = '***'
AMQP_QUEUE = 'task-queue'

SECRET_KEY = b'***'

"""
Sends a task to Guanciale workers. 

How to use: create an istance of SenderAMQP once, this opens all connections, it should be done once.
You should only use send_task method, all is described in its documentation

:Example:

from amqp_sender import SenderAMQP
s = SenderAMQP()
s.send_task( # the sh*t goes here # )
"""

class SenderAMQP:

    def __init__(self):
        params = pika.URLParameters(AMQP_URL)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=AMQP_QUEUE, exclusive=False, durable=True)
        
        
    def send_task(self, task_id, fname, furl, db_content=None, db_name=None):
        """
        Sends task to Guanciale workers
        
        Parameters
        - - - - - - -
        :param task_id:    task identifier
        :param fname:     file name
        :param furl:      URL of the file
        :param db_conent: ninary content of the database if it's avaiable. Default is None
        :param db_name:   name of the database. Default is None
        
        .. warings also:: db_content and db_name are set to None by default. If the db_name
                            isn't None, then also db_content must be non None (and viceversa).
                            Otherwise a TypeError is raised
        """
        if (db_content==None) != (db_name==None):
            raise TypeError("db_content or db_name is None while the other is not None")
        
        msg = self.encode(task_id, fname, furl, db_content, db_name)
        self.send_to_queue(msg)
            
         
        
        
    
    def encode(self, task_id, fname, furl, db_content, db_name):
        msg = SECRET_KEY + b'\0'.join((str(task_id).encode(), fname.encode(), furl.encode())) + b'\0'
        if db_content != None:
            msg += b'\0'.join((db_name.encode(), bytearray(db_content)))
        return msg
        
        
    def send_to_queue(self, msg):
        # delivery_mode=2 makes messages persistent
        self.channel.basic_publish(exchange='', body=msg, routing_key=AMQP_QUEUE,
				                    properties=pika.BasicProperties(delivery_mode=2))  
				                
				                
 
