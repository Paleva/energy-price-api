import requests
import xml.etree.ElementTree as ET

def get_energy_price(api_key, in_domain, out_domain, time_interval):
    """

    Get Energy Price from Entsoe API
    
    :param api_key: Your Entsoe API key
    :param in_domain: Input domain
    :param out_domain: Output domain
    :param time_interval: Time interval (ISO format e.g. 2016-01-01T00:00Z/2016-01-02T00:00Z (slash and colon have to be escaped in case of Get method)
    :return response: XML response
    """
    URL = 'https://web-api.tp.entsoe.eu/api?'
    
    params = {
        'securityToken': api_key,
        'documentType': 'A44',
        'in_Domain': in_domain,
        'out_Domain': out_domain,
        'timeInterval': time_interval
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        open('price.xml', 'w').write(response.text)
        return ET.fromstring(response.text)
    else:
        raise Exception('Error: ' + response.reason)

def get_energy_generation(api_key, in_domain, time_interval):
    """
    
    Get Energy Generation By Type from Entsoe API

    :param api_key: Your Entsoe API key
    :param in_domain: Input domain
    :param time_interval: Time interval (ISO format e.g. 2016-01-01T00:00Z/2016-01-02T00:00Z)
    :return response: XML response with the data
    """
    URL = 'https://web-api.tp.entsoe.eu/api?'

    params = {
        'securityToken': api_key,
        'documentType': 'A75',
        'processType': 'A16',
        'in_Domain': in_domain,
        'timeInterval': time_interval
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        return ET.fromstring(response.text)
    else:
        raise Exception('Error: ' + response.reason)
    
def get_wind_solar_forecast(api_key, in_domain, time_interval, psr_type):
    """

    Get Wind and Solar Forecast from Entsoe API

    :param api_key: Your Entsoe API key
    :param in_domain: Input domain
    :param time_interval: Time interval (ISO format e.g. 2016-01-01T00:00Z/2016-01-02T00:00Z)
    :param psr_type: PSR type (B16 for solar, B19 for wind onshore) 
    :return response: XML response with the data
    """
    URL = 'https://web-api.tp.entsoe.eu/api?'

    params = {
        'securityToken': api_key,
        'documentType': 'A69',
        'processType': 'A01',
        'in_Domain': in_domain,
        'timeInterval': time_interval,
         'psrType': psr_type
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        return ET.fromstring(response.text)
    else:
        raise Exception('Error: ' + response.reason)