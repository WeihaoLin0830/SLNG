# Reflection Questions

## 1. Biggest decision and what I would do differently with a full day

The biggest decision I made was to keep the gateway and the two fake providers as three separate FastAPI servers. This made the exercise closer to a real service-to-service architecture, where the gateway talks to external providers through HTTP instead of calling local functions. With a full day, I would improve the structure to keep the modules cleaner, using environment variables for provider URLs and moving mappings out of the gateway endpoint file. I would also add more specific and automated error handling to make the implementation easier to extend when adding new providers.


## 2. Most confusing or frustrating part

The most confusing and frustrating part was having to research and understand concepts that were new to me. I had to learn how a REST API is structured, how different services connect through different ports, and how endpoints are defined. Another confusing part was deciding how to handle AccurateSTT's `duration_sec` field, because the gateway response requires `processing_time_ms`, in the end, I decided to measure the provider call directly in the gateway and use that value as the processing time.


## 3. Three things I would change first to add a third provider

First, I would move provider URLs and provider names into a central configuration so they are not hardcoded inside the endpoint logic. Second, I would create separate adapter functions or classes for each provider, with one place for building payloads and normalizing responses. Third, I would create the new fake provider server and its matching gateway adapter, then add specific tests to verify the new provider works without breaking the existing FastTranscribe and AccurateSTT behavior.
