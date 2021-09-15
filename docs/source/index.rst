.. PyLookyloo documentation master file, created by
   sphinx-quickstart on Tue Mar 23 12:28:17 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyPhishtankLookup's documentation!
======================================

This is the client API for `Phishtank Lookup <https://github.com/Lookyloo/phishtank-lookup>`_:

  Phishtank Lookup is a tool that use the hourly dump of Phishtank and allows to run queries locally.


Installation
------------

The package is available on PyPi, so you can install it with::

  pip install pyphishtanklookup


Usage
-----

You can use `pyphishtanklookup` as a python script::

	$ phishtank-lookup -h
	usage: phishtank-lookup [-h] [--url URL]
							(--info | --url_query url | --urls_by_cc cc | --urls_by_ip ip | --urls_by_asn asn)

	Search a URL in Phishtank Lookup.

	optional arguments:
	  -h, --help         show this help message and exit
	  --url URL          URL of the instance (defaults to https://phishtankapi.circl.lu/).
	  --info             Info avout the instance.
	  --url_query url    URL to search.
	  --urls_by_cc cc    Country Code to search.
	  --urls_by_ip ip    IP address to search.
	  --urls_by_asn asn  ASN to search.


Or as a library:

.. toctree::
   :glob:

   api_reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
