import argparse
import json
import sys

from .api import PhishtankLookup


def main():
    parser = argparse.ArgumentParser(description='Search a URL in Phishtank Lookup.')
    parser.add_argument('--url', type=str, help='URL of the instance (defaults to https://phishtankapi.circl.lu/).')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--info', action='store_true', help='Info avout the instance.')
    group.add_argument('--url_query', metavar='url', help='URL to search.')
    group.add_argument('--urls_by_cc', metavar='cc', help='Country Code to search.')
    group.add_argument('--urls_by_ip', metavar='ip', help='IP address to search.')
    group.add_argument('--urls_by_asn', metavar='asn', help='ASN to search.')
    args = parser.parse_args()

    if args.url:
        phishtank_lookup = PhishtankLookup(args.url)
    else:
        phishtank_lookup = PhishtankLookup()

    if not phishtank_lookup.is_up:
        print(f'Unable to reach {phishtank_lookup.root_url}. Is the server up?')
        sys.exit(1)
    if args.info:
        response = phishtank_lookup.info()
    elif args.url_query:
        response = phishtank_lookup.get_url_entry(args.url_query)
    elif args.urls_by_cc:
        response = phishtank_lookup.get_urls_by_cc(args.urls_by_cc)
    elif args.urls_by_ip:
        response = phishtank_lookup.get_urls_by_ip(args.urls_by_ip)
    elif args.urls_by_asn:
        response = phishtank_lookup.get_urls_by_asn(args.urls_by_asn)
    print(json.dumps(response, indent=2))
