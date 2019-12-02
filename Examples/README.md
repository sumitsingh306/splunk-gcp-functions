# Example Configuration builds

The files here contain scripts can be executed in a GCP CLI to build a full sample configurations using all of the functions in this library. The following configurations are created:
(Note that there are some common sections for these examples, which do not need to be re-run if one of the other examples has been created. This is noted in the scripts)

## Example 1: PubSub 

This example will create 2 example Log Export Sinks, 2 PubSub Topics and use the PubSub Function with a Retry Function. A Cloud Schedule is also created to trigger the Retry Function (via PubSub Topic). Note that this Schedule and Topic is common between all of examples and doesn't need to be repeated if you build more than one example.

## Example 2a: Metrics Collection (Event Index)

This example will create a Cloud Schedule which triggers the Metrics Function (via a PubSub Topic). The function will send the metrics into Splunk HEC as an Event format (into an Event index). The script will also create a retry PubSub Topic, and set up a Function to retry any failed messages to HEC. 
If you have already created any other examples, the Cloud Schedule and PubSub Trigger topic doesn't need to be re-created.

## Example 2b: Metrics Collection (Metrics Index)

This example is a clone of example 2a, but this function will send the metrics into Splunk's Metrics Index. It creates a Cloud Schedule which triggers the Metrics Function (via a PubSub Topic). The script will also create a retry PubSub Topic, and set up a Function to retry any failed messages to HEC.
Note that in practice, only one Cloud Schedule would be needed for metrics unless there is a need to have different schedules/intervals. If you want to run both examples, the section to create the Cloud Schedule for Metrics and its trigger PubSub Topic can be ignored. In the same way, if you have already created any other examples, the Cloud Schedule and PubSub Trigger topic doesn't need to be re-created.


## Example 3: GCS

This example creates a Function that is trigged by an object being created in GCS. The script also creates a Retry Topic for any failed messages to Splunk HEC. A Retry Function is created to send any failed messages. It will also create a Cloud Schedule and PubSub Trigger - if you have already created any other examples, these don't need to be re-created.


## Example 4: Assets

The example creates a function to collect asset information periodically, writing this into a GCS Bucket. The function is triggered by a PubSub Topic (called via Cloud Schedule). The example also builds a GCS Function as per Exanmple 3 to collect this asset data and post to Splunk.


#### Log export Sinks:


<table><tr><td><strong>Sink</strong></td><td><strong>Description</strong></td><td><strong>Filter</strong></td></tr>
<tr><td>ExampleSinkFunctions</td><td>Selects all GCP Function logs. Important note that it filters out the PubSub Function!!</td><td>resource.labels.function_name!="ExamplePubSub"</td></tr>
<tr><td>ExampleSinkNoFunctions</td><td>Selects all Kubernetes/containers logs</td><td>protoPayload.serviceName="container.googleapis.com"</td></tr></table>

**Caution: With aggregated export sinks, you can export a very large number of log entries. Design your logs query carefully.**


#### PubSub Topics:

**ExamplePubSubLogsTopic** : This topic will collect logs from the export sinks

**ExamplePubSubRetryTopic** : This topic will collect failed writes from ExamplePubSub to HEC

**ExampleMetricsRetryTopic** : This topic will collect failed writes from ExampleMetricsFunction to HEC

**ExampleEventsRetryTopic** : This topic will collect failed writes from ExampleMetricsEventsFunction and ExampleAssets to HEC

**ExampleRawRetryTopic** : This topic will collect failed writes from ExampleGCSFunction to HEC

**ExampleAssetsRetryTopic** : This topic will collect failed writes from ExampleAssetFunction to HEC

#### GCP Functions:

**ExamplePubSub** : PubSub Function pulling from ExamplePubSubLogsTopic 

**ExamplePubSubRetry** : Retry Function to pull any failed messages from ExamplePubSub

**ExampleMetricsFunction** : Function to pull sample of metrics from compute. Formatted as metrics index into HEC

**ExampleMetricsRetryFunction** : Retry Function to pull any failed messages from ExampleMetricsFunction

**ExampleMetricsEventsFunction** : Mirror function to ExampleMetricsFunction, but sending metrics into a Splunk event index

**ExampleEventsRetryFunction** : Retry Function to pull any failed messages from ExampleMetricsEventsFunction

**ExampleGCSFunction** : Function to pull sample objects from a bucket

**ExampleGCSRetryFunction** : Function to retry failed messages from ExampleGCSFunction

**ExampleAssetFunction** : Function to pull asset information into HEC

**ExampleAssetsRetryFunction**: Function to retry failed assets write to HEC

#### Cloud Scheduler

**ExampleRetry** : Retry Schedule (10mins)
**ExampleAsset** : Schedule to run Asset list (12hrs)


## GCloud CLI Example

(run in bash or the Cloud Shell)

**Note that you will need to change values in bold in the scripts below to identify your project id, Log-Sink Service Account, HEC URL and HEC Token**

gcloud pubsub topics create ExamplePubSubRetryTopic

gcloud pubsub subscriptions create --topic ExamplePubSubRetryTopic ExamplePubSubRetryTopic-sub

gcloud pubsub topics create ExampleMetricsTriggerTopic

gcloud pubsub topics create ExampleMetricsRetryTopic

gcloud pubsub subscriptions create --topic ExampleMetricsRetryTopic ExampleMetricsRetryTopic-sub

gcloud pubsub topics create ExampleEventsRetryTopic

gcloud pubsub subscriptions create --topic ExampleEventsRetryTopic ExampleEventsRetryTopic-sub

gcloud pubsub topics create ExampleRawRetryTopic

gcloud pubsub subscriptions create --topic ExampleRawRetryTopic ExampleRawRetryTopic-sub

gcloud pubsub topics create ExampleAssetsRetryTopic

gcloud pubsub subscriptions create --topic ExampleAssetsRetryTopic ExampleAssetsRetryTopic-sub

gcloud pubsub topics create ExampleRetryTrigger

gcloud logging sinks create ExampleSinkFunctions pubsub.googleapis.com/projects/**MY-PROJECT**/topics/ExamplePubSubLogsTopic \
     --log-filter="resource.labels.function_name!=ExamplePubSub"

gcloud logging sinks create ExampleSinkNoFunctions pubsub.googleapis.com/projects/**MY-PROJECT**/topics/ExamplePubSubLogsTopic \
     --log-filter="protoPayload.serviceName=container.googleapis.com"

gcloud pubsub topics add-iam-policy-binding ExamplePubSubLogsTopic \
     --member serviceAccount:**LOG-SINK-SERVICE-ACCOUNT** --role roles/pubsub.publisher

git clone https://github.com/pauld-splunk/splunk-gcp-functions.git

cd splunk-gcp-functions/PubSubFunction

gcloud functions deploy ExamplePubSubFunction --runtime python37 --trigger-topic=ExamplePubSubLogsTopic --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',RETRY_TOPIC='ExamplePubSubRetryTopic'

cd ../RetryEvent

gcloud functions deploy ExamplePubSubRetry --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',SUBSCRIPTION='ExamplePubSubRetryTopic-sub'

cd ../Metrics

gcloud functions deploy ExampleMetricsFunction --runtime python37 --trigger-topic=ExampleMetricsTriggerTopic --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',METRICS_LIST='["compute.googleapis.com/instance/cpu/utilization","compute.googleapis.com/instance/disk/read_ops_count","compute.googleapis.com/instance/disk/write_bytes_count","compute.googleapis.com/instance/disk/write_ops_count","compute.googleapis.com/instance/network/received_bytes_count","compute.googleapis.com/instance/network/received_packets_count","compute.googleapis.com/instance/network/sent_bytes_count","compute.googleapis.com/instance/network/sent_packets_count","compute.googleapis.com/instance/uptime"]',TIME_INTERVAL='5',RETRY_TOPIC='ExampleMetricsRetryTopic',METRIC_INDEX_TYPE=METRICS

gcloud functions deploy ExampleMetricsEventsFunction --runtime python37 --trigger-topic=ExampleMetricsTriggerTopic --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',METRICS_LIST='["compute.googleapis.com/instance/cpu/utilization","compute.googleapis.com/instance/disk/read_ops_count","compute.googleapis.com/instance/disk/write_bytes_count","compute.googleapis.com/instance/disk/write_ops_count","compute.googleapis.com/instance/network/received_bytes_count","compute.googleapis.com/instance/network/received_packets_count","compute.googleapis.com/instance/network/sent_bytes_count","compute.googleapis.com/instance/network/sent_packets_count","compute.googleapis.com/instance/uptime"]',TIME_INTERVAL='5',RETRY_TOPIC='ExampleEventsRetryTopic'

cd ../RetryBatch

gcloud functions deploy ExampleMetricsRetryFunction --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',SUBSCRIPTION='ExampleMetricsRetryTopic-sub',EVENT_TYPE='METRIC'

gcloud functions deploy ExampleEventsRetryFunction --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',SUBSCRIPTION='ExampleEventsRetryTopic-sub',EVENT_TYPE='EVENT'

gcloud functions deploy ExampleGCSRetryFunction --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',SUBSCRIPTION='ExampleRawRetryTopic-sub',EVENT_TYPE='RAW'

gcloud functions deploy ExampleAssetsRetryFunction --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',SUBSCRIPTION='ExampleAssetsRetryTopic-sub',EVENT_TYPE='EVENT'

cd ../GCS

gcloud functions deploy ExampleGCSFunction --runtime python37 --trigger-bucket=**TRIGGER_BUCKET** --entry-point=hello_gcs --allow-unauthenticated --set-env-vars=HEC_URL='**HOSTNAME_OR_IP_FOR_HEC**',HEC_TOKEN='**0000-0000-0000-0000**',PROJECTID='**Project-id**',RETRY_TOPIC='ExampleRawRetryTopic'

cd ../Assets












