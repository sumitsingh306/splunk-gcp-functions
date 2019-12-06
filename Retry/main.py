#RetryAll0.1.5.py
'''MIT License
Copyright (c) 2019 Splunk
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

import os
import requests
from requests.adapters import HTTPAdapter
import urllib3
import time
##turns off the warning that is generated below because using self signed ssl cert
urllib3.disable_warnings()


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    #messageCount=phoneHome()
    messageCount=1
    while messageCount!=0:
        try:
            messageCount=synchronous_pull(os.environ['PROJECTID'],os.environ['SUBSCRIPTION'])
        except:
            messageCount=0

def synchronous_pull(project_id, subscription_name):
    """Pulling messages synchronously."""
    # [START pubsub_subscriber_sync_pull]
    from google.cloud import pubsub_v1

    
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    NUM_MESSAGES = 100     #max pull from pub-sub

    # The subscriber pulls a specific number of messages.
    response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

    ack_ids = []
    incount=0
    outcount=0

    for received_message in response.received_messages:
        incount=incount+1 
        tok=received_message.message.attributes["token"]
        url=received_message.message.attributes["url"]  
        #send to HEC
        if splunkHec(url,tok,received_message.message.data.decode(encoding="utf-8")): #successful write to HEC
            #keep track of succesful messages
            ack_ids.append(received_message.ack_id)
            outcount=outcount+1
            
            # Acknowledges the messages that were succesfully written so they will not be sent again.
        subscriber.acknowledge(subscription_path, ack_ids)

    print('in:'+str(incount)+' success:'+str(outcount))
    return outcount


    


def splunkHec(url,token,logdata):
  
  #test for over-rides. All 3 over-ride variables must be available to over-ride.
  try:
    url_o = 'https://'+os.environ['HEC_URL']+'/services/collector'
  except:
    url_o = 'x'
  try:
    token_o = os.environ['HEC_TOKEN']
  except:
    token_o = 'x'
  try:
    index_type=os.environ['EVENT_TYPE']
  except:
    index_type='x'

  if (url_o!='x' and token_o!='x' and index_type!='x'):
    token=token_o
    if index_type=='METRIC':
        url = 'https://'+os.environ['HEC_URL']+'/services/collector'
    elif index_type=='EVENT':
        url = 'https://'+os.environ['HEC_URL']+'/services/collector/event'
    else:
        url = 'https://'+os.environ['HEC_URL']+'/services/collector/raw'
  
  s = requests.Session() 
  s.mount( 'http://' , HTTPAdapter(max_retries= 3 )) 
  s.mount( 'https://' , HTTPAdapter(max_retries= 3 ))
  
  authHeader = {'Authorization': 'Splunk '+ token}

  try:
    r = s.post(url, headers=authHeader, data=logdata, verify=False, timeout=2)
    r.raise_for_status()
  except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
    if errh.response.status_code<500:
        print(r.json())
    return False
  except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
    return False
  except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
    return False
  except requests.exceptions.RequestException as err:
    print ("Error: ",err)
    return False
  return True
        
'''def phoneHome(): 
    #do a quick health check call to HEC - if there is still a connection issue, then no need to try remainder of function
    url = 'https://'+os.environ['HEC_URL']+'/services/collector/health'
    s = requests.Session() 
    s.mount( 'http://' , HTTPAdapter(max_retries= 3 )) 
    s.mount( 'https://' , HTTPAdapter(max_retries= 3 ))

    try:
        r = s.get(url, verify=False, timeout=2)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        if errh.response.status_code<500:
            print(r.json())
        return 0
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return 0
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return 0
    except requests.exceptions.RequestException as err:
        print ("Error: ",err)
        return 0
    except:
        print("unknown Error in http get health")
        return 0 
    #print(r.status_code)
    if r.status_code==200:
        return 1
    else:
        return 0'''