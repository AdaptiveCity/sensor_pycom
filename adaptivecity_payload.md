# Adaptive City Payload format

Compact opinionated data format for low-power sensors.

This format is similar to Cayenne, but easier to read the hex and makes more consideration of custom expansion.

## Conventions in this specification

`[ ]` is used to represent a byte position in the payload. Letters within the brackets are either 0..F representing hex nibbles,
or some other letter (e..g N) meaning some value that will be explained in the text.

`{ }` is a label for an element type within the payload

A `sensor_type` is a type of sensor e.g. `ijl20` sensors have sensor type `7B` which determines the payload format.

A `feature` is a reading beginning with a `feature_type`, e.g. `temperature` is feature type `10`. The byte defining a feature type is always
even, and less than `E0`, and the least-significant bit of the feature can be toggled to indicate a negative reading. So
the first byte of a temperature feature can be `10` or `11` - this can be converted back to the feature type by `feature_type & 0xFE`.

## Payload format

The first byte gives the sensor type (so a decoder can use an appropriate lookup), while the following bytes are consecutive
blocks of information each containing a feature reading.

`[ sensor_type ]` `{ feature }` `...`

Defined values for sensor_type:

`7B`: `ijl20`, i.e. custom sensors using this format

## Feature format

Feature values have three formats, in each case the first byte tells you which format, and the number of bytes in this fragment
of the total payload is either defined by the `feature_type`. E.g. a temperature value is defined as 2 bytes, so that plus the
one byte used to explain this feature value is `temperature` means the total is 3 bytes.

1. `[FN] [XX] [YY] ...` This `[FN]` followed by `N` bytes is a free-for-all format (first nibble `F`) for a feature value,
so you can mix your data with other feature values keeping the Adaptive City Payload format.
    - the most-significant 4 bits of the first byte are `0000`
    - the least-significant 4 bits of the first byte (`N`) are the number of additional bytes in this feature reading 0..15
    - `[XX]` a byte defining your feature type (e.g. `elevator_floor_number` = `22`)
    - `[YY]...` an N-1 sequence of bytes representing your custom reading.
    - e.g. `[F3] [AB] [01] [23]`

2. `[EN] followed by N bytes` (first nibble `E`) is reserved for expansion.

3. `[feature_type] [XX] [YY]...` where `feature_type` is a *pre-defined type* less than `E0`. The underlying feature type will
always be even, and the least-significant-bit being `1` affecting the reading (typically making it negative). The `[XX] [YY] ...` bytes
are the reading value, with formats defined entirely by the `feature_type` (see below).

## Defined sensor types

`7B` - The `ijl20` sensor type, means the payload can be assumed to be in this format.

## Defined feature types

Note each feature type is listed as *even*, and the least-significant-bit may be set to indicate a negative reading. These formats
have generally been chosen to be reasonably compact but also readable in the hex.

`10` - Temperature (deg C): `[10] [12] [34]` means 12.34 degrees C. `[11] [12] [34]` means -12.34 degrees C.

`12` - Humidity (%): `[12] [44]`  means 44% humidity. `[13] [00]` means 100% humidity.

`14` - Light (lux): `[14] [12] [34] [56]` means 123456 lux.


`30` - Latitude: `[30] [12] [34] [56] [78]` means 12.345678. `[31] [12] [34] [56] [78]` means -12.345678

`32` - Longitude: `[32] [12] [34] [56] [78]` means 12.345678
