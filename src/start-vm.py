from ovirtsdk.api import API
from ovirtsdk.xml import params
from threading import Thread
import time
import logging

#Configure
 
APIURL="https://engine.rktechs.com/api"
APIUSER="admin@internal"
APIPASS="admin123"
CAFILE="/root/ca.crt"
LOGFILENAME="/tmp/start_vms_dc.log"

threads=[]
failedVms=[]

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOGFILENAME,
                    filemode='w')
def start_vms(vmObj):
logging.info('Thread to start %s', vmObj.name)
try:
vmObj.start()
#time.sleep(5)
except Exception as e:
logging.debug('Exception caught on VM ( %s) start:\n%s' % (vmObj.name, str(e)))
failedVms.append(vmObj.name)
if __name__ == "__main__":
   try:	
        api = API(url=APIURL,
              username=APIUSER,
              password=APIPASS,
              ca_file=CAFILE)
              print 'Connected to oVIRT API %s Successfully' % APIURL
              logging.info ( 'Successfully Connected to %s' % APIURL)
     try:
print ' \n I am logging in %s \n' % LOGFILENAME
vmsList = api.vms.list()
for i in vmsList:
print i.name
if i.status.state != 'up':
logging.warning('%s is not up, trying to start it' % i.name)
threadMe = Thread(target=start_vms, args=[i])
threadMe.start()
threads.append(threadMe)
     except Exception as e:
         logging.debug('Error:\n%s' % str(e))
    
     logging.warning ('No of VMs to start : %s' % len(threads))
     print 'No of VMs to start: %s' % len(threads)
     for th in threads:
logging.info ('Waiting for %s to join' % th)
th.join (30)
if not th.isAlive():
logging.info ('Thread : %s terminated' % (th.getName()))

else:
logging.debug( 'Thread : %s is still alive, you may check this task..' % (th))
logging.debug (' Below Vms failed to start with an exception:%s' % (failedVms));
     api.disconnect()


   except Exception as ex:
    logging.debug('Unexpected error: %s' % ex)