# Example 2b Metrics Collection (Metrics Index)

This example will create a Cloud Schedule which triggers the Metrics Function (via a PubSub Topic). The function will send the metrics into Splunk HEC as a metric format (into an metric index). The script will also create a retry PubSub Topic, and set up a Function to retry any failed messages to HEC. 
(If you have already created any other examples, the Cloud Schedule and PubSub Trigger topic doesn't need to be re-created)

#### PubSub Topics:

**ExampleRetryTrigger** : This topic is common between all functions and triggers retries based on Cloud Schedule

**ExamplePubSubRetryTopic** : This topic can be common between all functions. This topic will collect failed writes from the Functions to HEC

**ExampleRetryTrigger** : This topic can be common between all functions and triggers retries based on Cloud Schedule


#### GCP Functions:

**ExampleMetricsFunction** : Function to pull sample of metrics from compute. Formatted as a metric into metrics index via HEC

**ExampleMetricRetryTopic** : Retry Function to pull any failed messages from ExampleMetricsFunction


#### Cloud Scheduler

**ExampleMetricsSchedule** : Schedule for Running Events (5mins) - Common for all metrics examples
**ExampleRetry** : Retry Schedule (10mins) - common for all examples


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


#this command only needs to be done once for all of the examples
git clone https://github.com/pauld-splunk/splunk-gcp-functions.git


cd splunk-gcp-functions/Metrics

#create function

echo -e "HEC_URL: '<strong>HOSTNAME_OR_IP_FOR_HEC</strong>'\\nHEC_TOKEN: <strong>0000-0000-0000-0000</strong>\\nPROJECTID: <strong>Project-id</strong>\\nTIME_INTERVAL: '5'\\nRETRY_TOPIC: ExamplePubSubRetryTopic\\nMETRIC_INDEX_TYPE: METRICS\\nMETRICS_LIST: '["compute.googleapis.com/instance/cpu/utilization","compute.googleapis.com/instance/disk/read_ops_count","compute.googleapis.com/instance/disk/write_bytes_count","compute.googleapis.com/instance/disk/write_ops_count","compute.googleapis.com/instance/network/received_bytes_count","compute.googleapis.com/instance/network/received_packets_count","compute.googleapis.com/instance/network/sent_bytes_count","compute.googleapis.com/instance/network/sent_packets_count","compute.googleapis.com/instance/uptime"]'" > EnvVarsMetrics.yaml

gcloud functions deploy ExampleMetricsFunction --runtime python37 \
--trigger-topic=ExampleMetricsTriggerTopic --entry-point=hello_pubsub --allow-unauthenticated \
--env-vars-file EnvVarsMetrics.yaml


#This is a common section for all examples
#Doesn't need to be repeated for all unless you wish to have separate PubSub Topics for retrying different events.

gcloud pubsub topics create ExamplePubSubRetryTopic

gcloud pubsub subscriptions create --topic ExamplePubSubRetryTopic ExamplePubSubRetryTopic-sub
cd ../Retry

#create Retry function

gcloud functions deploy ExamplePubSubRetry --runtime python37 \
 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --timeout=120 \
 --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',SUBSCRIPTION='ExamplePubSubRetryTopic-sub'

gcloud pubsub topics create ExampleRetryTrigger

gcloud scheduler jobs create pubsub ExampleRetrySchedule --schedule "*/10 * * * *" --topic ExampleRetryTrigger --message-body "Retry"


</pre>