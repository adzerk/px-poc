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
