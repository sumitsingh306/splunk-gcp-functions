# Example 1: PubSub

This example will create 2 example Log Export Sinks, 3 PubSub Topics and use the PubSub Function with a Retry Function. A Cloud Schedule is also created to trigger the Retry Function (via PubSub Topic). Note that the Schedule and Retry Trigger and Retry Topic is common between all of examples and doesn't need to be repeated if you build more than one example.

#### Log export Sinks Created:

<table><tr><td><strong>Sink</strong></td><td><strong>Description</strong></td><td><strong>Filter</strong></td></tr>
<tr><td>ExampleSinkFunctions</td><td>Selects all GCP Function logs. Important note that it filters out the PubSub Function!!</td><td>resource.labels.function_name!="ExamplePubSub"</td></tr>
<tr><td>ExampleSinkNoFunctions</td><td>Selects all Kubernetes/containers logs</td><td>protoPayload.serviceName="container.googleapis.com"</td></tr></table>

**Caution: With aggregated export sinks, you can export a very large number of log entries. Design your logs query carefully.**


#### PubSub Topics Created:

**ExamplePubSubLogsTopic** : This topic will collect logs from the export sinks

**ExamplePubSubRetryTopic** : This topic can be common between all functions. This topic will collect failed writes from ExamplePubSub to HEC

**ExampleRetryTrigger** : This topic can be common between all functions and triggers retries based on Cloud Schedule

#### GCP Functions Created:

**ExamplePubSub** : PubSub Function pulling from ExamplePubSubLogsTopic 

**ExampleRetry** : Retry Function to pull any failed messages from ExamplePubSub (can be re-used across all examples)


## CLI Example Scripts
(run in bash or the Cloud Shell)

**Note that you will need to change values in bold in the scripts below to identify your project id, Log-Sink Service Account, HEC URL and HEC Token**


<pre>

#this section is specific for this example only

gcloud pubsub topics create ExamplePubSubTopic

#create log-sinks...

gcloud logging sinks create ExampleSinkForFunctions \
  pubsub.googleapis.com/projects/<strong>MY-PROJECT</strong>/topics/ExamplePubSubLogsTopic \
  --log-filter="resource.labels.function_name!=ExamplePubSub"

gcloud logging sinks create ExampleSinkNoFunctions \
  pubsub.googleapis.com/projects/<strong>MY-PROJECT</strong>/topics/ExamplePubSubLogsTopic \
  --log-filter="protoPayload.serviceName=container.googleapis.com"

gcloud pubsub topics add-iam-policy-binding ExamplePubSubLogsTopic \
  --member serviceAccount:<strong>LOG-SINK-SERVICE-ACCOUNT</strong> --role roles/pubsub.publisher

#the clone command only needs to be done once for all of the examples
git clone https://github.com/pauld-splunk/splunk-gcp-functions.git

cd splunk-gcp-functions/PubSubFunction

#create function

gcloud functions deploy ExamplePubSubFunction --runtime python37 \
  --trigger-topic=ExamplePubSubLogsTopic --entry-point=hello_pubsub \
  --allow-unauthenticated \
  --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',RETRY_TOPIC='ExamplePubSubRetryTopic'


#This is a common section for all examples
#Doesn't need to be repeated for all unless you wish to have separate PubSub Topics for retrying different events.

gcloud pubsub topics create ExamplePubSubRetryTopic

gcloud pubsub subscriptions create --topic ExamplePubSubRetryTopic ExamplePubSubRetryTopic-sub
cd ../Retry

#create Retry function

gcloud functions deploy ExamplePubSubRetry --runtime python37 \
 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated \
 --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',SUBSCRIPTION='ExamplePubSubRetryTopic-sub'

gcloud pubsub topics create ExampleRetryTrigger

gcloud scheduler jobs create pubsub ExampleRetrySchedule --schedule "*/10 * * * *" --topic ExampleRetryTrigger --message-body "Retry"

</pre>
