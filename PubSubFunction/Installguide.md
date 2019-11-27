# GCP Cloud Functions – Installation / Setup Guide

## PubSub Function (version 0.1.6)

### **Pre-requisites**

HEC set-up on a Splunk instance (load balancer needed for a cluster)
Install GCP Add-On https://splunkbase.splunk.com/app/3088/ (uses the same sourcetypes defined in the add-on)
Set up Stackdriver logs; create an export(s) and subscription to a PubSub Topic (see important note below)
Set up a PubSub Topic for error messages (Note the name of the topic -  this will be used in the Environment variables later)

### **Setup**
1.	Create a new Cloud Function
2.	Name your function – note the name – see important note below on the log export
3.	Set the Trigger to be Cloud Pub Sub 
4.	Select a Topic from PubSub
5.	Add the code:
6.	Select Inline editor as source
7.	Select the Runtime as Python 3.7
8.	Copy the function code into the main.py
9.	Copy the requirements into the requirements.txt tab
10.	Click on “Show variables like environment, networking, timeouts and more” to open up more options
11.	Select the region where you want the function to run
12.	Click on the + Add variable to open up the Environment variables entry
13.	Add the Environment variables and values described in the table below
14.	In another browser window, check that the log export that is subscribed by the PubSub Topic has eliminated the name of the function. (see below)
15.	Click Deploy
16.	You will need to install the PubSubRetry function if you wish to have a recovery for any events that failed to write to Splunk. See install guide for that function.

#### Function Environment Variables


**Variable	      	Value**
--------------------------
HEC_URL             Hostname/IP address for URL for Splunk HEC (Load balancer recommended) – e.g. mysplunkinstance.splunk.com
					113.114.115.192
					Note, no need for https or /services/collector/event 
HEC_TOKEN			HEC Token for the input. Generate on Splunk instance.
PROJECTID			Project ID for where the Retry Topic exists
HOST				Host value that Splunk will assign for the PubSub event. Defaults to GCPFunction
SPLUNK_SOURCETYPE	Sourcetype that will be given to the event (defaults to google:gcp:pubsub:message)
SPLUNK_SOURCE		If set, this will be assigned to the “Source” of the event. If not set, defaults to PubSub topic
INDEX				If this is set, its value can be set to over-ride the HEC token index. If this is set to LOGNAME then another
					environment variable with the name of the log needs to be set with an index name e.g. if you want all logs from “cloudaudit.googleapis.com%2Factivity” to be sent to index ActivityIX, you need to create an environment variable with the name “activity” with the value of ActivityIX. Note to use the value after “%2F”, or if the log doesn’t have that, use the value after /logs/ (eg. A logname of projects/projname/logs/OSConfigAgent would have variable set to OSConfigAgent)
					Note that the HEC Token must have set access to the indexes noted here
					(defaults to no value – i.e. HEC token set index name)
_logname_			A variable with a log name (ending only) will override the HEC token index for the event. Note that INDEX needs to be 
					set to LOGNAME for this to be used.
					Use logname after /logs/ or if name has “%2F” in the name, use the logname after “%2F” 
					Examples:
					cloudaudit.googleapis.com%2Factivity -> use activity
					/logs/OSConfigAgent -> use OSConfigAgent
					(defaults to no value)
COMPATIBLE			Set this to TRUE to maintain compatibility with Add-On. If not TRUE, event payload will be exact copy of PubSub event
ERROR_TOPIC			Name of Topic to send event to on any failure scenario for the function



## PUB-SUB FUNCTION: IMPORTANT USAGE NOTE

As the cloud function executes within GCP’s environment, its own logs are collected in Stacktdriver logs. If your Log Export collects logs from Cloud Functions **MAKE SURE YOU ELIMINATE THE FUNCTION NAME FROM THE EXPORT**. Logs for this function cannot be collected by itself! 

For example, if your function name is GCP-Pub-Sub, and you wish to collect logs from other functions, then the Export Filter needs to include resource.labels.function_name!="GCP-Pub-Sub"

**Failure to do this will cause the function to race and max out function execution capacity in your project. (it is essentially logging itself, which then causes more logs to be created, causing a feedback race loop)**



