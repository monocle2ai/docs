# This guide describes various options to set trace and scopes in your application


### Set scope programatically in python 
```python
from monocle_apptrace import monocle_trace_scope
...
with monocle_trace_scope("Conversation"):
    while True:
        message = input("How can I help you:")
        cleaned_message = gaurdrail_chai(message)
        result = rag_chat_chain.invoke(message)
```
The above code will generate two traces (one per chain invocation). All the spans in these traces will have an attribute called `Conversaion` with a unique value.
```json
"attributes": {
    "span.type": "inference",
    ...
    "scope.conversation": "0xcb80e6f772968ed50ead80657b09cf52",
```

### Set scope programatically in typescript
TBD

### Set scope declaratively
You can set scope via a configuration file at the method level or to track http header, without having to make changes 
