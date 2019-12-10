# Example Cleanup

The script below cleans up (destructively) the examples created. It assumes that all of the examples have been installed. However, if you wish to only remove partially, then the comments in-line should help identify which section to use

** Warning:
THIS CANNOT BE UNDONE!!! 
Make sure you don't want to keep any remaining data!!!
The following commands also deletes all objects stored within the buckets. These objects cannot be recovered. If you want to avoid accidentally deleting objects, use the gsutil rb command below, which only deletes a bucket if the bucket is empty. **



<pre>

#run this script from where you originally ran the original examples from
#use the same environment variable values as for the example builds

#Example-1 Start
PUBSUB_FUNCTION=ExamplePubSubFunction

PUBSUB_TOPIC=ExamplePubSubLogsTopic
PUBSUB_SINK1=ExampleSinkForFunctions
PUBSUB_SINK2=ExampleSinkNoFunctions
#Example-1 End (note the retry needs to be cleaned up below also)

#Example-2a/b Start
METRICS_FUNCTIONa=ExampleMetricsEventsFunction
METRICS_TRIGGER=ExampleMetricsTriggerTopic
METRICS_SCHEDULE=ExampleMetricsSchedule
METRICS_FUNCTIONb=ExampleMetricsFunction
#Example 2a/b End

#Example 3 Start
GCS_FUNCTION=ExampleGCSFunction
GCS_BUCKET=<strong>example-bucket-xxxx</strong>/
#Example 3 End

#Example 4 Start
ASSETS_FUNCTION=ExampleAssetsFunction

GCS_ASSETS_BUCKET=<strong>example-assets-bucket-xxxx</strong>/
GCS_FUNCTION=ExampleGCSAssetsFunction

ASSETS_SCHEDULE=ExampleAssetsSchedule
ASSETS_TRIGGER_PUBSUB=ExampleAssetsTrigger
#Example 4 End

#Common for all examples#
RETRY_FUNCTON=ExamplePubSubRetry
RETRY_TOPIC=ExamplePubSubRetryTopic
RETRY_SUBSCRIPTION=ExamplePubSubRetryTopic-sub
RETRY_TRIGGER_PUBSUB=ExampleRetryTrigger
RETRY_SCHEDULE=ExampleRetrySchedule
#End of common

#remove git project clone (all examples)
rm -r splunk-gcp-functions

#Example 1
gcloud functions delete $PUBSUB_FUNCTION --quiet
gcloud logging sinks delete $PUBSUB_SINK1 --quiet
gcloud logging sinks delete $PUBSUB_SINK2 --quiet
gcloud pubsub topics delete $PUBSUB_TOPIC --quiet

#Example 2a
gcloud functions delete $METRICS_FUNCTIONa --quiet

#Example 2b
gcloud functions delete $METRICS_FUNCTIONb --quiet

#Examples 2a/2b
gcloud pubsub topics delete $METRICS_TRIGGER --quiet
gcloud scheduler jobs delete $METRICS_SCHEDULE --quiet

#Example 3
gcloud functions delete $GCS_FUNCTION --quiet
gsutil rm -r gs://$GCS_BUCKET

#Example 4
gcloud functions delete $ASSETS_FUNCTION --quiet
gcloud pubsub topics delete $ASSETS_TRIGGER_PUBSUB --quiet
gcloud scheduler jobs delete $ASSETS_SCHEDULE --quiet
gsutil rm -r gs://$GCS_ASSETS_BUCKET 

#Common for All
gcloud functions delete $RETRY_FUNCTON --quiet
gcloud scheduler jobs delete $RETRY_SCHEDULE --quiet
gcloud pubsub subscriptions delete $RETRY_SUBSCRIPTION --quiet
gcloud pubsub topics delete $RETRY_TOPIC --quiet
gcloud pubsub topics delete $RETRY_TRIGGER_PUBSUB --quiet




</pre>

