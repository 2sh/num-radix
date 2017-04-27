#!/usr/bin/env python3
#
#	radix.py, radix encoding, decoding and formatting
#	Copyright (C) 2017 2sh <contact@2sh.me>
#	
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import string
import math

class Radix:
	'''The Radix.
	
	Args:
		digits: The digits to be used for the radix.
			e.g. 0123456789ab... The number of digits will be the base.
		sep: The seperator character between integer and fraction.
		neg: The negative character.
		pos: The positive character.
		tsep: The thousand seperator character.
		exp: The exponent notation character.
	'''
	def __init__(self, digits, sep='.', neg='-',
			tsep=',', pos='+', exp='e'):
		self.digits = digits
		self.sep = sep
		self.neg = neg
		self.tsep = tsep
		self.pos = pos
		self.exp = exp
	
	def __repr__(self):
		return ("Radix({self.digits!r}, sep={self.sep!r}, neg={self.neg!r}, "
			"tsep={self.tsep!r}, pos={self.pos!r}, exp={self.exp!r})"
			).format(self=self)
	
	@classmethod
	def by_base(cls, base, **kwargs):
		'''Create radix by base number.
		
		Args:
			base: The digits to be used for the radix.
			**kwargs: See Radix class keyword arguments.
		'''
		return cls((string.digits + string.ascii_uppercase +
			string.ascii_lowercase + "")[:abs(base)], **kwargs)
	
	@classmethod
	def bin(cls, **kwargs):
		'''Create binary radix.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		return cls("01", **kwargs)
	
	@classmethod
	def oct(cls, **kwargs):
		'''Create octal radix.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		return cls(string.digits[:8], **kwargs)
	
	@classmethod
	def hex(cls, **kwargs):
		'''Create uppercase hexadecimal radix.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		return cls(string.digits + "ABCDEF", **kwargs)
		
	@classmethod
	def hex_lc(cls, **kwargs):
		'''Create lowercase hexadecimal radix.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		return cls(string.digits + "abcdef", **kwargs)
	
	@classmethod
	def dozenal(cls, **kwargs):
		'''Create Andrews notation dozenal radix.
		Notation advocated by Frank Emerson Andrews.
		Digits X and E for 10 and 11.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		kwargs.setdefault("sep", ";")
		return cls(string.digits + "XE", **kwargs)
	
	@classmethod
	def dozenal_pitman(cls, **kwargs):
		'''Create Pitman notation dozenal radix.
		Notation advocated by Isaac Pitman.
		Digits ↊ and ↋ for 10 and 11.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		kwargs.setdefault("sep", ";")
		return cls(string.digits + "↊↋", **kwargs)
	
	@classmethod
	def dozenal_pitman_ascii(cls, **kwargs):
		'''Create ASCII Pitman notation dozenal radix.
		Digits T and E for 10 and 11.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		kwargs.setdefault("sep", ";")
		return cls(string.digits + "TE", **kwargs)
	
	@classmethod
	def dozenal_dwiggins(cls, **kwargs):
		'''Create Dwiggins notation dozenal radix.
		Notation advocated by William Addison Dwiggins.
		Digits 𝒳 and ℰ for 10 and 11.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		kwargs.setdefault("sep", ";")
		return cls(string.digits + "𝒳ℰ", **kwargs)
	
	@classmethod
	def dozenal_kramer(cls, **kwargs):
		'''Create Kramer notation dozenal radix.
		Notation advocated by Edna Kramer.
		Digits * and # for 10 and 11.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		kwargs.setdefault("sep", ";")
		return cls(string.digits + "*#", **kwargs)
	
	@classmethod
	def base62(cls, **kwargs):
		'''Create Base62 notation dozenal radix.
		Digits 0-9A-Za-z.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		return cls(
			string.digits + string.ascii_uppercase + string.ascii_lowercase,
			**kwargs)

	@classmethod
	def base57(cls, **kwargs):
		'''Create Base57 notation dozenal radix.
		Digits 0-9A-Za-z, excluding Il1O0 to prevent digit mix-up.
		
		Args:
			**kwargs: See Radix class keyword arguments.
		'''
		digits = (string.ascii_uppercase + string.ascii_lowercase +
			string.digits)
		digits = digits.replace("I", "")
		digits = digits.replace("l", "")
		digits = digits.replace("1", "")
		digits = digits.replace("O", "")
		digits = digits.replace("0", "")
		return cls(digits, **kwargs)
	
	@property
	def digits(self):
		return self._digits
	
	@digits.setter
	def digits(self, digits):
		self._digits = digits
		self._base = len(digits)
	
	@property
	def base(self):
		return self._base
	
	def encode(self, number, fmt=None):
		'''Encode a number.
		
		Args:
			number: The number encode.
			fmt: The encode format.
				This value is either an integer, specifying the scale, or
				a string in the Python format string syntax.
		'''
		if type(fmt) is str:
			if fmt.endswith("e") or fmt.endswith("E"):
				exponent = math.floor(
					math.log(abs(number))/math.log(self.base))
				number *= self.base ** (exponent*-1)
		else:
			exponent = None
		
		integer, fraction = divmod(abs(number), 1)
		integer = int(integer)
		
		has_fraction = type(fraction) is float
		
		indexes = []
		
		if integer:
			while integer:
				integer, index = divmod(integer, self.base)
				indexes.insert(0, index)
		else:
			indexes.append(0)
		
		template_fmt = fmt
		if has_fraction:
			if not template_fmt:
				scale = 17-len(indexes)
				template_fmt = "." + str(scale) + "f"
			else:
				if type(template_fmt) is int:
					scale = template_fmt
					template_fmt = "." + str(scale) + "f"
				else:
					scale = self._get_scale_from_format(
						template_fmt)
				
			template = float(
				(len(indexes) * "1") + "." + (scale * "1"))
		else:
			if not template_fmt:
				template_fmt = "d"
			template = int(len(indexes) * "1")
		if number < 0:
			template *= -1
		template = format(template, template_fmt)
		
		if exponent is not None:
			template, _ = template.split(fmt[-1])
		
		if has_fraction:
			if type(fmt) is str:
				scale = len(template.split(".")[1])
			
			for i in range(scale):
				index, fraction = divmod(fraction*self.base, 1)
				indexes.append(int(index))
			
			if fraction > 0.5:
				for i in range(len(indexes)-1, -1, -1):
					if type(indexes[i]) is not int:
						continue
					if indexes[i] + 1 == self.base:
						indexes[i] = 0
						continue
					indexes[i] += 1
					break
				else:
					indexes.insert(0, 1)
		
		digits = [self.digits[index] for index in indexes]
		
		output = self._fill_template(template, digits)
		
		if has_fraction and not fmt:
			output = output.rstrip(self.digits[0])
			if output.endswith(self.sep):
				output += self.digits[0]
		
		if exponent is not None:
			output += self.exp + self.encode(exponent, "+03d")
		
		return output
	
	@staticmethod
	def _get_scale_from_format(fmt):
		scale = ""
		try:
			for char in fmt[fmt.index(".")+1:]:
				if char not in string.digits:
					break
				scale += char
			return int(scale)
		except:
			return None
	
	def _fill_template(self, template, digits):
		is_left_fill = True
		output = ""
		for char in template:
			if is_left_fill and char in string.digits[1:]:
				is_left_fill = False
			if char in string.digits:
				if digits and not is_left_fill:
					output += digits.pop(0)
				else:
					output += self.digits[0]
			elif char == "-":
				output += self.neg
			elif char == ".":
				output += self.sep
			elif char == ",":
				output += self.tsep
			elif char == "+":
				output += self.pos
			else:
				output += char
		return output
	
	def decode(self, number):
		'''Decode a number.
		
		Args:
			number: The number decode.
		'''
		number = number.strip()
		is_negative = number.startswith(self.neg)
		if is_negative or number.startswith(self.pos):
			number = number[1:]
		
		try:
			exponent = number.index(self.sep)-1
		except:
			exponent = len(number)-1
		else:
			number = number[:exponent+1] + number[exponent+2:]
		
		output = 0
		for digit in number:
			try:
				output += self.digits.index(digit) * (self.base ** exponent)
			except ValueError:
				raise ValueError("Invalid digit '{}'".format(digit))
			exponent -= 1
		
		if is_negative:
			output *= -1
		return output
	
	def wrap(self, *obj):
		'''Wrap in a RadixFormatWrapper.
		This method wraps a number or the numbers contained within an iterable
		in a RadixFormatWrapper.
		
		Args:
			*obj: Either a number or an iterable containing numbers.
			fmt: The encode format.
				This value is given in the Python format string syntax.
		'''
		if len(obj) == 1:
			obj = obj[0]
		if type(obj) is int or type(obj) is float or type(obj) is str:
			return RadixFormatWrapper(obj, self)
		else:
			return type(obj)(self.wrap(x) for x in obj)

class RadixFormatWrapper:
	'''Wrapper for easily formatting numbers by radix.
	
	Args:
		number: The number to wrap.
		radix: The radix.
	'''
	def __init__(self, number, radix):
		if type(number) is str:
			number = radix.decode(number)
		self.number = number
		self.radix = radix
	
	def __format__(self, fmt):
		return self.radix.encode(self.number, fmt)

	def __str__(self):
		return self.radix.encode(self.number)
		
	def __repr__(self):
		return ("RadixFormatWrapper({self.number!r}, {self.radix!r})"
			).format(self=self)

if __name__ == "__main__":
	from datetime import datetime
	from time import sleep
	import argparse
	import os
	import sys
	import fileinput
	
	parser = argparse.ArgumentParser(description="Radix Converter")
	
	parser.add_argument("-b", "--base",
		dest="base", metavar="BASE", type=str, default="dozenal",
		help="set the base. This can eiter be a number or one of the "
			"following: bin, oct, hex, hex_lc, dozenal (andrews), "
			"dozenal_pitman, dozenal_pitman_ascii, dozenal_dwiggins, "
			"dozenal_kramer, base62, base57 [Default: %(default)s]")
	
	parser.add_argument("-g", "--digits",
		dest="digits", metavar="DIGITS", type=str,
		help="set the digits to be used for the radix e.g. 0123456789ab... "
			"The number of digits will be the base")
		
	parser.add_argument("-e", "--encode",
		dest="encode", metavar="NUMBER", type=str,
		help="encode the specified number or specify '-' to encode a list of"
			"numbers separated by a newline")

	parser.add_argument("-f", "--format",
		dest="format", metavar="FORMAT", type=str,
		help="set the encode output format. This value is either an integer, "
			"specifying the scale, or a string "
			"in the Python format string syntax")
	
	parser.add_argument("-d", "--decode",
		dest="decode", metavar="NUMBER", type=str,
		help="decode the specified number or specify '-' to decode a list of"
			"numbers separated by a newline")
	
	parser.add_argument("--demo",
		dest="demo", action='store_true',
		help="run the radix demo")
	
	group = parser.add_argument_group('Symbols')
	group.add_argument("--sep",
		dest="sep", metavar="CHAR", type=str,
		help="set the seperator char between integer and fraction")
	group.add_argument("--neg",
		dest="neg", metavar="CHAR", type=str,
		help="set the negative character")
	group.add_argument("--pos",
		dest="pos", metavar="CHAR", type=str,
		help="set the positive character")
	group.add_argument("--tsep",
		dest="tsep", metavar="CHAR", type=str,
		help="set the thousand seperator character")
	group.add_argument("--exp",
		dest="exp", metavar="CHAR", type=str,
		help="set the exponent notation character")
	
	args = parser.parse_args()
	
	radix_params = {}
	if args.sep:
		radix_params["sep"] = args.sep
	if args.neg:
		radix_params["neg"] = args.neg
	if args.pos:
		radix_params["pos"] = args.pos
	if args.tsep:
		radix_params["tsep"] = args.tsep
	if args.exp:
		radix_params["exp"] = args.exp
	
	if args.digits:
		radix = Radix(args.digits, **radix_params)
	else:
		try:
			radix = Radix.by_base(int(args.base), **radix_params)
		except:
			radix = getattr(Radix, args.base)(**radix_params)
	
	if args.encode:
		number = args.encode
	elif args.decode:
		number = args.decode
	else:
		number = None
	
	if number:
		
		try:
			fmt = int(args.format)
		except:
			fmt = args.format
		
		if number == "-":
			numbers = sys.stdin
		else:
			numbers = [number]
		for number in numbers:
			number = number.strip()
			if not number:
				continue
			if args.encode:
				try:
					number = int(number)
				except ValueError:
					number = float(number)
				print(radix.encode(number, fmt))
			else:
				print(radix.decode(number))
	
	elif args.demo:
		show_colors = (sys.platform != 'win32' or 'ANSICON' in os.environ and
			hasattr(sys.stdout, 'isatty') and sys.stdout.isatty())
		
		# Radix Demonstration
		
		# Creating a radix with the dozenal classmethod:
#		radix = Radix.dozenal()
		
		print("Multiplication Table")
		for a in range(1, radix.base+1):
			for b in range(1, radix.base+1):
				n = a*b
				fmt_string = "{:>2d}"
				if show_colors:
					if n%radix.base == 0:
						fmt_string = "\033[1;31m{:>2d}\033[0;0m"
					elif n%(radix.base/2) == 0 or n%(radix.base/4) == 0:
						fmt_string = "\033[0;32m{:>2d}\033[0;0m"
					elif n%2 != 0:
						fmt_string = "\033[1;36m{:>2d}\033[0;0m"
				print(fmt_string.format(radix.wrap(n)), end=" ")
			print()
		print()
		
		print("Mathematical Constants")
		print("π  =", radix.encode(math.pi, 14))
		print("τ  =", radix.encode(2*math.pi, 13))
		print("e  =", radix.encode(math.e, 12))
		print("√2 =", radix.encode(math.sqrt(2), 11))
		print("ϕ  =", radix.encode((1+math.sqrt(5))/2, 10))
		print()
		
		print("Physical Constants")
		print("c  = {:,d} m/s".format(radix.wrap(299792458)))
		print("c  = {:.2e} m/s".format(radix.wrap(299792458)))
		print("G  = {:.8e} Nm²/kg²".format(radix.wrap(6.6740831*10**-11)))
		print("h  = {:.8e} Js".format(radix.wrap(6.62607004081*10**-34)))
		print("e  = {:.8e} C".format(radix.wrap(1.6021766208*10**-19)))
		print()
		
		print("Fractions")
		for i in range(2, radix.base+1):
			print("1/{:>2d} = {}".format(i, radix.wrap(1/i)))
		print()
		
		print("Date & Time")
		while 1:
			local = datetime.now()
			radix_local = radix.wrap(local.timetuple()[:6])
			utc = datetime.utcnow()
			radix_utc = radix.wrap(utc.timetuple()[:6])
			print(("  Local: {}-{:02}-{:02} {:02}:{:02}:{:02}  "
				"UTC: {}-{:02}-{:02} {:02}:{:02}:{:02}  "
				).format(*(radix_local+radix_utc)), end='\r', flush=True)
			sleep(1-(local.microsecond/1000000))
	else:
		parser.print_help()
