## Overview

* When a flight is created, upsert a ContentDB record containing the DMAs and/or
  zip codes the flight will target.
* When an ad is created, upsert a ContentDB record containing the ad units the
  ad will target.
* The `upsert-location-targeting` and `upsert-adunit-targeting` scripts show
  how to do this. (They all have a `-h` command line option to get usage and
  help info.)
* Sample location and adunit ContentDB records are provided in the `templates`
  directory. (Note that the sample records may be YAML files&mdash;ContentDB
  requires JSON.)
* The schema of the ContentDB records has been optimized for size: comma
  separated strings are used instead of JSON arrays for DMAs, zip codes, and ad
  units.

## Example

Suppose we have a flight (ID = 123) containing an ad (ID = 456).

### Configure Targeting (Ad/Flight Creation)

Create the location targeting ContentDB JSON payload:

```bash
cat <<EOT > location.json
{
  "dmas": "500,501,502",
  "zipcodes": "10124,20456,33139"
}
EOT
```

Upsert the record to ContentDB:

```bash
curl -s \
  -H x-adzerk-apikey:$ADZERK_API_KEY \
  -d @location.json \
  https://e-${networkid}.adzerk.net/cdb/${networkid}/custom/LocationTargeting/${flightid}
```

Create the ad unit targeting ContentDB JSON payload:

```bash
cat <<EOT > adunit.json
{
  "adunits": "dbea6999fffd48ac802c042cdf090a6d,2524916b616b47d6b205347c6a2a5764"
}
EOT
```

Upsert the record to ContentDB:

```bash
curl -s \
  -H x-adzerk-apikey:$ADZERK_API_KEY \
  -d @adunit.json \
  https://e-${networkid}.adzerk.net/cdb/${networkid}/custom/AdUnitTargeting/${adid}
```

### Make A Decision API Request

An example decision API JSON body which will match the targeting on the example
ad and flight:

```json
{
  "placements": [
    {
      "networkId": 777,
      "siteId": 42,
      "adTypes": [5]
    }
  ],
  "keywords": [
    "adunit=dbea6999fffd48ac802c042cdf090a6d",
    "dma=500"
  ]
}
```

or

```json
{
  "placements": [
    {
      "networkId": 777,
      "siteId": 42,
      "adTypes": [5]
    }
  ],
  "keywords": [
    "adunit=dbea6999fffd48ac802c042cdf090a6d",
    "zipcode=10124"
  ]
}
```
