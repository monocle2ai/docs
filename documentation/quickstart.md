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
- Option 1. Generate traces from your local application without any instrumentation
```
   python -m monocle_apptrace your-app-name.py
```
- Option 2. Instrument your app code
     - Import the Monocle package
       ```python
          from monocle_apptrace.instrumentation.common.instrumentor import setup_monocle_telemetry
       ```
     - Setup instrumentation in your ```main()``` function  
       ```python
          setup_monocle_telemetry(workflow_name="your-app-name")
       ```         

# Examine the traces
By default Monocle traces are written out to a json file `monocle_trace_<workflow>_<traceID>_<timestamp>.json` in the directory where the application is executed. Checkout this [example](examples/monocle_trace_openai_app_0xfbcf020bcfbaf3e7e3a14b1a87b267a9_2025-03-09_19.10.52.json)