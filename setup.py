#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="num-radix",
	version="1.0.1",
	
	author="2sh",
	author_email="contact@2sh.me",
	
	description="Number radix/base encoding, decoding and formatting",
	long_description=long_description,
	long_description_content_type="text/markdown",
	
	url="https://github.com/2sh/num-radix",
	
	packages=["num_radix"],
	
	python_requires='>=3',
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent",
		"Topic :: Scientific/Engineering :: Mathematics"
	),
	
	entry_points={"console_scripts":["num-radix=num_radix:_main"]}
)
