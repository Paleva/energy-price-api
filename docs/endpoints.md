
# Endpoints
### **GET /api/v1/price**

**Params:**
- `year` (int): The year for which you want to retrieve the energy price data.
- `month` (int): The month for which you want to retrieve the energy price data.
- `day` (int): The day for which you want to retrieve the energy price data.

**Returns:**
- SVG of the requested day's price graph.

### **GET /api/v1/generation-actual**

**Params:**
- `year` (int): The year for which you want to retrieve the actual wind and solar generation data.
- `month` (int): The month for which you want to retrieve the actual wind and solar generation data.
- `day` (int): The day for which you want to retrieve the actual wind and solar generation data.

**Returns:**
- SVG of the requested day's wind and solar actual generation graph.

### **GET /api/v1/forecast**

**Params:**
- `year` (int): The year for which you want to retrieve the wind and solar forecast data.
- `month` (int): The month for which you want to retrieve the wind and solar forecast data.
- `day` (int): The day for which you want to retrieve the wind and solar forecast data.

**Returns:**
- SVG of the requested day's wind and solar forecast graph.

### **GET /api/v1/forecast-actual-wind**

**Params:**
- `year` (int): The year for which you want to compare the forecasted and actual wind generation data.
- `month` (int): The month for which you want to compare the forecasted and actual wind generation data.
- `day` (int): The day for which you want to compare the forecasted and actual wind generation data.

**Returns:**
- SVG of the requested day's forecasted wind compared to the actual wind generation for that day.

### **GET /api/v1/forecast-actual-solar**

**Params:**
- `year` (int): The year for which you want to compare the forecasted and actual solar generation data.
- `month` (int): The month for which you want to compare the forecasted and actual solar generation data.
- `day` (int): The day for which you want to compare the forecasted and actual solar generation data.

**Returns:**
- SVG of the requested day's forecasted solar compared to the actual solar generation for that day.

### **GET /api/v1/today-price**

**Params:**
- None

**Returns:**
- SVG of today's energy prices graph.

### **GET /api/v1/today-forecast**

**Params:**
- None

**Returns:**
- SVG of today's wind and solar forecast graph.

### **GET /api/v1/today-actual**

**Params:**
- None

**Returns:**
- SVG of today's wind and solar actual generation graph.

### **GET /api/v1/today-forecast-actual-wind**

**Params:**
- None

**Returns:**
- SVG of today's wind forecast generation compared to the actual generation.

### **GET /api/v1/today-forecast-actual-solar**

**Params:**
- None

**Returns:**
- SVG of today's solar forecast generation compared to the actual generation.


### **GET /api/v1/price-json**

**Params:**
- `year` (int): The year for which you want to retrieve the energy price data.
- `month` (int): The month for which you want to retrieve the energy price data.
- `day` (int): The day for which you want to retrieve the energy price data.

**Returns (JSON):**
- `max_price` (float): The maximum price for the requested day.
- `min_price` (float): The minimum price for the requested day.
- `average_price` (float): The average price for the requested day, rounded to 2 decimal places.
- `below_avg_hours` (dict): Contains ranges of hours where the price was below average, with ranges provided in the following format:
  - `one_range`: First continuous range of hours below average.
  - `second_range`: Second continuous range of hours below average (if applicable).
  - `third_range`: Third continuous range of hours below average (if applicable).

**Example Response:**
```json
{
  "max_price": 259.67,
  "min_price": 5.99,
  "average_price": 131.57,
  "below_avg_hours": {
    "one_range": [0, 5],
    "second_range": [8, 11],
    "third_range": [20, 22]
  }
}
```
### **GET /api/v1/forecast-json**

**Params:**
- `year` (int): The year for which you want to retrieve the generation forecast data.
- `month` (int): The month for which you want to retrieve the generation forecast data.
- `day` (int): The day for which you want to retrieve the generation forecast data.

**Returns (JSON):**
- `max_solar` (float): The maximum solar forecast for the requested day.
- `max_wind` (float): The maximum wind forecast for the requested day.
- `min_wind` (float): The minimum wind forecast for the requested day (if there is no wind, this will be 'No wind').
- `average_solar` (float): The average solar forecast for the requested day, rounded to 2 decimal places.
- `average_wind` (float): The average wind forecast for the requested day, rounded to 2 decimal places.
- `above_average_solar_hours` (dict): Contains ranges of hours where the solar generation was above average, with ranges provided in the following format:
  - `range_1`: First continuous range of hours above average.
  - `range_2`: Second continuous range of hours above average (if applicable).
  - `range_3`: Third continuous range of hours above average (if applicable).
- `above_average_wind_hours` (dict): Contains ranges of hours where the wind generation was above average, with ranges provided in the following format:
  - `range_1`: First continuous range of hours above average.
  - `range_2`: Second continuous range of hours above average (if applicable).
  - `range_3`: Third continuous range of hours above average (if applicable).

**Example Response:**
```json
{
  "above_average_solar_hours": {
    "range_1": [
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16
    ]
  },
  "above_average_wind_hours": {
    "range_1": [
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23
    ]
  },
  "average_solar": 41.71,
  "average_wind": 274.33,
  "max_solar": 168.0,
  "max_wind": 485.0,
  "min_wind": 103.0
}
```

### **GET /api/v1/actual-generation-json**

**Params:**
- `year` (int): The year for which you want to retrieve the actual generation data.
- `month` (int): The month for which you want to retrieve the actual generation data.
- `day` (int): The day for which you want to retrieve the actual generation data.

**Returns (JSON):**
- `max_solar` (float): The maximum solar generation for the requested day.
- `max_wind` (float): The maximum wind generation for the requested day.
- `min_wind` (float): The minimum wind generation for the requested day (if there is no wind, this will be 'No wind').
- `average_solar` (float): The average solar generation for the requested day, rounded to 2 decimal places.
- `average_wind` (float): The average wind generation for the requested day, rounded to 2 decimal places.
- `above_average_solar_hours` (dict): Contains ranges of hours where the solar generation was above average, with ranges provided in the following format:
  - `range_1`: First continuous range of hours above average.
  - `range_2`: Second continuous range of hours above average (if applicable).
  - `range_3`: Third continuous range of hours above average (if applicable).
- `above_average_wind_hours` (dict): Contains ranges of hours where the wind generation was above average, with ranges provided in the following format:
  - `range_1`: First continuous range of hours above average.
  - `range_2`: Second continuous range of hours above average (if applicable).
  - `range_3`: Third continuous range of hours above average (if applicable).

**Example Response:**
```json
{
  "above_average_solar_hours": {
    "range_1": [
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16
    ]
  },
  "above_average_wind_hours": {
    "range_1": [
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23
    ]
  },
  "average_solar": 41.71,
  "average_wind": 274.33,
  "max_solar": 168.0,
  "max_wind": 485.0,
  "min_wind": 103.0
}
```

### **GET /api/v1/generation-comparison-json**

**Params:**
- `year` (int): The year for which you want to retrieve the generation comparison data.
- `month` (int): The month for which you want to retrieve the generation comparison data.
- `day` (int): The day for which you want to retrieve the generation comparison data.

**Returns (JSON):**
- `actual` (dict): Contains the actual generation data for the day.
  - `average_solar` (float): The average solar generation for the day, rounded to 2 decimal places.
  - `average_wind` (float): The average wind generation for the day, rounded to 2 decimal places.
- `forecast` (dict): Contains the forecasted generation data for the day.
  - `average_solar` (float): The average solar forecast for the day, rounded to 2 decimal places.
  - `average_wind` (float): The average wind forecast for the day, rounded to 2 decimal places.
- `error_percentage` (dict): Shows the percentage error between the actual and forecasted generation.
  - `solar` (float): The percentage error for solar generation.
  - `wind` (float): The percentage error for wind generation.
- `status` (dict): Indicates whether the actual generation is within the acceptable error range (20%), better than expected, or not as expected.
  - `solar` (string): 
    - `"better than expected"` if the actual generation is significantly higher than the forecast (negative error > 20%).
    - `"as expected"` if the error is within ±20%.
    - `"not as expected"` if the error exceeds ±20%.
  - `wind` (string): 
    - `"better than expected"` if the actual generation is significantly higher than the forecast (negative error > 20%).
    - `"as expected"` if the error is within +-20%.
    - `"not as expected"` if the error exceeds +-20%.

**Example Response:**
```json
{
  "actual": {
    "average_solar": 109.17,
    "average_wind": 594.46
  },
  "error_percentage": {
    "solar": 225.47,
    "wind": -15.86
  },
  "forecast": {
    "average_solar": 33.54,
    "average_wind": 583.58
  },
  "status": {
    "solar": "not as expected",
    "wind": "better than expected"
  }
}
```