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

## Combining multiple APIs under single traceID
By default monocle instrumetation will generate traces for every chain or API call that your application. If you want to combine some traces for multiple APIs under a single traceID, 
- Use `start_trace()` and `stop_trace()` APIs
```python
token = start_trace()
try:
    embedding_api()
    inferece_api()
finally:
    stop_trace(token)
```
- Wrapp the code under `monocle_trace`
```python
with monocle_trace():
    embedding_api()
    inferece_api()


## Track application business logic coded in a top level application method/API
Consider a chatbot application with a method called conversation() that implements a chat conversion thread with end user. This method in turn calls other APIs like OpenAI and Langchain to use LLMs and generate responses.
```python
...
    def conversation():
        ...
        message = input("How can I help you:")
        cleaned_message = response = openai.chat.completions.create(message)    ==> GenAI code
        result = rag_chat_chain.invoke(cleaned_message)                         ==> GenAI code
```
By default monocle instrumetation will generate a unique trace ID for every chain or API call that your application. This is very useful to track how your app is using the GenAI services. However, that's often not sufficient. As an app developer or owner, you might want to look at bigger picture from the logic or business context. For example, you want to look at the prompts or latency etc at the conversion level than API level. Monocle has this notion of [scopes](Monocle_User_Guide.md#scopes) which allows to you tie multiple traces/spans under a unique id so you can group it.
- Enableing scope programatically at method level
```python
    with monocle_trace_scope("conversation"):
        message = input("How can I help you:")
        cleaned_message = response = openai.chat.completions.create(message)    ==> GenAI code
        result = rag_chat_chain.invoke(cleaned_message)                         ==> GenAI code
```
- By adding a decorator `monocle_trace_scope_method` to this `conversation()` method
```python
@monocle_trace_scope_method("conversation")
def conversation():
...
```
- Configuraging the method name in ```monocle_scope.json``` file that's placed in the working directory of the application
```json
    {
        "package": "myapp.bot",
        "object": "chat",
        "method": "conversation",
        "scope_name": "conversation"
    }
```
The above code will generate two traces (one per chain invocation). All the spans in these traces will have an attribute called `conversaion` with a unique value.
```json
"attributes": {
    "span.type": "inference",
    ...
    "scope.conversation": "0xcb80e6f772968ed50ead80657b09cf52",
```

## Build on existing application logic to capture scope
Imagine you have a chatbot where the frontend app is running in browser and the backend gen AI code is running in a REST framework like Flask or hosted in serverless cloud service like Azure function or AWS Lambda. Let's say that the application has a notion of conversaions, a chat thread that goes between end user and chatbot. A conversation IDs is genearted in the frontend to track each conversions and for sent as a REST header to stateless backend to retrieve the right context. Monocle enables you to track this conversation ID as a scope so all the gen AI APIs called during a conversation are marked with this unique conversation ID.
- GenAI code running in the Flask
Monocle support Flask instrumentation out of the box. All you need to do is to add `setup_monocle_telemetry()` in your flask app and specify the http headers you want to track in the `monocle_scope.json` file
```python
from flask import Flask, request, jsonify
from monocle_apptrace.instrumentation.common.instrumentor import setup_monocle_telemetry

web_app = Flask(__name__)
setup_monocle_telemetry(workflow_name = "my-chatbot-webapp")

def main():
    web_app.run(host="0.0.0.0", port=8096, debug=False)

@web_app.route('/chat',methods = ["POST"])
def chat():
    try:
        coversation_id= request.headers["coversation-id"]
        question = request.args["question"]
        response = chat(question, coversation_id)
        return response

```
Save the `monocle_scope.json` in the folder where you run the Flask application
```json
    {
        "http_header": "client-id",
        "scope_name": "conversation"
    }
```
The above code will generate two traces (one per chain invocation). All the spans in these traces will have an attribute called `conversaion` with a unique value.
```json
"attributes": {
    "span.type": "inference",
    ...
    "scope.conversation": "conversion-id: 0xcb80e6f772968ed50ead80657b09cf52",
```

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=18f8082a-587b-41a3-976b-0117380fa4dd&page=Monocle_Cookbook_python" />
