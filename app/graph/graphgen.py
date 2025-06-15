from .parser import parse_price, parse_generation_forecast, parse_generation_actual
from .request import get_energy_generation, get_energy_price, get_wind_solar_forecast
from flask import abort
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as DT
import dotenv
import numpy as np
import os.path
from math import ceil
from api.paths import FULL_PATH

dotenv.load_dotenv('.env')

def generate_graph(ax, lines, line_labels, line_names, line_colors, max):
    """
    Generate the graph.

    :param ax: Axis
    :param lines: List
    :param line_labels: List
    :param line_names: List
    :param line_colors: List
    :param max: Integer
    """

    for line, label, name, color in zip(lines, line_labels, line_names, line_colors):
        ax.plot(line, linewidth=2, label=label, color=color)
        ax.text((len(line) - 1) * 1.01, line[-1], name, color='black', fontweight='bold')

    if max < 100:
        max = ceil(max / 10) * 10 + 1
        ax.set_yticks(np.arange(0, max, 20))
        ax.set_xticks(ticks=range(0, 24, 2))
    else:
        max = ceil(max / 100) * 100 + 1
        ax.set_yticks(np.arange(0, max, 50))   
        ax.set_xticks(ticks=range(0, 24, 2))

    draw_grid_lines(ax, max)

def get_energy_data(time_interval, type, psr=None):
    """
    Get the data from the API.

    :param time_interval: String
    :param type: String
    (price, forecast, actual)
    :param psr: String
    (Forecast PSR type: B16 for solar, B19 for wind)
    :return xml: String
    """

    if type == 'price':
        return get_energy_price(os.getenv("API_KEY"), '10YLT-1001A0008Q', '10YLT-1001A0008Q', time_interval)
    elif type == 'forecast' and psr is not None:
        return get_wind_solar_forecast(os.getenv("API_KEY"), '10YLT-1001A0008Q', time_interval, psr)
    elif type == 'actual':
        return get_energy_generation(os.getenv("API_KEY"), '10YLT-1001A0008Q', time_interval)
    else:
        abort(400, 'Invalid type')

def draw_grid_lines(ax, max_gen):
    """
    Draw grid lines on the graph.

    :param ax: Axis 
    :param max_gen: Integer
    """

    if max_gen < 100:
        index=divmod(max_gen, 10)
        index = round(index[0]/2)
        for line in range(1, index+1):
            ax.plot([(line)*20]*24, color='lightgray', linestyle='dotted')
    else:
        index=divmod(max_gen, 100)
        index = round(index[0])
        for line in range(1, index+1):
            ax.plot([(line)*100]*24, color='lightgray', linestyle='dotted')


def save_graph(fig, filename):
    """
    Save the graph as an SVG file.

    :param fig: Figure
    :param filename: String
    """

    plt.savefig(f'{FULL_PATH}{filename}', format='svg', transparent=True)
    plt.close(fig)

def make_date_string(year, month, day):
    """"
    
    Returns a string with the start and end date in the format for the request
    On error returns raise an exception

    :param start_date: String
    :param end_date: String
    :return date_string: String

    """

    if(year > DT.datetime.now().year):
        abort(400, 'Invalid year')

    try: 
        if(day == 1):
            start_date = DT.datetime.combine(DT.date(year, month, 1), DT.time(22, 0)) - DT.timedelta(days=1)
            start_date = start_date.strftime('%Y-%m-%dT%H:%MZ')
            end_date = DT.datetime.combine(DT.date(year, month, 1), DT.time(22, 0)).strftime('%Y-%m-%dT%H:%MZ')
        else:
            start_date = DT.datetime.combine(DT.date(year, month, day-1), DT.time(22, 0)).strftime('%Y-%m-%dT%H:%MZ')
            end_date = DT.datetime.combine(DT.date(year, month, day), DT.time(22, 0)).strftime('%Y-%m-%dT%H:%MZ')
    except TypeError:
        print(day)
        abort(400, 'Invalid date')

    time_interval = f'{start_date}/{end_date}'
    print(time_interval)

    return time_interval

def remove_border(ax):
    """"
    
    Remove the border of the graph

    :param ax: Graph
    :return: None

    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

def calc_average(prices):
    """
    
    Calculate the average of a list of prices

    :param prices: List of prices
    :return average: Float

    """
    return sum(prices) / len(prices)

def graphgen_gen_actual(year, month, day):
    """"

    Generates the graph and saves it in a .svg file
    Returns the name of the .svg file

    :param year: Integer 
    :param month: Integer
    :param day: Integer
    :return filename: String

    """
    
    time_interval = make_date_string(year, month, day)
    filename = f'gen_actual{time_interval[0:10:1]}.svg'
    
    xml = get_energy_data(time_interval, 'actual')
    solar = parse_generation_actual(xml, 'B16')
    wind = parse_generation_actual(xml, 'B19')
    max_gen = round(max(max(wind), max(solar)))

    fig, ax = plt.subplots()

    generate_graph(ax, [solar, wind], ['Solar Generation', 'Wind Generation'], ['Solar', 'Wind'], ['yellow', 'blue'], max_gen)
    remove_border(ax)

    ax.set_xlabel('Hour of the day')
    ax.set_ylabel('Power generated (MW)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(loc='upper center',
            frameon=False, 
            bbox_to_anchor=(0.53, -0.11), 
            fancybox=True, ncol=2)

    save_graph(fig, filename)
    return filename


def graphgen_price(year, month, day):
    """"

    Generatees the graph and saves it in a .svg file
    Returns the name of the .svg file

    :param year: Integer 
    :param month: Integer
    :param day: Integer
    :return filename: String

    """

    time_interval = make_date_string(year, month, day)
    filename = f'gen_price{time_interval[0:10:1]}.svg'
    
    if(os.path.isfile(f'{FULL_PATH}{filename}')):
        print(f'{filename} already exists')
        return filename
    
    xml = get_energy_data(time_interval, 'price')
    prices = parse_price(xml)
    max_price = round(max(prices))
    
    fig, ax = plt.subplots()
    
    avg = calc_average(prices)

    generate_graph(ax, [prices, [round(avg, 2)] * 24], ['Price', 'Average'], ['Price', 'Average'], ['black', 'darkgray'], max_price)


    np_prices = np.array(prices)
    ax.fill_between(range(0, len(np_prices)), 
                    np_prices, 
                    0, 
                    where=(np_prices < avg), 
                    interpolate=True, color='lightgray', alpha=0.5, 
                    label='Below Average Price'
                    )

    ax.set_yticks(np.arange(50, max_price*1.25, 50))
    ax.set_xticks(ticks=range(0, 24, 2))

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    remove_border(ax)
    
    ax.set_xlabel('Hour of the day')
    ax.set_ylabel('Price per MW')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend( 
            loc='upper center', 
            frameon=False, 
            bbox_to_anchor=(0.53, -0.11), 
            fancybox=True, ncol=3)
    
    save_graph(fig, filename)
    return filename
    

def graphgen_gen_forecast(year, month, day):
    """"

    Generates the graph and saves it in a .svg file
    Returns the name of the .svg file

    :param year: Integer 
    :param month: Integer
    :param day: Integer
    :return filename: String

    """

    time_interval = make_date_string(year, month, day)
    filename = f'gen_forecast{time_interval[0:10:1]}.svg'
    
    if(os.path.isfile(f'{FULL_PATH}{filename}')):
        print(f'{filename} already exists')
        return filename
    
    xml = get_energy_data(time_interval, 'forecast', 'B19')
    wind = parse_generation_forecast(xml)
    xml = get_energy_data(time_interval, 'forecast', 'B16')
    solar = parse_generation_forecast(xml)

    max_gen = round(max(max(wind), max(solar)))
        
    fig, ax = plt.subplots()
    
    generate_graph(ax, [solar, wind], ['Solar Forecast', 'Wind Forecast'], ['Solar', 'Wind'], ['yellow', 'blue'], max_gen)
        
    remove_border(ax)

    ax.set_xlabel('Hour of the day')
    ax.set_ylabel('Power generated (MW)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend( 
            loc='upper center', 
            frameon=False, 
            bbox_to_anchor=(0.53, -0.11), 
            fancybox=True, ncol=2)
    
    save_graph(fig, filename)
    return filename



def graphgen_actual_forecast_wind(year, month, day):
    """"

    Generates the graph and saves it in a .svg file
    Returns the name of the .svg file

    :param year: Integer 
    :param month: Integer
    :param day: Integer
    :return filename: String

    """

    time_interval = make_date_string(year, month, day)
    filename = f'gen_actual_forecast_wind{time_interval[0:10:1]}.svg'
    
    xml = get_energy_data(time_interval, 'forecast', 'B19')
    wind = parse_generation_forecast(xml)
    xml = get_energy_data(time_interval, 'actual')
    wind_gen = parse_generation_actual(xml, 'B19')
    max_gen = round(max(max(wind), max(wind_gen)))

    fig, ax = plt.subplots()

    generate_graph(ax, [wind, wind_gen], ['Wind Forecast', 'Wind Generation'], ['Forecast', 'Generation'], ['lightblue', 'blue'], max_gen)

    wind_forecast = wind[0:len(wind_gen)]
    ax.fill_between(range(0, len(wind_gen)), 
                    wind_gen, 
                    wind_forecast, 
                    where=(np.array(wind_forecast) < np.array(wind_gen)), 
                    interpolate=False, color='lightblue', alpha=0.5, 
                    label='Gen higher than forecast'
                    )

    

    remove_border(ax)
    
    ax.set_xlabel('Hour of the day')
    ax.set_ylabel('Power generated (MW)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(
            loc='upper center',
            frameon=False,
            bbox_to_anchor=(0.53, -0.11), 
            fancybox=True,
            ncol=3)

    save_graph(fig, filename)
    return filename



def graphgen_actual_forecast_solar(year, month, day):
    """"

    Generates the graph and saves it in a .svg file
    Returns the name of the .svg file

    :param year: Integer 
    :param month: Integer
    :param day: Integer
    :return filename: String

    """
    time_interval = make_date_string(year, month, day)
    filename = f'gen_actual_forecast_solar{time_interval[0:10:1]}.svg'

    xml = get_energy_data(time_interval, 'forecast', 'B16')
    solar = parse_generation_forecast(xml)
    xml = get_energy_data(time_interval, 'actual')
    solar_gen = parse_generation_actual(xml, 'B16')
    max_gen = round(max(max(solar), max(solar_gen)))
    
    fig, ax = plt.subplots()

    generate_graph(ax, [solar, solar_gen], ['Solar Forecast', 'Solar Generation'], ['Forecast', 'Generation'], ['lightcoral', 'red'], max_gen)
    
    solar_forecast = solar[0:len(solar_gen)]
    ax.fill_between(range(0, len(solar_gen)),
                    solar_gen,
                    solar_forecast, 
                    where=(np.array(solar_forecast) < np.array(solar_gen)), 
                    interpolate=False, color='lightyellow', alpha=0.8, 
                    label='Gen higher than forecast'
                    )

    

    remove_border(ax)
    
    ax.set_xlabel('Hour of the day')
    ax.set_ylabel('Power generated (MW)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(
            loc='upper center',
            frameon=False,
            bbox_to_anchor=(0.53, -0.11), 
            fancybox=True,
            ncol=3)

    save_graph(fig, filename)    
    return filename
