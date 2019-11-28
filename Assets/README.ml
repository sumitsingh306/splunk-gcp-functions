# GCP Functions Library for Ingesting into Splunk

**Assets Functions**

This function periodically requests Assets configurations (API Call) and publishes it to a GCS Bucket. The GCS Function can then ingest this content into Splunk via HEC.
The trigger for the Assets function would be done by a Cloud Schedule trigger to a PubSub Topic.
