**Normal Flow:**
GCS Object -> GCP Function -> HEC
**Error Flow:** 
GCS Object -> GCP Function -> PubSub error Topic
Cloud Schedule -> PubSub Topic (Trigger) -> GCP Function(->Pull from PubSub error Topic)-> HEC
