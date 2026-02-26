---
layout: default
---

# Instrument TypeScript GenAI code
- Get the Monocle package
  
```
    npm install --save monacle2ai
```
- Instrument your app code
```js
    const { setupMonocle } = require("monacle2ai")
    setup_monocle_telemetry(workflow_name="your-app-name")
```

# Instrument Python GenAI code
- Get the Monocle package
  
```
    pip install monocle_apptrace 
```
- Option 1. Generate traces from your local application without any instrumentation when you control how to run the application.
```
   python -m monocle_apptrace your-app-name.py
```
- Option 2. Instrument your app code if it's hosted where you don't control the runtime (eg serverless functions like AWS Lambda)
     - Import the Monocle package
       ```python
          from monocle_apptrace.instrumentation.common.instrumentor import setup_monocle_telemetry
       ```
     - Setup instrumentation in your ```main()``` function  
       ```python
          setup_monocle_telemetry(workflow_name="your-app-name")
       ```         

# Examine the traces
By default Monocle traces are written out to a json file `monocle_trace_<workflow>_<traceID>_<timestamp>.json` in the directory where the application is executed. Checkout this [example](./examples/monocle_trace.json)

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=18f8082a-587b-41a3-976b-0117380fa4dd&page=quickstart" />
