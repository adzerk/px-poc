#!/usr/bin/env python3

import datetime, json, os, requests, sys


def getenv(var):
    val = os.getenv(var)
    if val is None:
        raise RuntimeError(f'environment variable not set: {var}')
    return val


def json_from_file(file):
    with open(file) as f:
        return json.load(f)


def delete_contentdb(network, schema_name, content_key):
    url = f'https://e-{network}.adzerk.net/cdb/{network}/custom/{schema_name}/{content_key}'
    resp = requests.delete(url, headers=HEADERS)
    try:
        resp.raise_for_status()
    except:
        raise RuntimeError(f'HTTP status {resp.status_code}: {url}: {resp.text}')


def usage(exit_status):
    print(f'USAGE: {os.path.basename(__file__)} <network-id> <creative-template-id>')
    exit(exit_status)


HEADERS = {'x-adzerk-apikey': getenv('ADZERK_API_KEY')}


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage(1)

    network = sys.argv[1]
    creative_template = sys.argv[2]

    delete_contentdb(network, 'Template', f'Extensions{creative_template}')
