# Scripts

This folder contains Home Assistant scripts split into individual files (`!include_dir_merge_named`).

## Files
- `federico_habitacion.yaml`: clean by room name using an internal room-to-segment map.
- `federico_limpieza.yaml`: send robot to cleaning point.
- `federico_location.yaml`: locate robot.
- `federico_start.yaml`: start full cleaning.
- `federico_volver.yaml`: return robot to base.
- `set_radiador_config.yaml`: configure the base sensor and tuning parameters for each radiator.
- `set_radiador.yaml`: generic radiator target/valve adjustment routine.

## Federico Current Location (x/y)
For `roborock.vacuum.s5` (Federico), local miio status does not expose live `x/y` directly.
The reliable method is:
1. Get current `map_id` from LAN (`get_map_v1`).
2. Authenticate against Xiaomi Cloud.
3. Request signed map URL (`/home/getmapfileurl`).
4. Download and parse map data to extract robot and charger position.

### Libraries used
- `python-miio`: local LAN connection to the robot and `get_map_v1`.
- `requests`: Xiaomi Cloud login + API calls.
- `pycryptodome` (`Crypto.Cipher.ARC4`): RC4 encryption/decryption required by Xiaomi Cloud API.
- `vacuum-map-parser-roborock`: parse Roborock map binary.
- `vacuum-map-parser-base`: parser config/data structures used by the map parser.

### Methods/endpoints used
- LAN (robot):
  - `get_status`
  - `get_map_v1` -> returns `robomap%2F<did>%2F<index>` when map is ready (can return `retry` first).
- Xiaomi Cloud:
  - Login sequence:
    - `GET /pass/serviceLogin?sid=xiaomiio&_json=true`
    - `POST /pass/serviceLoginAuth2`
    - `GET <location>` to obtain `serviceToken`
  - Additional challenges may appear:
    - captcha (`code=87001`)
    - extra verification (`notificationUrl`)
  - Map URL:
    - `POST /app/home/getmapfileurl` with `obj_name=<map_id>` (RC4-signed request)
- Map parsing:
  - Gzip decompress map payload.
  - Parse with `RoborockMapDataParser`.
  - Read:
    - `vacuum_position` (`x`, `y`, `a`)
    - `charger_position` (`x`, `y`, `a`)
    - `vacuum_room_id`

### How the location script works
- Inputs:
  - Xiaomi account (`user`, `password`)
  - robot LAN `ip`
  - robot `token`
  - cloud region (`de`, `cn`, `us`, `sg`, etc.)
- Flow:
  - Connect LAN and resolve `map_id`.
  - Login cloud and resolve short-lived signed `map_url`.
  - Download map from `map_url`.
  - Parse map and print current coordinates and room id.

### Reconstruction checklist (no file dependency)
Implement a standalone Python script with these parts:
1. CLI arguments:
   - `user`, `password`, `country`, `ip`, `token`
   - optional tuning: map retries/wait, optional `map_id` override
2. LAN map id retrieval (`python-miio`):
   - connect to robot with `ip` + `token`
   - call `get_map_v1` until result is not `retry`
3. Xiaomi Cloud login (`requests`):
   - step 1: `serviceLogin`
   - step 2: `serviceLoginAuth2`
   - handle:
     - captcha (`code=87001`, `captchaUrl`)
     - extra verification (`notificationUrl`)
   - step 3: GET `location` and extract `serviceToken`
4. Encrypted cloud request for map URL:
   - call `/app/home/getmapfileurl` with `obj_name=<map_id>`
   - build RC4 encrypted params and signatures with:
     - nonce generation
     - signed nonce (`sha256`)
     - request signature (`sha1`)
     - RC4 encrypt/decrypt (`pycryptodome`)
5. Map download and parse:
   - download signed `map_url`
   - gunzip payload
   - parse with `RoborockMapDataParser` from `vacuum-map-parser-roborock`
6. Output JSON fields:
   - `map_id_raw`, `map_id_decoded`, `map_url`
   - `vacuum_position` (`x`, `y`, `a`)
   - `charger_position` (`x`, `y`, `a`)
   - `vacuum_room_id`, `rooms_count`

### Minimal dependencies
Install in any Python environment:
```bash
pip install python-miio requests pycryptodome vacuum-map-parser-roborock
```

### Typical output fields
- `map_id_raw`
- `map_id_decoded`
- `map_url`
- `vacuum_position` (`x`, `y`, `a`)
- `charger_position` (`x`, `y`, `a`)
- `vacuum_room_id`
- `rooms_count`

### Notes and caveats
- `map_url` is temporary (signed URL with expiration).
- Region matters; if `de` fails, try `cn`, `us`, `sg`, etc.
- Captcha/2FA may be required by Xiaomi depending on account risk checks.
- Keep robot token and Xiaomi credentials out of tracked files.
