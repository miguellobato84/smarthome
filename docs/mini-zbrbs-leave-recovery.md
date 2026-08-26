# SONOFF MINI-ZBRBS: unexpected Zigbee leave and recovery

This runbook records the incident affecting the large bedroom shutter and the
safe recovery procedure. It applies to SONOFF `MINI-ZBRBS` roller-shutter
modules using Zigbee2MQTT (Z2M).

## Affected device

| Field | Value |
| --- | --- |
| Z2M name | `persiana_dormitorio_big` |
| Home Assistant entity | `cover.persiana_dormitorio_big` |
| IEEE address | `0xc02cedfffec07a55` |
| Model | SONOFF MINI-ZBRBS |
| Firmware | `1.0.5` (`fileVersion` 4101; date code 20250711) |
| Device type | Zigbee router, mains powered |
| External switch mode | `edge` (three-position rocker) |
| Travel calibration | calibrated |

## Incident summary

On 16 August 2026 at 12:04:54--12:04:55 CEST (10:04:54--10:04:55 UTC),
the device emitted three Zigbee `leaveInd` events and departed the network.
It then stopped responding to Z2M and Home Assistant commands. The scheduled
automation at 04:00 CEST on 17 August did run, but its command could not reach
the departed device (`MAC_NO_ACK`).

### Root cause

The physical external rocker was toggled rapidly while trying to make the
shutter move. In Edge mode, alternating the UP and DOWN keys **more than three
times within six seconds** is the MINI-ZBRBS factory-reset gesture. The
gesture caused the module to leave Zigbee and enter its reset/pairing flow.

This was not caused by the Home Assistant automation, MQTT, Z2M deleting the
device, or poor Zigbee link quality.

## Evidence timeline

| Time (CEST) | Evidence | Interpretation |
| --- | --- | --- |
| 16 Aug 12:04:52 | Device reported `motorRunStatus: Reverse`, link quality 42--54, and a closed position. | The module was online and receiving the physical switch action. |
| 16 Aug 12:04:53 | Device reported `motorRunStatus: Stop`, link quality 51. | A rapid follow-up rocker input stopped/reversed the motor almost immediately. |
| 16 Aug 12:04:54--55 | Three ZNP `ZDO leaveInd` events from `0xc02cedfffec07a55`. | The device had left the Zigbee network. |
| 17 Aug 04:00 | HA logged `automation.persiana_estudio` running; Z2M sent the position command and retried five times. | The automation ran correctly. |
| 17 Aug 04:00 | Z2M returned `MAC_NO_ACK`. | The target was no longer joined/reachable. |
| 17 Aug 05:17 | The same IEEE rejoined, received network address `0x4D42`, and sent live reports. | Recovery completed; no Z2M deletion was needed. |

### What the logs prove about the initial non-movement

Immediately before the leave, there was no Home Assistant or MQTT command for
this cover. The module itself reported a motor start followed one second later
by a stop, while it also reported the shutter as closed. Therefore the logs
rule out an automation, MQTT, or Zigbee-delivery failure at that moment.

They cannot establish a separate mechanical reason for any earlier apparent
non-movement: MINI-ZBRBS exposes no motor-current, output-voltage, limit-switch,
or relay-fault telemetry. If the problem recurs while the device remains
connected, investigate motor supply, wiring, mechanical limits, and the relay
load with an electrician.

## Why the Z2M ignore-leave extension was insufficient

The deployed Z2M external extension intercepts `deviceLeave` events for
`MINI-ZBRBS` and prevents Z2M from removing the device record. It worked: the
device stayed in the Z2M database.

It cannot prevent the physical module from leaving the Zigbee network. Once the
module has erased/left its network membership, it must rejoin before it can
receive commands. Keep the extension as database protection, but do not treat
it as a cure for the device-side reset gesture.

## Safe recovery procedure (no wall opening)

Do not delete the Z2M or Home Assistant device first. Rejoining with the same
IEEE address lets Z2M recover the existing device record and avoids needless
entity changes.

1. Open Z2M permit-join for a short, controlled window (for example, five
   minutes).
2. With the module powered, use the external three-position rocker: toggle UP
   and DOWN alternately more than three times within six seconds.
3. Wait for Z2M to detect the same IEEE address and finish its interview.
4. Confirm that Z2M receives live reports and that the device has a current
   network address. A changed short/network address is normal after rejoining.
5. Verify `external_trigger_mode` is `edge` and
   `motor_travel_calibration_status` is `Calibrated`.
6. Send one deliberate open or close command and confirm both movement and the
   reported position.

The documented alternative is holding the module's physical button for five
seconds. Use it only if accessible; it is not required for the external-rocker
recovery described above.

## Prevention

- Do not rapidly alternate the physical UP/DOWN rocker. In Edge mode this is a
  factory-reset gesture, not a normal pairing shortcut.
- If movement does not start, wait and diagnose before repeating commands.
  Opposite rocker inputs can stop/reverse the motor immediately.
- Before using the reset gesture intentionally, open permit-join first; the
  device otherwise may leave and remain offline.
- Do not install the withdrawn MINI-ZBRBS `1.1.0` OTA image. It was retracted
  because it was published with an incorrect image type.

## References

- [SONOFF MINI-ZBRBS user manual](https://www.smart-switch.cz/user/related_files/user_manual_mini-zbrbs_en.pdf)
- [Zigbee2MQTT issue: MINI-ZBRBS routers disappear and require re-pairing](https://github.com/Koenkk/zigbee2mqtt/issues/32633)
- [Zigbee2MQTT issue: unsolicited device-leave handling](https://github.com/Koenkk/zigbee2mqtt/issues/31990)
- [OTA repository issue: withdrawn MINI-ZBRBS 1.1.0 image](https://github.com/Koenkk/zigbee-OTA/issues/1272)
