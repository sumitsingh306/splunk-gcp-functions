# Example 3: GCS Function

This example will create 2 PubSub Topics, create the GCS Function with a Retry Function, and a GCS example bucket. A Cloud Schedule is also created to trigger the Retry Function (via PubSub Topic). Note that the Schedule and Retry Trigger and Retry Topic is common between all of examples and doesn't need to be repeated if you build more than one example.


#### PubSub Topics Created:

**ExamplePubSubRetryTopic** : This topic can be common between all functions. This topic will collect failed writes from ExamplePubSub to HEC

**ExampleRetryTrigger** : This topic can be common between all functions and triggers retries based on Cloud Schedule

#### GCP Functions Created:

**ExampleGCS** : GCS Function pulling from an ExampleBucket 

**ExampleRetry** : Retry Function to pull any failed messages from ExamplePubSub (can be re-used across all examples)

## GCS Bucket

**example-bucket-xxxx** : Example GCS Bucket - note you will need to change the name to make sure that the bucket name is globally unique.


## CLI Example Scripts
(run in bash or the Cloud Shell)

**Note that you will need to change values in bold in the scripts below to identify your project id, GCS Bucket, HEC URL and HEC Token**


<pre>

#this section is specific for this example only; give the bucket a global unique id

gsutil mb gs://<strong>example-bucket-xxxx</strong>/


#the clone command only needs to be done once for all of the examples
git clone https://github.com/pauld-splunk/splunk-gcp-functions.git

cd splunk-gcp-functions/GCS

#create function

gcloud functions deploy ExampleGCSFunction --runtime python37 \
  --trigger-bucket=<strong>example-bucket-xxxx</strong> --entry-point=hello_gcs \
  --allow-unauthenticated \
  --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',RETRY_TOPIC='ExamplePubSubRetryTopic'


#This is a common section for all examples
#Doesn't need to be repeated for all unless you wish to have separate PubSub Topics for retrying different events.

gcloud pubsub topics create ExamplePubSubRetryTopic

gcloud pubsub subscriptions create --topic ExamplePubSubRetryTopic ExamplePubSubRetryTopic-sub
cd ../RetryEvent

#create Retry function

gcloud functions deploy ExamplePubSubRetry --runtime python37 \
 --trigger-topic=ExampleRetryTrigger --entry-point=hello_pubsub --allow-unauthenticated \
 --set-env-vars=HEC_URL='<strong>HOSTNAME_OR_IP_FOR_HEC</strong>',HEC_TOKEN='<strong>0000-0000-0000-0000</strong>',PROJECTID='<strong>Project-id</strong>',SUBSCRIPTION='ExamplePubSubRetryTopic-sub'

gcloud pubsub topics create ExampleRetryTrigger

gcloud scheduler jobs create pubsub ExampleRetrySchedule --schedule "*/10 * * * *" --topic ExampleRetryTrigger --message-body "Retry"

</pre>
