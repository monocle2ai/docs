# This cookbook provides receipts of various instrumenation solution with Monocle

## Generate out of box telemetry, without any code chante
If you have a python app that run locally ie ```python my-app.py [args]``` (as opposed to hosting in a cloud serverless container like AWS Lambda or Azure Function), you can use Monocle package to enable telemetry with any code change
```shell
python -m monocle_apptrace my-app.py [args]
```
This will genearate the trace files monocle_trace_*.json in the local directory

## Instrument your app to enable Monocle telemetry
- Python
Install monocle package or add `monocle_telemetry` in your ```requirements.txt``` file.
```shell
pip install monocle_telemetry
```
Import the package and add Monocle a single line of code to enable Monocle telemetry
```python
    from monocle_apptrace import setup_monocle_telemetry
    setup_monocle_telemetry(workflow_name="your-app-name")
```
Now when you run the application, it will generate the trace files `monocle_trace_*.json` in the directory where the application is ran.

- Typescript
Get the Monocle package
  
```shell
    npm install --save monacle2ai
```
Instrument your app code
```js
    const { setupMonocle } = require("monacle2ai")
    setup_monocle_telemetry(workflow_name="your-app-name")
```

## Track application business logic coded in a top level application method/API
Consider a chatbot application with a method called conversation() that implements a chat conversion thread with end user. When the 
```python
...
    def conversation():
    while True:
        ...
        message = input("How can I help you:")
        cleaned_message = gaurdrail_chai(message)   ==> GenAI code
        result = rag_chat_chain.invoke(message)     ==> GenAI code
```

The above code will generate two traces (one per chain invocation). All the spans in these traces will have an attribute called `Conversaion` with a unique value.
```json
"attributes": {
    "span.type": "inference",
    ...
    "scope.conversation": "0xcb80e6f772968ed50ead80657b09cf52",
```