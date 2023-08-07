from flask import Flask, Response, jsonify, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

api_key='' # Your API-Key
url="https://weatherapi-com.p.rapidapi.com/current.json"

headers = {
    "X-RapidAPI-Key" : api_key,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

@app.route("/getCurrentWeather",methods=['POST'])
def get_current_weather():
    try:
        input = request.json
        #print(request.json)
        if 'city' in input and 'output_format' in input :
            city = input['city']
            output_format = input['output_format']
        else :
            return jsonify({'error':'Invalid JSON data. Missing Parameters'}),400 
        
        querystring = {"q":city}
        output = {}
        response = requests.get(url,headers=headers,params= querystring)
        response_json = response.json()
        latitude = response_json.get('location').get('lat')
        longitude = response_json.get('location').get('lon')
        country = response_json.get('location').get('country')
        weather = response_json.get('current').get('temp_c')
        output["Weather"] = str(weather)+" C"
        output["Latitude"] = latitude
        output["Longitude"] = longitude
        output["City"] = city.capitalize() + " " + country
        if output_format == 'json':
            return jsonify(output)
        elif output_format == 'xml':
            root = ET.Element('root')
            for key, value in output.items():
                if key == "Weather":
                    elem = ET.SubElement(root,"Temperature")
                else :
                    elem = ET.SubElement(root, key)
                if key == "City":
                    elem.text= str(value.split()[0])
                else :
                    elem.text = str(value)
            xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
            xml_output = xml_declaration + ET.tostring(root,encoding='utf-8').decode('utf-8')
            return Response(xml_output, content_type='application/xml')
        else :
            return jsonify({'error':'Invalid Output Format'}),500
        
    except Exception as e:
         print(e)
         return jsonify({'error':'Invalid JSON data'}),500

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5432)