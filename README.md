# Amogify
A simple Python script to fill your images with amogi. Inspired by Reddit's [r/place](https://www/reddit.com/r/place)

## Usage
Create a new virtual environment:
`python3 -m venv venv`

Source the new environment:
`source venv/bin/activate`

Install the requirements:
`pip install -r requirements.txt`

Run the script, specifying an input image:
`python amogify.py --input image.png`

```
usage: amogify.py [-h] --input INPUT [--output OUTPUT] [--density DENSITY]
                  [--show]

optional arguments:
  -h, --help         show this help message and exit
  --input INPUT      path to the input image to be converted
  --output OUTPUT    path to the output image to be saved
  --density DENSITY  number of amogi to add per pixel
  --show             show a plot comparing the original image and its conversion
```
