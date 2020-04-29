from flask import Flask, render_template, Response
import time
import json

app = Flask(__name__)
#-------------------------------
# Configuration of the application.
# num_bars: number of progress bars to render
# prog_inc: how mcuh the progress bar increases per update
# update_rate: how frequently to update the progress bar, in seconds
#-------------------------------
class Config:
    num_bars = 3
    prog_inc = 10
    update_rate = 1

# Instantiate app_config
app_cfg = Config

#---------------------------------------
# App Routes
#---------------------------------------

@app.route('/')
def index():
    return render_template('index.html', num_bars = app_cfg.num_bars)

@app.route('/progress')
def progress():
    #vid_dict = {}
    def generate():
        x = 0
        # {'video_1':str(x)}
        while x <= 100:
            #vid_dict['suresh']="0"
            vid_dict = {}
            for bar in range(0,app_cfg.num_bars):
                vid_dict[bar] = min(x+bar*app_cfg.prog_inc,100)
            #yield "data:" + str(x) + "\n\n"
            ret_string = "data:" + json.dumps(vid_dict) + "\n\n"
            print(ret_string)
            yield ret_string
            x = x + 10
            time.sleep(app_cfg.update_rate)

    return Response(generate(), mimetype= 'text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)