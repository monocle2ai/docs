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
- Instrument your app code
     - Import the Monocle package
       ```
          from monocle_apptrace.instrumentor import setup_monocle_telemetry
       ```
     - Setup instrumentation in your ```main()``` function  
       ``` 
          setup_monocle_telemetry(workflow_name="your-app-name")
       ```         
