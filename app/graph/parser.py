import re

# B16 - solar
# B19 - wind onshore

def parse_data(data, xml_namespace):
    result = []
    
    for value in data:
        if(value.tag == xml_namespace.group(0) + 'Point'):
           result.append(float(value[1].text))

    if len(result) > 24:
        new_list_data = []
        i = 0
        sum = 0
        for value in result:
            sum += value
            i += 1
            if i == 4:
                new_list_data.append(sum / 4)
                sum = 0
                i = 0

        result = new_list_data
    return result

def parse_generation_forecast(xml):
    """
    
    Parse Forecast generation from the XML by g (psr_type)

    :param xml: XML response from ENTSOE
    :return array: Array of generation forecast for the day every hour

    """
    xml_namespace = re.match(r'{.*}', xml.tag)
    namespace = {'ns': xml_namespace.group(0).removeprefix('{').removesuffix('}')}
    generation_period = xml.find('ns:TimeSeries', namespace).find('ns:Period', namespace)

    generation_data = parse_data(generation_period, xml_namespace)

    return generation_data

def parse_price(xml):

    """
    
    Parse Price from the XML

    :param xml: XML response from ENTSOE
    :return array: Array of prices for the day every hour

    """
    xml_namespace = re.match(r'{.*}', xml.tag)
    namespace = {'ns': xml_namespace.group(0).removeprefix('{').removesuffix('}')}
    price_data_period = xml.find('ns:TimeSeries', namespace).find('ns:Period', namespace)

    prices = parse_data(price_data_period, xml_namespace)
   
    return prices

def parse_generation_actual(xml, type):
    """
    
    Parse Actual generation from the XML by g (psr_type)

    :param xml: XML response from ENTSOE
    :param type: PSR type (B16 for solar, B19 for wind onshore etc.)
    :return array: Array of the actual generation for the day every hour
    """

    xml_namespace = re.match(r'{.*}', xml.tag)
    namespace = {'ns': xml_namespace.group(0).removeprefix('{').removesuffix('}')}

    generation_type_periods = xml.findall('ns:TimeSeries', namespace)
    gen_data = []
    for period in generation_type_periods:
    
        gen_type = period.find('ns:MktPSRType', namespace)
        if gen_type[0].text == type:
            generation_period = period.find('ns:Period', namespace)
            points = generation_period.findall('ns:Point', namespace)
            for point in points:
                gen_data.append(float(point[1].text))
            
    if len(gen_data) > 24:
        new_list_data = []
        i = 0
        sum = 0
        for value in gen_data:
            sum += value
            i += 1
            if i == 4:
                new_list_data.append(sum / 4)
                sum = 0
                i = 0

        gen_data = new_list_data

    return gen_data