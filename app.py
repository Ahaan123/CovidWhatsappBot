from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    formed_message = ""
    json_data = requests.get('https://coronavirus-19-api.herokuapp.com/countries')
    parsed_json = json.loads(json_data.text)
    for json_object in parsed_json:
        if json_object['country'].lower() == str(msg).lower():
            formed_message = 'Country: ' + str(json_object['country']) + "\n" "Cases: " + str(
                json_object['cases']) + "\n" "Today Cases: " + str(json_object['todayCases']) + "\n" + "Deaths: " + str(
                json_object['deaths']) + "\n" + "Today Deaths: " + str(
                json_object['todayDeaths']) + "\n" + "Recovered: " + str(
                json_object['recovered']) + "\n" + "Active Cases: " + str(json_object['active']) + "\n" + "**Powered by Ahaan Pandya's Covid Bot**"

            break
        else:
            formed_message = 'Sorry, the country could not be found.'

    state_json_data = requests.get('https://api.covid19india.org/data.json')
    state_parsed_json = json.loads(state_json_data.text)
    state_data = state_parsed_json['statewise']
    for state in state_data:
        if state['state'].lower() == str(msg).lower():
            formed_message = 'State: '+str(state['state'])+'\n'+'Cases: '+str(state['confirmed'])+'\n'+'Deaths: '+str(state['deaths'])+'\n'+'Today Cases: '+str(state['deltaconfirmed'])+'\n'+'Today Deaths: '+str(state['deltadeaths'])+'\n'+'Recovered: '+str(state['recovered'])+'\n'+'Active cases: '+str(state['active'])+'\n'+"**Powered by Ahaan Pandya's Covid Bot**"
            break
    

    resp = MessagingResponse()
    resp.message(formed_message)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)


