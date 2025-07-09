#!/usr/bin/env python3

from __future__ import annotations

import ipaddress

from importlib.metadata import version
from datetime import datetime
from typing import Any
from urllib.parse import urljoin, urlparse

import requests

from urllib3.util import Retry
from requests.adapters import HTTPAdapter


class PhishtankLookup():

    def __init__(self, root_url: str | None=None, useragent: str | None=None,
                 *, proxies: dict[str, str] | None=None) -> None:
        '''Query a specific Phishtank Lookup instance.

        :param root_url: URL of the instance to query.
        :param useragent: User-Agent to use for the requests.
        :param proxies: Proxies to use for the requests.
        '''
        self.root_url = root_url if root_url else 'https://phishtankapi.circl.lu/'

        if not urlparse(self.root_url).scheme:
            self.root_url = 'http://' + self.root_url
        if not self.root_url.endswith('/'):
            self.root_url += '/'
        self.session = requests.session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.headers['user-agent'] = useragent if useragent else f'PyPhishtankLookup / {version("phishtanklookup")}'
        if proxies:
            self.session.proxies.update(proxies)

    @property
    def is_up(self) -> bool:
        '''Test if the given instance is accessible'''
        r = self.session.head(self.root_url)
        return r.status_code == 200

    def redis_up(self) -> dict[str, Any]:
        '''Check if redis is up and running'''
        r = self.session.get(urljoin(self.root_url, 'redis_up'))
        return r.json()

    def info(self) -> dict[str, Any]:
        '''Get information about the instance'''
        r = self.session.get(urljoin(self.root_url, 'info'))
        return r.json()

    def get_urls(self) -> list[str]:
        '''Returns the URLs'''
        r = self.session.get(urljoin(self.root_url, 'urls'))
        return r.json()

    def get_ips(self) -> list[str]:
        '''Returns the IPs'''
        r = self.session.get(urljoin(self.root_url, 'ips'))
        return r.json()

    def get_asns(self) -> list[str]:
        '''Returns the ASNs'''
        r = self.session.get(urljoin(self.root_url, 'asns'))
        return r.json()

    def get_ccs(self) -> list[str]:
        '''Returns the Country Codes'''
        r = self.session.get(urljoin(self.root_url, 'ccs'))
        return r.json()

    def get_urls_by_ip(self, ip: str) -> list[str]:
        '''Returns the URLs by IP

        :param ip: The IP address
        '''
        params = {'ip': ip}
        r = self.session.get(urljoin(self.root_url, 'urls_by_ip'), params=params)
        return r.json()

    def get_urls_by_asn(self, asn: str | int) -> list[str]:
        '''Returns the URLs by ASN

        :param asn: The Autonomus System Number
        '''
        params = {'asn': asn}
        r = self.session.get(urljoin(self.root_url, 'urls_by_asn'), params=params)
        return r.json()

    def get_urls_by_cc(self, cc: str) -> list[str]:
        '''Returns the URLs by Country Code

        :param cc: Country code (ex: LU)
        '''
        params = {'cc': cc}
        r = self.session.get(urljoin(self.root_url, 'urls_by_cc'), params=params)
        return r.json()

    def get_url_entry(self, url: str, pythonify: bool=False) -> dict[str, Any]:
        '''Returns all URL entry

        :param url: URL to search.
        :param pythonify: Convert the response to Python objects/integers/bools
        '''
        params = {'url': url}
        r = self.session.get(urljoin(self.root_url, 'url'), params=params)
        entry = r.json()
        if not entry or not pythonify:
            return entry
        if entry['verified'] == 'yes':
            entry['verified'] = True
        else:
            entry['verified'] = False
        if entry['online'] == 'yes':
            entry['online'] = True
        else:
            entry['online'] = False
        entry['verification_time'] = datetime.fromisoformat(entry['verification_time'])
        entry['submission_time'] = datetime.fromisoformat(entry['submission_time'])
        entry['phish_id'] = int(entry['phish_id'])
        for detail in entry['details']:
            detail['ip_address'] = ipaddress.ip_address(detail['ip_address'])
            detail['cidr_block'] = ipaddress.ip_network(detail['cidr_block'])
            detail['announcing_network'] = int(detail['announcing_network'])
            detail['detail_time'] = datetime.fromisoformat(detail['detail_time'])
        return entry
