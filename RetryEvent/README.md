# GCP Functions Library for Ingesting into Splunk

**Retry Functions**

These functions (two types) periodically requests any failed events that were sent to a PubSub Topic, and re-tries sending to HEC. There are 2 functions, one for the PubSub function, and another for all other functions. If there is a subsequent failure to send to Splunk, the functions will not acknowledge the pull from PubSub, and therefore will be re-tried at a later attempt.

**RetryEvent**
This function periodically requests failed events from the PubSub function.

As the events are originally created as individual events, this function pulls a batch from PubSub and sends to HEC as a batch rather than single events to improve efficiency. 