#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys

from pyphishtanklookup import PhishtankLookup
from pylookyloo import Lookyloo


def main() -> None:
    parser = argparse.ArgumentParser(description='Get URLs from Phishtank Lookup, capture them with Lookyloo.')
    parser.add_argument('--url', type=str, help='URL of the instance (defaults to https://phishtankapi.circl.lu/).')
    parser.add_argument('--lookyloo', type=str, help='URL of Lookyloo (defaults to https://lookyloo.circl.lu/).')
    group = parser.add_mutually_exclusive_group(required=True)
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

    if args.lookyloo:
        lookyloo = Lookyloo(args.lookyloo)
    else:
        lookyloo = Lookyloo()
    if not lookyloo.is_up:
        print(f'Unable to reach {lookyloo.root_url}. Is the server up?')
        sys.exit(1)

    if args.urls_by_cc:
        response = phishtank_lookup.get_urls_by_cc(args.urls_by_cc)
    elif args.urls_by_ip:
        response = phishtank_lookup.get_urls_by_ip(args.urls_by_ip)
    elif args.urls_by_asn:
        response = phishtank_lookup.get_urls_by_asn(args.urls_by_asn)

    for url in response:
        uuid = lookyloo.submit(url=url, quiet=True)
        print(f'{url}: {lookyloo.root_url}/tree/{uuid}')


if __name__ == '__main__':
    main()
