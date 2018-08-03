# Number Radix

This is a Python script and library to encode, decode and format numbers
including fractions and exponential notation in radixes/bases other than
decimal, such as octal, dozenal/duodecimal, hexadecimal, base57 and base62. The
radix can also be determined by any number of digits specified: 0123456789ab...

## Requirements
* Python 3

## Installation
From the Python Package Index:
```
pip install num-radix
```

Or download and run:
```
python3 setup.py install
```

## Command-Line
Use the ```--help``` argument for help.
```
num-radix --help
```

By default, the script encodes and decodes in dozenal.

This outputs '6X,534;3000' encoded in dozenal.
```
num-radix --encode 142456.25 --format ',.4f'
```
The format string causes the output to have a scale of 4 and every 3 integer
digits to be separated by a comma.
The format is given in [Python format string syntax](https://docs.python.org/3/library/string.html#format-specification-mini-language).

Format with e-notation. This outputs '4;133X82e-0E'.
```
num-radix --encode 0.000000000005526745 --format '.6e'
```

Encode in hexadecimal.
```
num-radix --encode 142 --base hex
```

Decode back to a decimal from dozenal.
```
num-radix --decode '6X534;3'
```

The input and output can be piped. Each line of input is encoded
(or decoded) and output on a new line.
```
echo -e "142\n4353" | num-radix --encode - | cat
```

## Python
Import the library.
```
from num_radix import Radix
```

Create a radix.
```
dozenal = Radix.dozenal()
hexa = Radix.hex()
base20 = Radix("0123456789ABCDEFGHIJ", sep="|")
```

Encode with the radix object.
```
dozenal.encode(3546)
dozenal.encode(142456.25, "013.4f")
numbers = [142456.25, 34, 0.000345]
"These numbers {:013.4f}, {}, {:e} are in dozenal".format(*dozenal.wrap(numbers))
```

Encoding date & time.
```
from datetime import datetime
now = datetime.now()
dozenal_now = dozenal.wrap(now.timetuple()[:6])
"{}-{:02}-{:02} {:02}:{:02}:{:02}".format(*dozenal_now)
```

Decode with the radix object.
```
dozenal.decode("6X534;3")
```
There are more examples in the demo section at the end of the ```__init__.py``` file.
