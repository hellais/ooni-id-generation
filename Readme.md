# OONI Measurement ID generation

This is a proposed solution to: https://github.com/TheTorProject/ooni-pipeline/issues/48.

The scheme proposed in here has the following properties:

1. IDs can be regenerated from the source data

2. Generated IDs are sorted (which is also nice because IDs close in time will
   be close together), though sorting is not strict.

My proposal for implementing this is actually twofold:

- We will regenerate all the historical IDs inside of measurements that are
  published via the API using functionality inside of this repo.

- We will add support for generating the IDs in this format on the serverside
  and "stamping" them onto reports when they are submitted to a collector.


The gist of how this ID generation scheme works within the context of OONI Reports is that we basically are customizing the generating of an ID of the xid flavour (see: https://github.com/rs/xid).

Instead of seeding the current time for the timestamp, we take the
`measurement_start_time`, instead of using the machineID and process ID for the
5 middle bytes, we use the `report_id`, instead of using a random 3-byte
counter, we use the offset or index into a particular measurement.

The script `make-id.py` includes a full example of how you can use this within
the context of the OONI Pipeline. In practice you can do
`gen_measurement_id(report_id, measurement_start_time, entry_index)`, where
`entry_index` is the line number (counting from zero) of the measurement being
looked at.
