# GCP Cloud Functions – Installation / Setup Guide

# RetryEvent Function 
(0.1.5)
_(note that this is only for the Retry for PubSub Function Events, not for GCS or Metrics functions)_

### **Pre-requisites**
HEC set-up on a Splunk instance (load balancer needed for a cluster)
Install GCP Add-On https://splunkbase.splunk.com/app/3088/ (uses the same sourcetypes defined in the add-on)
Set up a PubSub Topic for error messages from the PubSub based functions.  Note the name of the topic -  this will be used for Environment variables for the functions.
Set up Stackdriver log subscription for the PubSub error Topic
Create a Retry Trigger PubSub Topic (note that this topic is only going to be used as a trigger, with no events being sent there)
Create a Cloud Schedule, triggering the Retry PubSub Topic. Schedule this for how frequent you wish to “flush” out any events that failed to send to Splunk (e.g. 15mins)

### **Setup**

1.	Create a new Cloud Function
2.	Name your function
3.	Set the Trigger to be Cloud Pub Sub 
4.	Select the Retry Trigger Topic from PubSub
5.	Add the code:
6.	Select Inline editor as source
7.	Select the Runtime as Python 3.7
8.	Copy the function code into the main.py
9.	Copy the requirements.txt contents into the requirements.txt tab
10.	Click on “Show variables like environment, networking, timeouts and more” to open up more options
11.	Select the region where you want the function to run
12.	Increase the timeout for this function to 120
13.	Click on the + Add variable to open up the Environment variables entry
14.	Add the Environment variables and values described in the table below
15.	Click Deploy

### **Function Environment Variables**

<table><tr><td><strong>Variable</strong></td><td><strong>Value</strong></td></tr>
<tr><td>HEC_URL</td><td>Hostname/IP address for URL for Splunk HEC (Load balancer required for cluster)
e.g. mysplunkinstance.splunk.com or 113.114.115.192</td></tr>
<tr><td>HEC_TOKEN</td><td>HEC Token for the input. Generate on Splunk instance.
Ideally this should be the same as the token used for the function that is using this as a retry</td></tr>
<tr><td>PROJECTID</td><td>Project ID for where the Retry Topic exists</td></tr>
<tr><td>SUBSCRIPTION</td><td>Name of the subscription that pulls from the Retry/Error PubSub Topic.</td></tr>
</table>


## Install with gcloud CLI

git clone https://github.com/pauld-splunk/splunk-gcp-functions.git

cd splunk-gcp-functions/RetryEvent

gcloud functions deploy **myRetryEventFunction** --runtime python37 --trigger-topic=**RETRY_TRIGGER_TOPIC** --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',SUBSCRIPTION='**Retry_PubSub_Subscription**'

** *Update the bold values with your own settings* **
