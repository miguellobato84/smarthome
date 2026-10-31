# Wallpanel Dashboard

This folder defines the wall-mounted tablet dashboard configuration.

Blind icons on the main view and the office/Dario icons on the blinds view call
`script.toggle_blind`: above 50% closes; at or below 50% opens to 90%.
Unknown or unavailable positions do nothing. The bedroom small blind card on the blinds view
remains read-only; main-view long presses still navigate to the blinds view.

Validation: Home Assistant template checks cover positions 0, 49, 50, 51, 90,
and 100, plus missing/unavailable positions. YAML checks cover all five icon
bindings and preserved navigation/read-only actions. Rendered tablet layout and
physical movement still require manual verification; browser access was disabled
during implementation.

## Files and folders
- `dashboard.yaml`: wallpanel settings and view includes.
- `views/`: split view definitions (main, robot, automations, heating).
