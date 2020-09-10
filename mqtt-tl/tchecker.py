import os,json,logging,csv

class T_checker():
    def __init__(self,key_dir="klog",MAX_LOG_SIZE=5000):
        self.key_root_dir=key_dir
        self.create_root_dir(self.key_root_dir)
        self.columns = ['name', 'uid']
        self.MAX_LOG_SIZE=MAX_LOG_SIZE

    def create_key_dir(self, key_dir):
        fo.flush()
        os.fsync(fo.fileno())

    def log_key(self,data):
        columns=list(data.keys())
        


        

    def write(self,fo,data,writer):
        if(self.key_new):
        logging.info(data)
        writer.writerow(data)
        
    def create_key_file(self,dir,columns,fo="",count=0):
        key_numbr="{0:003d}".format(count)
        logging.info("log number")
        log_numbr="{0:003d}".format(count)
        logging.info("log number "+str(log_numbr)+ "  dir "+dir)
        filename= "log"+str(log_numbr)+".csv"
        try:
                os.stat(filename)
                os.remove(filename)#remove old log if exists
        except:
            pass
            filename=dir+"/"+filename
            logging.info("Creating log "+str(count))

            if count==0:
                pass   
            else:
                fo.close() #close old log file

            #update_topic_counter(topic,count)
            fo=open(filename, 'w')
            count+=1
            writer=csv.DictWriter(fo,\
                                    fieldnames=columns,quoting=csv.QUOTE_MINIMAL)
            self.topics[topic]=[fo,dir,filename,count,writer]
            writer.writeheader() 
            return (fo,writer)

