#GCP Functions Library for Ingesting into Splunk

This library contains GCP Function Templates to read from:
- PubSub
- Metrics
- Google Cloud Storage
- Assets

**PubSubFunction**

This function pulls any event that is posted into PubSub and packages it up into a Splunk event. The event is then sent to the Http Event Collector (HEC). The function is written such that the event format can be sent compatible with Splunk's Add-On for Google Cloud Platform (https://splunkbase.splunk.com/app/3088/).
If any faiures occur during sending the message to HEC, the event is posted back to a Pub-Sub Topic. A recovery function is provided which is executed via a Cloud Scheduler trigger (PubSub). The recovery function will attempt to clear out the PubSub retry topic and send these events into HEC.

**MetricsFunction**

This function is triggered by a Cloud Scheduler trigger (via PubSub). The function calls Stackdriver Monitoring APIs to retrieve the metrics (metrics request list, and poll frequency set in environment variable). These metrics are then sent to Splunk HEC. Two formats are supported - one to be compatible with the Add-on for GCP, sending the metrics as events into Splunk, the second is sent as a metric into Splunk's Metrics index.
As with the PubSub Function, any failed messages are sent into a PubSub topic for retry. A recovery function will attempt to resend periodically.

**Google Cloud Storage**

This function triggers on objects being written to a GCS Bucket. The bucket is set in when defining the function settings. All of the contents from the bucket is sent to HEC in batches of events – an event delimiter/breaker regex should be set in a function environment variable so that the function can break up the batches in the appropriate places. The batches are formed so that it can achieve an even event distribution across indexers (otherwise all of the content would go into 1 indexer). Code variables can be configured within the template to adjust the batch size. The Splunk HEC token should be created with the appropriate sourcetype for the events, as well as the index, as the events are not re-formatted/procecessed in any way.
Any messages that failed to be sent to HEC are sent into a PubSub topic for retry. A recovery function will attempt to resend periodically.

**Assets**

This function is periodically triggered via a Cloud Scheduler push to a PubSub topic. The function calls GCP’s API to retrieve the cloud asset list. The list is written to a GCS bucket. (bucket location is defined in an environment variable).
Once in the GCS Bucket, the GCS function above can be used to read in the contents of the asset list into Splunk.



