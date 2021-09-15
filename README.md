# PyPhishtank Lookup

This is the client API for [Phishtank Lookup](https://github.com/Lookyloo/phishtank-lookup),
not the official phishtank API.

## Installation

```bash
pip install pyphishtanklookup
```

## Usage

### Command line

You can use the `phishtank-lookup` command to search in the database:

```bash
usage: phishtank-lookup [-h] [--url URL] (--info | --url_query url | --urls_by_cc cc | --urls_by_ip ip | --urls_by_asn asn)

Search a URL in Phishtank Lookup.

optional arguments:
  -h, --help         show this help message and exit
  --url URL          URL of the instance (defaults to https://phishtankapi.circl.lu/).
  --info             Info avout the instance.
  --url_query url    URL to search.
  --urls_by_cc cc    Country Code to search.
  --urls_by_ip ip    IP address to search.
  --urls_by_asn asn  ASN to search.
```

### Library

See [API Reference](https://pyphishtanklookup.readthedocs.io/en/latest/)
