# Scripts

This folder contains Home Assistant scripts split into individual files (`!include_dir_merge_named`).

## Files
- `toggle_blind.yaml`: shared wallpanel icon action; close above 50%, open to 90% at or below 50%, and ignore unavailable or missing positions.
- `set_radiador_config.yaml`: configure the base sensor and tuning parameters for each radiator.
- `set_radiador.yaml`: generic radiator target/valve adjustment routine.
