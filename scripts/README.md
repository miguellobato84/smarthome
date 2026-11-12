# Scripts

This folder contains Home Assistant scripts split into individual files (`!include_dir_merge_named`).

## Files
- `toggle_blind.yaml`: shared wallpanel icon action; close above 50%, open to 90% at or below 50%, and ignore unavailable or missing positions.
- `set_radiador_config.yaml`: configure the base sensor and tuning parameters for each radiator.
- `update_radiador_external_temperatures.yaml`: refresh valid external temperature readings without overwriting them with missing sensor values.
- `set_radiador.yaml`: generic radiator target/valve adjustment routine.
