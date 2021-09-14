import argparse
import json

from .api import PhishtankLookup


def main():
    parser = argparse.ArgumentParser(description='Search a URL in Phishtank Lookup.')
    parser.add_argument('--url', type=str, help='URL of the instance (defaults to https://0.0.0.0:5300, the local instance).')
    parser.add_argument('--url_query', required=True, help='URL to search.')
    args = parser.parse_args()

    if args.url:
        phishtank_lookup = PhishtankLookup(args.url)
    else:
        phishtank_lookup = PhishtankLookup()

    if phishtank_lookup.is_up:
        url = phishtank_lookup.get_url_entry(args.url_query)
        print(json.dumps(url, indent=2))
    else:
        print(f'Unable to reach {phishtank_lookup.root_url}. Is the server up?')
