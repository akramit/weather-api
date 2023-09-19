import requests
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


api_key = ''  # Your API-Key
url = "https://weatherapi-com.p.rapidapi.com/current.json"

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}


def get_xml_output(output):
    root = ET.Element('root')
    for key, value in output.items():
        elem = ET.SubElement(root, key if key != "Weather" else "Temperature")
        elem.text = str(value.split()[0]) if key == "City" else str(value)
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    xml_output = (
        xml_declaration + ET.tostring(root, encoding='utf-8').decode('utf-8')
    )

    return xml_output


@app.route("/",methods=['GET'])
def index():
    return "<marquee> <Big> Hello World !!! </Big> </marquee>"

@app.route("/getCurrentWeather", methods=['POST'])
def get_current_weather():
    try:
        input_data = request.json

        if 'city' in input_data and 'output_format' in input_data:
            city = input_data['city']
            output_format = input_data['output_format']
        else:
            return (
                jsonify({'error': 'Invalid JSON data. Missing Parameters'}),
                400
            )

        querystring = {"q": city}
        output = {}
        response = requests.get(url, headers=headers, params=querystring)
        response_json = response.json()
        location = response_json.get('location')
        current = response_json.get('current')

        latitude = location.get('lat')
        longitude = location.get('lon')
        country = location.get('country')
        weather = current.get('temp_c')

        output["Weather"] = str(weather) + " C"
        output["Latitude"] = latitude
        output["Longitude"] = longitude
        output["City"] = city.capitalize() + " " + country

        if output_format == 'json':
            return jsonify(output)
        elif output_format == 'xml':
            xml_output = get_xml_output(output)
            return Response(xml_output, content_type='application/xml')
        else:
            return jsonify({'error': 'Invalid Output Format'}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid JSON data'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432)
