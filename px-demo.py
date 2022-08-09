#!/usr/bin/env python3

import datetime, json, os, requests


"""
This program creates a site, channel, advertiser, campaign, flight, creative,
and ad. It upserts the special ContentDB records which contain the ad unit,
zip code, and DMA targeting for this flight and ad. Once these resources are
created a report is printed in JSON format including the new campaign's name
and some sample decision API request payloads you can use for testing.
"""


###############################################################################
# REQUIRED CONFIGURATION: YOU MUST EDIT THE FOLLOWING VALUES
###############################################################################


API_KEY             = None  # Your Kevel API key.
NETWORK             = None  # Your Kevel Network ID.
CREATIVE_TEMPLATE   = None  # The ID of your creative template.


###############################################################################
# OPTIONAL CONFIGURATION
###############################################################################


NAME        = f'kevel px-demo {datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}'
AD_TYPE     = 5
DMAS        = '500,501,502,503'
ZIPCODES    = '10465,10123,33139,27587'
ADUNITS     = 'c82dddf72ac045a6895b9f0491d1d25b,3d957e5c107948b99fb4e037273638ad,06f76f88fa4a42afb25c8b246282bc27,c57785b914cf40ad96758115e1e127e6,290f1ad47dab4416806b915afe0c10ec,1e7b5310b80d471e979f2b94ae7f6486'


###############################################################################
# GENERAL HELPER FUNCTIONS
###############################################################################


HEADERS = {'x-adzerk-apikey': API_KEY}


def first_comma(x):
    return x.split(',')[0]


###############################################################################
# MANAGEMENT API HELPER FUNCTIONS
###############################################################################


def mgt_api(endpoint, json):
    url = f'https://api.kevel.co/v1/{endpoint}'
    resp = requests.post(url, headers=HEADERS, json=json)
    try:
        resp.raise_for_status()
    except:
        print(f'{url}:', resp.text)
        raise
    return resp.json().get('Id')


def create_site():
    json = {'Title': NAME, 'URL': 'https://example.com'}
    return mgt_api('site', json)


def create_channel():
    json = {'Title': NAME, 'AdTypes': [AD_TYPE], 'Engine': 0}
    return mgt_api('channel', json)


def create_channel_site_map(site, channel):
    json = {'SiteId': site, 'ChannelId': channel, 'Priority': 1}
    return mgt_api('channelSite', json)


def get_priorities(channel):
    resp = requests.get(f'https://api.kevel.co/v1/channel/{channel}/priorities', headers=HEADERS)
    resp.raise_for_status()
    return list(map(lambda x: x['Id'], sorted(resp.json(), key=lambda x: x['Weight'])))


def create_advertiser():
    json = {'Title': NAME, 'IsActive': True}
    return mgt_api('advertiser', json)


def create_campaign(advertiser):
    json = {'AdvertiserId': advertiser, 'Name': NAME, 'IsActive': True}
    return mgt_api('campaign', json)


def create_flight(campaign, priority):
    json = {'Name': NAME,
            'StartDateISO': datetime.datetime.now().strftime('%Y-%m-%d'),
            'CampaignId': campaign,
            'PriorityId': priority,
            'GoalType': 2,
            'Impressions': 100,
            'IsActive': True}
    return mgt_api('flight', json)


def create_creative(advertiser):
    json = {'Title': NAME,
            'AdvertiserId': advertiser,
            'AdTypeId': AD_TYPE,
            'IsActive': True,
            'TemplateId': CREATIVE_TEMPLATE,
            'TemplateValues': '{}'}
    return mgt_api('creative', json)


def create_ad(creative, flight):
    json = {'Creative': {'Id': creative}, 'FlightId': flight, 'IsActive': True}
    return mgt_api(f'flight/{flight}/creative', json)


###############################################################################
# CONTENTDB API HELPER FUNCTIONS
###############################################################################


def upsert_contentdb(schema_name, content_key, json):
    url = f'https://e-{NETWORK}.adzerk.net/cdb/{NETWORK}/custom/{schema_name}/{content_key}'
    resp = requests.post(url, headers=HEADERS, json=json)
    try:
        resp.raise_for_status()
    except:
        print(f'{url}:', resp.text)
        raise


###############################################################################
# MAIN PROGRAM
###############################################################################


def main():

    ###########################################################################
    # CREATE ENTITIES
    ###########################################################################

    # create inventory
    site = create_site()
    channel = create_channel()
    create_channel_site_map(site, channel)
    priority = get_priorities(channel)[0]

    # create campaign
    advertiser = create_advertiser()
    campaign = create_campaign(advertiser)

    # create flight
    flight = create_flight(campaign, priority)

    # create ad 1 in flight 1
    creative = create_creative(advertiser)
    ad = create_ad(creative, flight)

    # create keyword targeting for flight 1
    upsert_contentdb('LocationTargeting', flight, {'dmas': DMAS, 'zipcodes': ZIPCODES})

    # create keyword targeting for ad 1 in flight 1
    upsert_contentdb('AdUnitTargeting', ad, {'adunits': ADUNITS})

    # IMPORTANT: the above ContentDB records must exist for each ad and flight
    # but they can be just an empty object (or the property value can be null)
    # if no targeting is desired.

    ###########################################################################
    # GENERATE SAMPLE DECISION API REQUEST PAYLOADS
    ###########################################################################

    placement = {
        'networkId': NETWORK,
        'siteId': site,
        'adTypes': [AD_TYPE],
    }

    adunit_keyword = f'adunit={first_comma(ADUNITS)}'

    decision_api_dma = {
        'placements': [placement],
        'keywords': [adunit_keyword, f'dma={first_comma(DMAS)}'],
    }

    decision_api_zipcode = {
        'placements': [placement],
        'keywords': [adunit_keyword, f'zipcode={first_comma(ZIPCODES)}'],
    }

    ###########################################################################
    # RESULT
    ###########################################################################

    return {
        'campaign_name': NAME,
        'sample_decision_api_requests': [decision_api_dma, decision_api_zipcode],
    }


if __name__ == '__main__':
    assert API_KEY is not None, 'API_KEY not configured (see comment in this file)'
    assert NETWORK is not None, 'NETWORK not configured (see comment in this file)'
    assert CREATIVE_TEMPLATE is not None, 'CREATIVE_TEMPLATE not configured (see comment in this file)'
    print(json.dumps(main(), indent=4))
