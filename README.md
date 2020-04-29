A simple Flask application to show how to render multiple progress bars. 
## Concept
The application uses Flask framework to build the web application. The main technique used is to open a server-sent-event connection using [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) API. Once the web connection is established, and the client renders index.html page, it opens an SSE with the server to get events. Server sends a stream of text to the client. Client side JavaScript code updates the corresponding html elements to update the progress bar.

## Details
### Routes
1. '/' for the home page, and index page
2. '/progress' for EventSource to connect to. One can choose any name for this route, but the same name should be used in JavaScript when establishing SSE

### html
We will use BootStrap progress bar elements to render progress bars. One can find more details here:  https://getbootstrap.com/docs/4.4/components/progress/
Since we want to parameterize how many progress bars to render, we will pass that as argument to the render_template for index.html route.
```
{% for bar in range(0,num_bars) %}
    <div class="progress" style="width: 50%; margin: 50px;" >
        <div class="progress-bar progress-bar-striped " role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%" id="prog_{{bar}}">
            <span class="progress-bar-label" id="prog_{{bar}}_label">0%</span>
        </div>
    </div>
{% endfor %}

```
Note the `id=` labels for progress-bar, and progress-bar-label css elements. These will come handy to get access to by the JavaScript.
The main elements to set values are:
- aria-valuenow, and width for progress-bar element
- progress-bar-label for each of them

### JavaScript
```
var source = new EventSource("/progress");
```
establishes the SSE connection to the server
```
source.onmessage = function(event) {
    ...
}
```
is the function that gets called whenever server sends a message to the client.

The data sent from the server is of the form:
```
data: {'0': value_0, '1':value_1,'2':value_2}
```
where value_x indicates the progress of the stream x

We close the SSE connection when all the progress bars reach 100%
