mqttclient_log = False
import json
import paho.mqtt.client as mqtt
import logging
import collections
import time

class MQTTClient(mqtt.Client):#extend the paho client class
   run_flag=False #global flag used in multi loop
   def __init__(self,cname,**kwargs):
      super(MQTTClient, self).__init__(cname,**kwargs)
      self.topic_ack=[] #used to track subscribed topics
      self.subscribe_flag=False
      self.bad_connection_flag=False
      self.bad_count=0
      self.count=0
      self.connected_flag=False
      self.connect_flag=False #used in multi loop
      self.sub_topic="painlessMesh/#"
      self.sub_topics=[] #multiple topics
      self.sub_qos=0
      self.broker="127.0.0.1"
      self.port=1883
      self.keepalive=60
      self.cname="logger"
      self.delay=10 #retry interval

class User(object):
    def __init__(self, name, key):
        self.name=name
        self.key=key

def Initialise_clients(cname,mqttclient_log=False,cleansession=True,flags=""):
    #flags set

   logging.info("initialising clients")
   client= MQTTClient(cname,clean_session=cleansession)
   client.cname=cname
   client.on_connect= on_connect        #attach function to callback
   client.on_message= on_message        #attach function to callback
   if mqttclient_log:
      client.on_log=on_log
   return client

def on_connect(client, userdata, flags, rc):
   """
   set the bad connection flag for rc >0, Sets onnected_flag if connected ok
   also subscribes to topics
   """
   logging.debug("Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id")

   if rc==0:
      client.connected_flag=True #old clients use this
      client.bad_connection_flag=False
      if client.sub_topic!="": #single topic
          print("subscribing "+str(client.sub_topic))
          topic=client.sub_topic
          if client.sub_qos==0:
              qos=client.sub_qos
              client.subscribe(topic,qos)
      elif client.sub_topics!="":

        client.subscribe(client.sub_topics)
        print("Connected and subscribed to ",client.sub_topics)

   else:
     client.bad_connection_flag=True #
     client.bad_count +=1
     client.connected_flag=False #

def on_message(client,userdata, msg):
    
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    message_handler(client,m_decode,topic)
    print("message received ",topic)
    
def message_handler(client,msg,topic):
    data=collections.OrderedDict()
    data = json.loads(msg)
    key = data['uid']
    #client.q.put(data) #put messages on queue
    data['user'] = key_handler(key)
    print(data)

def add_key(key):
    with open('keys.json') as jsonfile:
        keyfile = json.load(jsonfile)
    print('Unknown Key/User\n Enter Name:\n')
    newname= str(input())
    y = {"user" : newname,
         "uid" : key}
    keyfile['user'].append(y)
    

def key_handler(key):
    print('f')
    i = 0
    with open ('keys.json', 'a') as jsonfile:
        
        try:
            #see if we can load data from file
            keyfile = json.load(jsonfile)
        except:
            keyfile = collections.orderedDict()
            print('h')
    isnew = True
    
    try:
        for object in keyfile['uid']:
            print('i')
            i = i+1
            if key == object['uid']:
                print('j')
                isnew = False
                return object['name']
            if isnew == True:
                print('Unknown Key/User\n Enter Name:\n')
                newname= str(input())
                temp = {key : newname}
                keyfile += temp
                return(newname)
    except: 
        if isnew == True:
            print('Unknown Key/User\n Enter Name:\n')
            newname= str(input())
            temp = {key : newname}
            keyfile += temp
            return(newname)



client=Initialise_clients("logger",mqttclient_log,False)#create and initialise client object

try:
    res=client.connect(client.broker,client.port)
    print("connecting to broker",client.broker)
    client.loop_start() #start loop
except:
    logging.debug("connection failed")
    print("connection failed")
    client.bad_count +=1
    client.bad_connection_flag=True #old clients use this
#loop and wait until interrupted  

try:
    while True:
        time.sleep(1)
        pass
except KeyboardInterrupt:
    print("interrrupted by keyboard") 

client.loop_stop()    


