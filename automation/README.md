# Automations

This folder contains Home Assistant automations split by topic. Each file holds one primary automation behavior.

## Files
- `ac_heat_schedule.yaml`: schedule-based AC heating control around alarm time.
- `ambiente.yaml`: ambient lighting scene automation.
- `armarios.yaml`: wardrobe/light-related automation.
- `auto_off_extractor_bano.yaml`: bathroom extractor auto-off logic.
- `autoenable_radiador_smart_mode.yaml`: re-enable smart mode for radiators.
- `humidity_rise_extractor_bano.yaml`: shower-oriented extractor activation. Require humidity at least 75%, at least 12 percentage points and 20% above its one-hour baseline, continuously for three minutes. Require valid readings, an off extractor, and at least 60 minutes since the last automatic activation. One activation per qualifying humidity episode; the trigger must clear before it can fire again. Manual control and the separate 15-minute auto-off remain unchanged.
- `is_holiday.yaml`: holiday/workday state automation.
- `luz_estudio.yaml`: studio light automation.
- `persianas_auto.yaml`: automatic blind/shutter automation for studio and Dario.
- `auto_radiadores.yaml`: external temperature-based radiator control.
- `globo_dario.yaml`: mirrors Globo Dario switch state to Globito light.
- `ventilador_dario.yaml`: detached Dario wall-switch presses toggle the corresponding ceiling light; fan state is unchanged.
- `ventilador_dormitorio.yaml`: detached bedroom wall-switch presses toggle the corresponding ceiling light; fan state is unchanged.
- `wallpanel_battery_charging.yaml`: starts/stops wallpanel charger based on battery thresholds.

## Bathroom humidity detection validation

Acceptance criteria: all humidity thresholds must hold continuously for three
minutes; invalid readings cancel qualification. The extractor must be off and
the previous automatic activation at least 60 minutes ago. A sustained high
reading does not repeatedly activate the extractor. The separate 15-minute
auto-off and manual controls retain their behavior. Pending three-minute
qualification is reset by an automation reload or Home Assistant restart.

On 2026-10-31, the logbook confirmed one humidity-driven activation in the
preceding 48 hours, at 22:17 Madrid time: humidity 69%, baseline 61.67%.
The user reported no showers during this period. Six other brief on/off cycles
had no automation attribution in the returned logbook data; their cause was
not established.

Validation in Home Assistant's template engine: the old rule accepted the
confirmed false activation; the revised rule rejected all 52 historical humidity
samples. Twelve synthetic threshold/invalid-reading cases and four cooldown
boundary cases passed. YAML checks confirm the three-minute trigger and off-state
guard. Thresholds are a conservative heuristic, not verified shower detection;
no confirmed shower trace was available. Sustained trigger timing and physical
response still require observation during a real shower.
