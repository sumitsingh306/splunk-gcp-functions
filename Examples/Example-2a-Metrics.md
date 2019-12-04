# Example 2a Metrics Collection (Event Index)

This example will create a Cloud Schedule which triggers the Metrics Function (via a PubSub Topic). The function will send the metrics into Splunk HEC as an Event format (into an Event index). The script will also create a retry PubSub Topic, and set up a Function to retry any failed messages to HEC. 
(If you have already created any other examples, the Cloud Schedule and PubSub Trigger topic doesn't need to be re-created)

#### PubSub Topics:

**ExampleRetryTrigger** : This topic is common between all functions and triggers retries based on Cloud Schedule

**ExampleMetricsTriggerTopic** : This topic is the trigger for the metrics functions (set by Cloud Schedule)

**ExampleEventsRetryTopic** : This topic will collect failed HEC writes from ExampleMetricsEventsFunction



#### GCP Functions:

**ExampleMetricsFunction** : Function to pull sample of metrics from compute. Formatted as metrics index into HEC

**ExampleEventsRetryTopic** : Retry Function to pull any failed messages from ExampleMetricsFunction


#### Cloud Scheduler

**ExampleMetricsSchedule** : Schedule for Running Events (5mins)
**ExampleRetry** : Retry Schedule (10mins)


## CLI Example

(run in bash or the Cloud Shell)

**Note that you will need to change values in bold in the scripts below to identify your project id, Log-Sink Service Account, HEC URL and HEC Token**

<pre>

#This Schedule and topic only needs to be created once for all metrics functions unless you want different schedules. 
#Note:Match the schedule to the value in the TIME_INTERVAL environment variable below
#This example assumes a 5 minute schedule

gcloud pubsub topics create ExampleMetricsTriggerTopic

gcloud scheduler jobs create pubsub ExampleMetricsSchedule --schedule "*/5 * * * *" --topic ExampleMetricsTriggerTopic --message-body "RunMetric"

# ..End of common Metric trigger section

#create retry topics/subscription

gcloud pubsub topics create ExampleEventsRetryTopic

gcloud pubsub subscriptions create --topic ExampleEventsRetryTopic ExampleEventsRetryTopic-sub


#this command only needs to be done once for all of the examples
git clone https://github.com/pauld-splunk/splunk-gcp-functions.git

cd splunk-gcp-functions/PubSubFunction

cd ../Metrics

#create function

gcloud functions deploy ExampleMetricsEventsFunction --runtime python37 /
--trigger-topic=ExampleMetricsTriggerTopic --entry-point=hello_pubsub --allow-unauthenticated /
--set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',METRICS_LIST='["compute.googleapis.com/instance/cpu/utilization","compute.googleapis.com/instance/disk/read_ops_count","compute.googleapis.com/instance/disk/write_bytes_count","compute.googleapis.com/instance/disk/write_ops_count","compute.googleapis.com/instance/network/received_bytes_count","compute.googleapis.com/instance/network/received_packets_count","compute.googleapis.com/instance/network/sent_bytes_count","compute.googleapis.com/instance/network/sent_packets_count","compute.googleapis.com/instance/uptime"]',TIME_INTERVAL='5',RETRY_TOPIC='ExampleEventsRetryTopic'

cd ../RetryBatch

#create Retry function

gcloud functions deploy ExampleEventsRetryFunction --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',SUBSCRIPTION='ExampleEventsRetryTopic-sub',EVENT_TYPE='EVENT'


# This section only needs to be done once for all examples. All examples will use the same Retry Schedule/Topic

gcloud pubsub topics create ExampleRetryTrigger

gcloud scheduler jobs create pubsub ExampleRetrySchedule --schedule "*/10 * * * *" --topic ExampleRetryTrigger --message-body "Retry"

</pre>