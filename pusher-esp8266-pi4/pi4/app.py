from flask import Flask ,render_template, jsonify
import paho.mqtt.client as mqtt
import pusher
import time

pusher_client = pusher.Pusher(
  app_id='1262894',
  key='c36ff86c1ec4ca2d7167',
  secret='a3d491e6e3b342777300',
  cluster='ap2',
  ssl=True,
);
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    client.subscribe("esp8266")
    # client.subscribe("/esp8266/humidity")
def on_message(client, userdata, message):
    simplestring  = str(message.payload)
    clearwithbyte = simplestring.strip("b")
    value = float(clearwithbyte.strip("\'"))
    if(value  <= 10 ):
                print('helloworld')
                pusher_client.trigger('my-channel1', 'my-event', {'message': value})
    global redi
    redi=value
    print(value)
def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect('localhost', 1883, 60) 
    # Connect to the MQTT server and process messages in a background thread. 
    mqtt_client.loop_start() 


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',redi=10)
@app.route('/meow')
def ajax():
      main()
      time.sleep(1)
      return jsonify(response=redi)


if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')