# YSpeed

YSpeed is a Python library that scrapes the Speedtest site using Selenium and displays the results with Rich. This library makes it easy to retrieve internet connection speed data (upload, download and latency) in an automated manner and display it elegantly using the Rich library.

## Features

- Speedtest.net site scraping with Selenium
- Retrieve internet connection speed results (upload, download and latency)
- Display results with Rich for better readability

## Installation

Make sure you have Python 3.6 or later installed. To install YSpeed, use the following command:

```python
pip install yspeed
```

or :

Clone the Project

```cmd
git clone https://github.com/Foufou-exe/Yspeed
```

Go to the directory

```cmd
cd Yspeed
```

Install the dependencies

cmd
pip isntall -r requirements.txt
```

Run the Yspeed.py script

```cmd
python yspeed.py
```

## Usage

Here is an example of how to use the YSpeed library:

```python
from yspeed import YSpeed

ys = YSpeed()
result = ys.run_speedtest()
ys.display_results(result)
```

## Dependencies

YSpeed depends on the following libraries:

- selenium
- rich

Make sure you also have a Selenium-compatible driver installed for your preferred browser (Chrome, Firefox, etc.).

## Contribution

Feel free to contribute to this project by opening issues or submitting pull requests. All contributions are welcome.

## License

YSpeed is distributed under the MIT license. See the ``LICENSE`` file for more information.

