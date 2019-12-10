# Example Cleanup

The script below cleans up (destructively) the examples created. 

## Warning
**THIS CANNOT BE UNDONE!!!** 
Make sure you don't want to keep any remaining data!!!
The following commands also deletes all objects stored within the buckets. These objects cannot be recovered. If you want to avoid accidentally deleting objects, use the replace gsutil rm with the gsutil rb command below, which only deletes a bucket if the bucket is empty.


Update the Highlighted items, and save as a shell script (e.g. cleanup.sh). 
Before running the script make sure you set permissions eg <pre>chmod +x cleanup.sh</pre> 
To run the script, use the example number as the script argument :
for example 1 use <pre>./cleanup.sh 1 </pre> 
example 2a use <pre>./cleanup.sh 2b</pre> 
both example 2a and 2b use <pre>./cleanup.sh 2</pre> 
example 3 <pre>./cleanup.sh 3</pre> etc. 
To clean up all use <pre>./cleanup.sh ALL</pre> or just <pre>./cleanup.sh</pre> 


``
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


case $1 in
	1) 
		CLEAN=1
		;;
	2a)
    	CLEAN=2
    	;;
    2b)
    	CLEAN=3
    	;;
    2)
    	CLEAN=4
    	;;
    3)
    	CLEAN=5
    	;;
    4)
    	CLEAN=6
    	;;
    ALL)
    	CLEAN=0
    	;;
    *)
    	CLEAN=0
    	;;
esac

#Example 1
if [$CLEAN=1] || [ $CLEAN = 0 ]
then
	gcloud functions delete $PUBSUB_FUNCTION --quiet
	gcloud logging sinks delete $PUBSUB_SINK1 --quiet
	gcloud logging sinks delete $PUBSUB_SINK2 --quiet
	gcloud pubsub topics delete $PUBSUB_TOPIC --quiet
fi

#Example 2a
if [ $CLEAN -eq 2 ] || [ $CLEAN -eq 4 ] || [ $CLEAN -eq 0 ]
then
	gcloud functions delete $METRICS_FUNCTIONa --quiet
fi

#Example 2b
if [ $CLEAN -eq 3 ] || [ $CLEAN -eq 4 ] || [ $CLEAN -eq 0 ]
then
	gcloud functions delete $METRICS_FUNCTIONb --quiet
fi

#Examples 2a/2b
if [ $CLEAN -eq 2 ] || [ $CLEAN -eq 3 ] || [ $CLEAN -eq 4 ] || [ $CLEAN -eq 0 ]
then
	gcloud pubsub topics delete $METRICS_TRIGGER --quiet
	gcloud scheduler jobs delete $METRICS_SCHEDULE --quiet
fi

#Example 3
if [ $CLEAN -eq 5 ] || [ $CLEAN -eq 0 ]
then
	gcloud functions delete $GCS_FUNCTION --quiet
	gsutil rm -r gs://$GCS_BUCKET
fi

#Example 4
if [ $CLEAN -eq 6 ] || [ $CLEAN -eq 0 ]
then
	gcloud functions delete $ASSETS_FUNCTION --quiet
	gcloud pubsub topics delete $ASSETS_TRIGGER_PUBSUB --quiet
	gcloud scheduler jobs delete $ASSETS_SCHEDULE --quiet
	gsutil rm -r gs://$GCS_ASSETS_BUCKET 
fi

#Common for All
gcloud functions delete $RETRY_FUNCTON --quiet
gcloud scheduler jobs delete $RETRY_SCHEDULE --quiet
gcloud pubsub subscriptions delete $RETRY_SUBSCRIPTION --quiet
gcloud pubsub topics delete $RETRY_TOPIC --quiet
gcloud pubsub topics delete $RETRY_TRIGGER_PUBSUB --quiet

``

