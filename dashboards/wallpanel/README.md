# Wallpanel Dashboard

This folder defines the wall-mounted tablet dashboard configuration.

Blind icons on the main view and all blind icons on the blinds view call
`script.toggle_blind`: above 50% closes; at or below 50% opens to 90%.
Unknown or unavailable positions do nothing. The bedroom small blind is manually controlled only and is excluded from
automations. Its wallpanel and Resumen card/icon taps use the same 90% opening
rule. Main-view long presses still navigate to the blinds view.

Validation: Home Assistant template checks cover positions 0, 49, 50, 51, 90,
and 100, plus missing/unavailable positions. YAML checks cover all six icon
bindings and preserved navigation actions. Rendered tablet layout and
physical movement still require manual verification; browser access was disabled
during implementation.

## Files and folders
- `dashboard.yaml`: wallpanel settings and view includes.
- `views/`: split view definitions (main, robot, automations, heating).
