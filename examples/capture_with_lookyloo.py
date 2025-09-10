#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime
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

    # get the remote lacuses to pass the right proxies to the captures
    cc_mapping = {}
    remote_lacuses = lookyloo.get_remote_lacuses()
    # could be a dict (one remote lacus), or a list (multiple remote lacuses)
    if isinstance(remote_lacuses, dict):
        remote_lacuses = [remote_lacuses]
    for remote_lacus in remote_lacuses:
        if not remote_lacus['is_up']:
            # The remote lacus is down, ignoring
            continue
        if 'proxies' in remote_lacus:
            for name, infos in remote_lacus['proxies'].items():
                if 'meta' in infos and 'country_code' in infos['meta']:
                    cc_mapping[infos['meta']['country_code']] = name
                    pass

    if args.urls_by_cc:
        response = phishtank_lookup.get_urls_by_cc(args.urls_by_cc)
    elif args.urls_by_ip:
        response = phishtank_lookup.get_urls_by_ip(args.urls_by_ip)
    elif args.urls_by_asn:
        response = phishtank_lookup.get_urls_by_asn(args.urls_by_asn)

    uuids_file = f'{args.urls_by_cc}_uuids.txt'
    with open(uuids_file, 'w') as f:
        for url in response:
            if args.urls_by_cc:
                print(f'{datetime.now()} Capturing {url} with proxy {cc_mapping.get(args.urls_by_cc)}...')
                uuid = lookyloo.submit(url=url, proxy=cc_mapping.get(args.urls_by_cc), quiet=True)
            else:
                print(f'{datetime.now()} Capturing {url}...')
                uuid = lookyloo.submit(url=url, quiet=True)
            print(f'{datetime.now()} {url}: {lookyloo.root_url}/tree/{uuid}')
            f.write(f'{uuid}\n')


if __name__ == '__main__':
    main()
