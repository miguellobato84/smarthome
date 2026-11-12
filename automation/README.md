# Automations

This folder contains Home Assistant automations split by topic. Each file holds one primary automation behavior.

## Files
- `ac_heat_schedule.yaml`: schedule-based AC heating control around alarm time.
- `ambiente.yaml`: ambient lighting scene automation.
- `armarios.yaml`: wardrobe/light-related automation.
- `auto_off_extractor_bano.yaml`: bathroom extractor auto-off logic.
- `autoenable_radiador_smart_mode.yaml`: re-enable smart mode for radiators.
- `humidity_rise_extractor_bano.yaml`: bath-oriented extractor activation. Require humidity at least 75%, at least 4 percentage points and 5% above its one-hour baseline, continuously for 30 seconds. Require valid readings, an off extractor, and at least 60 minutes since the last automatic activation. One activation per qualifying humidity episode; the trigger must clear before it can fire again. Manual control and the separate 15-minute auto-off remain unchanged.
- `is_holiday.yaml`: holiday/workday state automation.
- `luz_estudio.yaml`: studio light automation.
- `persianas_auto.yaml`: automatic blind/shutter automation for studio and Dario.
- `auto_radiadores.yaml`: external temperature-based radiator control.
- `globo_dario.yaml`: mirrors Globo Dario switch state to Globito light.
- `ventilador_dario.yaml`: detached Dario wall-switch presses toggle the corresponding ceiling light; fan state is unchanged.
- `ventilador_dormitorio.yaml`: detached bedroom wall-switch presses toggle the corresponding ceiling light; fan state is unchanged.
- `wallpanel_battery_charging.yaml`: starts/stops wallpanel charger based on battery thresholds.

## Bathroom humidity detection validation

Acceptance criteria: humidity must be at least 75%, at least 4 percentage
points and 5% above the one-hour mean, continuously for 30 seconds. Invalid
readings cancel qualification. The extractor must be off and the previous
automatic activation at least 60 minutes ago. A sustained high reading does
not repeatedly activate the extractor. The separate 15-minute auto-off and
manual controls retain their behavior. Pending 30-second qualification is
reset by an automation reload or Home Assistant restart.

On 2026-10-31, the logbook confirmed one humidity-driven activation in the
preceding 48 hours, at 22:17 Madrid time: humidity 69%, baseline 61.67%.
The user reported no showers during this period. Six other brief on/off cycles
had no automation attribution in the returned logbook data; their cause was
not established.

The earlier rule rejected all 52 historical humidity samples in Home Assistant's
template engine; it also rejected the known false activation at 69% because of
the 75% floor. Recent history shows two user-reported bath events meeting the
updated thresholds: yesterday at 20:17, humidity rose from 84% (one-hour mean
74%) to 92% (mean 80%); today at 18:15, it rose from 91% (mean 84.33%) to 96%
(mean 87.25%). The 30-second hold fits both recorded rises. The revised rule has
not been replayed against all 52 historical samples. These thresholds remain a
heuristic; actual activation and physical response require runtime observation.
