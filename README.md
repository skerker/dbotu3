# Distribution-based OTU calling

A new implementation of Sarah Preheim's
[dbOTU](http://aem.asm.org/content/79/21/6593.long) algorithm.
The scope is narrower, the numerical comparisons are faster, and the interface
is more user-friendly.

Read the [documentation](http://dbotu3.readthedocs.io/en/latest/) for:

- a guide to getting started,
- an explanation of the algorithm, and
- the API reference.

You can also read our new [manuscript](http://dx.doi.org/10.1101/076927) for
more technical details about the algorithm.

## Requirements

- **Python 3**
- Numpy, SciPy, [BioPython](http://biopython.org), [Pandas](http://pandas.pydata.org)
- [Levenshtein](https://pypi.python.org/pypi/python-Levenshtein)

## To-do

- Better coverage for unit tests

## Authors

* **Scott Olesen** - *swo at mit.edu*
