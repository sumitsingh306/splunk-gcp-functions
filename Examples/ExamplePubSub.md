# Example 1: PubSub

This example will create 2 example Log Export Sinks, 2 PubSub Topics and use the PubSub Function with a Retry Function. A Cloud Schedule is also created to trigger the Retry Function (via PubSub Topic). Note that this Schedule and Topic is common between all of examples and doesn't need to be repeated if you build more than one example.

#### Log export Sinks Created:

<table><tr><td><strong>Sink</strong></td><td><strong>Description</strong></td><td><strong>Filter</strong></td></tr>
<tr><td>ExampleSinkFunctions</td><td>Selects all GCP Function logs. Important note that it filters out the PubSub Function!!</td><td>resource.labels.function_name!="ExamplePubSub"</td></tr>
<tr><td>ExampleSinkNoFunctions</td><td>Selects all Kubernetes/containers logs</td><td>protoPayload.serviceName="container.googleapis.com"</td></tr></table>

**Caution: With aggregated export sinks, you can export a very large number of log entries. Design your logs query carefully.**


#### PubSub Topics Created:

**ExamplePubSubLogsTopic** : This topic will collect logs from the export sinks

**ExamplePubSubRetryTopic** : This topic will collect failed writes from ExamplePubSub to HEC


#### GCP Functions Created:

**ExamplePubSub** : PubSub Function pulling from ExamplePubSubLogsTopic 

**ExamplePubSubRetry** : Retry Function to pull any failed messages from ExamplePubSub


## CLI Example Scripts
(run in bash or the Cloud Shell)

**Note that you will need to change values in bold in the scripts below to identify your project id, Log-Sink Service Account, HEC URL and HEC Token**
<pre>
gcloud pubsub topics create ExamplePubSubRetryTopic

gcloud pubsub subscriptions create --topic ExamplePubSubRetryTopic ExamplePubSubRetryTopic-sub

gcloud pubsub topics create ExampleEventsRetryTopic

gcloud pubsub subscriptions create --topic ExampleEventsRetryTopic ExampleEventsRetryTopic-sub

gcloud logging sinks create ExampleSinkForFunctions pubsub.googleapis.com/projects/**MY-PROJECT**/topics/ExamplePubSubLogsTopic \
     --log-filter="resource.labels.function_name!=ExamplePubSub"

gcloud logging sinks create ExampleSinkNoFunctions pubsub.googleapis.com/projects/**MY-PROJECT**/topics/ExamplePubSubLogsTopic \
     --log-filter="protoPayload.serviceName=container.googleapis.com"

gcloud pubsub topics add-iam-policy-binding ExamplePubSubLogsTopic \
     --member serviceAccount:<strong>LOG-SINK-SERVICE-ACCOUNT</strong> --role roles/pubsub.publisher

git clone https://github.com/pauld-splunk/splunk-gcp-functions.git

cd splunk-gcp-functions/PubSubFunction

gcloud functions deploy ExamplePubSubFunction --runtime python37 --trigger-topic=ExamplePubSubLogsTopic --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',RETRY_TOPIC='ExamplePubSubRetryTopic'

cd ../RetryEvent

gcloud functions deploy ExamplePubSubRetry --runtime python37 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',SUBSCRIPTION='ExamplePubSubRetryTopic-sub'

# This section only needs to be done once for all examples

gcloud pubsub topics create ExampleRetryTrigger

</pre>
