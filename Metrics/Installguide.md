# GCP Cloud Functions – Installation / Setup Guide

## Metrics Function (version 0.5.8)

### Pre-requisites – 
HEC set-up on a Splunk instance (load balancer needed for a cluster)
HEC token/input MUST allow access to an appropriate index – if the function is creating event metrics, an event index is needed, or if the function is to send to metrics index, the token must be associated with a metrics index.
Install GCP Add-On https://splunkbase.splunk.com/app/3088/ (uses the same sourcetypes defined in the add-on)
Set up a PubSub Topic for error messages from an event based functions (PubSub Function, Metrics Events Function) OR if this will be generating metrics, a PubSub for metrics Note the name of the topic -  this will be used for Environment variables for the functions.
Set up Stackdriver log subscription for the PubSub error Topic
Create a Retry Trigger PubSub Topic (note that this topic is only going to be used as a trigger, with no events being sent there)
Create a Cloud Schedule, triggering the Retry PubSub Topic. Schedule this for how frequent you wish to “flush” out any events that failed to send to Splunk (e.g. 15mins)

## Function Dependencies:

Metrics Function requires the RetryBatch Function 

## Setup

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
12.	Click on the + Add variable to open up the Environment variables entry
13.	Add the Environment variables and values described in the table below
14.	Click Deploy

## Function Environment Variables

<table><tr><td><strong>Variable</strong></td><td><strong>Value</strong></td></tr>
<tr><td>HEC_URL</td><td>Hostname/IP address for URL for Splunk HEC (Load balancer required for cluster)
e.g. mysplunkinstance.splunk.com or 113.114.115.192</td></tr>
<tr><td>HEC_TOKEN</td><td>HEC Token for the input. Generate on Splunk instance.
Ideally this should be the same as the token used for the function that is using this as a retry
</td></tr>
<tr><td>PROJECTID</td><td>Project ID for where the Retry Topic exists</td></tr>
<tr><td>METRICS_LIST</td><td>A list of metrics for the function to pull. Enclose the comma separated list with square brackets. Use full names for the metrics. For example:
["compute.googleapis.com/instance/cpu/utilization","compute.googleapis.com/instance/disk/read_ops_count"]
</td></tr>
<tr><td>TIME_INTERVAL</td><td>Time interval for the function to retrieve metrics for (in minutes). This is retrospective – i.e a setting of 5 will retrieve metrics from the last 5 minutes.</td></tr>
<tr><td>HOST</td><td>Hostname you wish to give the event
Defaults to GCPMetricsFunction
</td></tr>
<tr><td>SPLUNK_SOURCETYPE</td><td>Sourcetype to assign to the events. Note that this is only used if the metric is going into an event index.
Defaults to google:gcp:monitoring
</td></tr>
<tr><td>METRIC_INDEX_TYPE</td><td>Sets the type of metrics index that is being sent to. This should be METRICS for metrics index, or EVENT for event index.The event format is compatible with the GCP Add-On metrics.
Defaults to EVENT
</td></tr>
<tr><td>RETRY_TOPIC</td><td>Name of Topic to send event/metric to on any failure scenario for the function</td></tr>
</table>


## **Function Flow process**

**Normal Flow:**
Cloud Schedule -> PubSub Topic (Trigger) -> GCP Function(->Pull from Stackdriver API)-> HEC

**Error Flow:** 
Cloud Schedule -> PubSub Topic (Trigger) -> GCP Function(->Pull from Stackdriver API)-> PubSub error Topic
Cloud Schedule -> PubSub Topic (Trigger) -> GCP Function(->Pull from PubSub error Topic)-> HEC
