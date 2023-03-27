![logo](https://socialify.git.ci/Foufou-exe/Yspeed/image?description=1&descriptionEditable=Yspeed%20is%20a%20library%20that%20scrapes%20the%20Speedtest%20site&font=Jost&forks=1&issues=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FFoufou-exe%2FYspeed%2Fdev%2F.github%2Fimages%2Foffice.svg&name=1&owner=1&pulls=1&stargazers=1&theme=Dark)

<div align="center">

[![Build Status](https://app.travis-ci.com/Foufou-exe/Yspeed.svg?branch=main)](https://app.travis-ci.com/Foufou-exe/Yspeed)

</div>

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

```cmd
pip install -r requirements.txt
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

or use script yspeed.py

```bash
python yspeed.py
```

## Dependencies

YSpeed depends on the following libraries:

- selenium
- rich
- holo

Make sure you also have a Selenium-compatible driver installed for your preferred browser (Chrome, Firefox, etc.).

## Use screen



<details>  
  <summary> 🎬 Yspeed </summary>
  <hr>



  
</details>

## Contribution

Feel free to contribute to this project by opening issues or submitting pull requests. All contributions are welcome.

## License

YSpeed is distributed under the MIT license. See the ``LICENSE`` file for more information.
