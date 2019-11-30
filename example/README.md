# Example Configuration build

The following script can be executed in a GCP CLI to build a full sample configuration using all of the functions in this library. The following configuration is created:


#### Log export Sinks:


<table><tr><td><strong>Sink</strong></td><td><strong>Description</strong></td><td><strong>Filter</strong></td></tr>
<tr><td>ExampleSinkFunctions</td><td>Selects all GCP Function logs. Important note that it filters out the PubSub Function!!</td><td>resource.labels.function_name!="GCP-Pub-Sub"</td></tr>
<tr><td>ExampleSinkNoFunctions</td><td>Selects all Kubernetes/containers logs</td><td>protoPayload.serviceName="container.googleapis.com"</td></tr></table>

**Caution: With aggregated export sinks, you can export a very large number of log entries. Design your logs query carefully.**


#### PubSub Topics:

**ExamplePubSubLogsTopic** : This topic will collect logs from the export sinks

**ExamplePubSubRetryTopic** : This topic will collect failed writes from ExamplePubSub to HEC

**ExampleMetricsRetryTopic** : This topic will collect failed writes from ExampleMetricsFunction to HEC

**ExampleEventsRetryTopic** : This topic will collect failed writes from ExampleMetricsEventsFunction and ExampleAssets to HEC

**ExampleRawRetryTopic** : This topic will collect failed writes from ExampleGCSFunction to HEC

#### GCP Functions:

**ExamplePubSub** : PubSub Function pulling from ExamplePubSubLogsTopic 

**ExamplePubSubRetry** : Retry Function to pull any failed messages from ExamplePubSub

**ExampleMetricsFunction** : Function to pull sample of metrics from compute. Formatted as metrics index into HEC

**ExampleMetricsRetryTopic** : Retry Function to pull any failed messages from ExampleMetricsFunction

**ExampleMetricsEventsFunction** : Mirror function to ExampleMetricsFunction, but sending metrics into a Splunk event index

**ExampleEventsRetryFunction** : Retry Function to pull any failed messages from ExampleMetricsEventsFunction

**ExampleAssetFunction** : Function to pull asset information into HEC

#### Cloud Scheduler

**ExampleRetry** : Retry Schedule (10mins)
**ExampleAsset** : Schedule to run Asset list (12hrs)




