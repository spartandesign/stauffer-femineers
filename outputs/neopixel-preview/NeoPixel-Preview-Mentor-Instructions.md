# NeoPixel preview: mentor preparation for September 24

Prepare a tabletop demonstration with two button-controlled light patterns and an A+B lights-off command. Build and check one complete example before duplicating it. For Thursday, one demonstration system plus one identical tested spare is a practical starting point; add hands-on systems only to match the supervised group size.

**Order checked:** the Stauffer order identifies the strip as BTF-LIGHTING WS2812B/ECO, Amazon ASIN B088BPGMXB, and lists the harness consumables. Two points remain unresolved: the physical connection to micro:bit P0/GND and confirmation of the data-interface compatibility for the delivered strip and battery supplies. No dedicated breakout, crocodile leads, or level shifter is listed in the populated Stauffer order. These systems have not been physically assembled or tested by Codex.

## Stauffer order findings

Source: [Stauffer order, rows 17-36](https://docs.google.com/spreadsheets/d/12Vz_3wxPcU4_DL9g7hyvn1MOQ-3SmjVzx2BUPvUoqgs/edit#gid=2033800378&range=A17:G36), checked September 21, 2026. The relevant Quantity Received cells are blank: these are requested quantities, not confirmed stock on hand.

| Row | Requested part | Requested quantity / identified contents |
|---|---|---|
| 17 | BTF-LIGHTING WS2812B strip, B088BPGMXB | 4 rolls; density discrepancy below |
| 18 | GeeekPi micro:bit V2 Club Kit, B0BGRRYXSG | 4 ten-board kits: 40 boards, 40 USB cables, 40 two-cell holders, and 80 included AAA cells according to the linked kit listing |
| 19 | WMYCONGCONG switched 3 x AAA holders, B081C7FYY4 | 6 ten-packs = 60 holders |
| 20 | Amazon Basics AAA alkaline cells | 2 hundred-packs = 200 additional cells |
| 21-23 | BNTECHGO 22 AWG silicone wire | 3 x 100-foot spools; black, yellow, and one color not named in the sheet |
| 24 | 330 ohm, 1/4 W, 1% resistors | 1 hundred-pack = 100 resistors |
| 25 | 1000 microfarad, 6.3 V electrolytic capacitors, B0GBYCXDH8 | Quantity 2; the linked listing is a twenty-pack, implying 40 capacitors if that variant was ordered |
| 30 | innhom heat-shrink assortment | 1 x 650-piece assortment; confirm suitable tubing sizes |
| 36 | ALITOVE 3-pin JST-SM connector sets, B071H5XCN5 | 3 twenty-set packs = 60 mating pairs; 15 cm, 20 AWG leads |

The [Club Kit listing](https://www.amazon.com/dp/B0BGRRYXSG) supplies ordinary board, USB, and battery accessories; it does not list a breakout or level shifter. The [manufacturer's Club Kit contents](https://52pi.com/products/bbc-micro-bit-v2-club-kit-10-pack-microbit-v2-go-kit-with-10-bbc-micro-bit-v2-boards-battery-holders-micro-usb-cable-20-aaa-batteries-for-coding-and-programming) agree. The [capacitor listing](https://www.amazon.com/dp/B0GBYCXDH8) establishes the twenty-pack size. M3 standoffs, nuts, and washers also appear in rows 49-51, but their presence does not establish a tested electrical connection method.

**Strip discrepancy:** row 17 says 30 LEDs/m (150 per 5 m roll), but [the specified ASIN currently selects 300 LEDs per 5 m roll, black PCB, IP30](https://www.amazon.com/dp/B088BPGMXB). That is 60 LEDs/m. Four matching rolls would provide 1200 pixels; the sheet description implies 600. Verify the delivered roll before allocating stock. For this preview, count **12 pixels** and cut only at a marked cut line: approximately 20 cm at 60/m or 40 cm at 30/m. The code remains set to 12 in either case.

**For one demo plus one spare, pull:** two W micro:bits, two included two-cell holders, two switched three-cell holders, ten fresh AAA cells, two 12-pixel strip segments, two 330 ohm resistors, two capacitors, two JST mating pairs, wire, heat-shrink, and two nonconductive mounting bases. Resolve the P0/GND connection and data interface before powering either set.

## 1. Gather these parts for each complete system

| Item | Quantity / specification |
|---|---|
| Wearables micro:bit V2 | 1, labeled W-NP-01 (or the matching set number) |
| RGB WS2812B-compatible strip | 1 segment of 12 pixels from the requested BTF-LIGHTING B088BPGMXB roll; verify the delivered density and marked cut line |
| micro:bit battery holder | 1 correct-polarity 2 x AAA holder with the proper micro:bit battery plug |
| Pixel battery holder | 1 switched 3 x AAA holder, subject to the strip's voltage specification |
| Batteries | 5 fresh AAA alkaline cells total; do not silently substitute a different chemistry |
| Data resistor | 1 x 330 ohm |
| Power capacitor | 1 x 1000 microfarad polarized electrolytic, rated at least 6.3 V (10 V is also suitable for this planned supply) |
| Removable strip connector | 1 mating pair of the requested ALITOVE three-pin JST-SM leads, with the actual pin mapping checked; this connector does not attach directly to the micro:bit edge |
| micro:bit signal connection | A suitable edge breakout or secure insulated connections to P0 and GND; do not solder directly to the micro:bit |
| Data interface, if required | A WS2812-compatible logic-level interface selected for the actual controller and pixel supply voltages |
| Assembly materials | Short insulated stranded wire, heat-shrink, strain relief, labels, and a nonconductive mounting base |

Shared tools: multimeter, wire stripper, soldering iron and solder, appropriate soldering workspace, heat-shrink tool, Windows laptop, USB data cable, and an iPad/phone for the demonstration video.

The 1000 microfarad capacitor and 330 ohm resistor fit Adafruit's published guidance. Verify capacitor polarity from its markings; its negative side usually has a stripe. [Adafruit power guidance](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)

## 2. Resolve the data connection before soldering

The micro:bit uses approximately 3 V logic; the planned three-cell pixel supply is nominally 4.5 V. Whether the strip recognizes that data signal reliably depends on its exact LED chip and both supplies. A direct P0 connection is not universally guaranteed by the name "WS2812B."

Check the strip's input-high specification against the controller's output over the intended battery range. If it does not meet that requirement, use a suitable level-shifting interface. Its operating-voltage range, direction, enable pins, and grounding must also match the system. Do not select a generic four-channel converter by appearance or assume a 5 V-only module remains in specification as three AAA cells discharge.

The order identifies a 5 V strip and nominally 4.5 V battery holders, but it does not supply the delivered LED chip's input-high specification or a level shifter. The functional diagram below therefore leaves that interface unresolved. Do not assume the order proves compatibility. The 330 ohm resistor protects the data connection; it does not raise its voltage. [Adafruit logic-level explanation](https://learn.adafruit.com/adafruit-neopixel-uberguide/logic-level)

## 3. Follow this functional wiring map

```text
2 x AAA holder -------- proper battery plug -------- micro:bit
                                                     |
                                                    P0
                                                     |
                                  [verified data interface]
                                                     |
                                                 330 ohm
                                                     |
                                                   DIN ---> pixel 0 ---> ... ---> pixel 11

3 x AAA holder (+), through its switch --------------- strip +V
                                                     |
                                               capacitor (+)
                                               capacitor (-)
                                                     |
3 x AAA holder (-) ---------------------------------- strip GND
                                                     |
micro:bit GND ----------------------------------------+
```

The capacitor is connected **across** the strip's +V and GND, not in series. Put the resistor close to the first pixel's DIN pad. Additional supply/enable connections for a level shifter must follow the identified module's documentation; they are not specified by this functional diagram.

**The three-cell positive supply never connects to the micro:bit's 3V ring or battery input.** The micro:bit and pixels share ground. The pixel strip gets power from its own holder. The micro:bit's operating supply must remain within its specified range. [micro:bit power documentation](https://tech.microbit.org/hardware/powersupply/)

## 4. Assemble the harness with all power removed

1. Remove the batteries and unplug USB. Count 12 pixels, locate the marked cut line, and identify the input end. Strip arrows point away from DIN toward the remaining pixels.
2. Identify the strip pads by their printed labels: +V, DIN, GND. Check the connector wires end-to-end with a meter. Do not infer their functions from wire colors or connector gender.
3. Plan the connector mapping and label both halves +V / DATA / GND. Arrange the supply side so energized contacts will be recessed when assembled. Keep the wires short.
4. Connect pixel-holder negative, strip ground, and micro:bit GND to the common ground. Connect pixel-holder switched positive to strip +V. Include the verified interface's documented connections if one is required.
5. Install the capacitor with its positive lead on strip +V and negative lead on common ground, near the strip input.
6. Complete P0 through the verified interface, then the 330 ohm resistor near DIN, then DIN. A direct interface is permitted only after the voltage compatibility check in section 2.
7. Inspect every joint for bridges or loose strands. Check point-to-point continuity against the labels with power removed. Confirm there is no sustained short between pixel +V and GND; a charging capacitor can cause a brief meter indication. Confirm pixel +V has not been joined to the micro:bit 3V ring.
8. Insulate exposed joints separately and add strain relief so pulling a lead cannot pull a solder pad off the strip. Secure the strip, holders, and board to a nonconductive base. Keep switches and buttons accessible.
9. With the holder disconnected from the harness, check its output polarity and voltage. Switch it off before reconnecting. Only power the assembled harness after inspection and the data-interface decision are complete.

Secure soldered leads and a resistor near DIN follow [Adafruit's connection guidance](https://learn.adafruit.com/adafruit-neopixel-uberguide/best-practices). This is an adult preparation task.

## 5. Load the starter program

1. Open [MakeCode for micro:bit](https://makecode.microbit.org/) and create a project named `Femineers-NeoPixel-Preview`.
2. Add the Microsoft `neopixel` extension. If searching does not locate it, use `https://github.com/microsoft/pxt-neopixel` in the extension search.
3. Switch to JavaScript and paste the contents of `NeoPixel-Preview-Starter.ts` from this folder. The default is **12 pixels, P0, brightness 40/255**. Change `PIXEL_COUNT` to the actual segment length if needed.
4. Disconnect both battery supplies and unplug the strip harness from the micro:bit before USB programming. Use only a W-labeled board, not an R-labeled Robotics board.
5. Download to the micro:bit and wait for the transfer to finish. Remove USB; reconnect the inspected, unpowered demonstration system.

Expected behavior: startup clears the strip; **A = all purple**, **B = alternating cyan and blue**, **A+B = all off**. The program has no repeating animation that could turn the lights back on after A+B. A+B clears the light output but does not electrically disconnect the system.

`NeoPixelMode.RGB` is the extension's standard GRB-order RGB strip mode. A different product may need a different color order; do not change wires to fix swapped colors. [Microsoft NeoPixel extension](https://makecode.microbit.org/pkg/microsoft/pxt-neopixel)

## 6. Bench-test each complete set

Use the actual batteries, strip, connector, harness, and board that will stay together on Thursday. This checklist is a suggested classroom rehearsal, not a substitute for component specifications.

- Start with both holders off and all connections secure. Power the pixels first, then the micro:bit. Startup should leave the strip dark.
- Press A. Confirm all 12 pixels display purple without flicker.
- Press A+B. Confirm every pixel goes dark and stays dark after button release.
- Press B. Confirm 12 pixels alternate cyan/blue from pixel 0 at the DIN end.
- Press A+B again. Confirm every pixel goes dark.
- Repeat that sequence five times; leave each pattern on for several minutes while observing it. Confirm the board resets to lights off.
- Check for damaged insulation, loose mounting, heat, odor, flicker, or unstable behavior. Stop and disconnect power for a fault; investigate with the system off.
- Run through three full shutdown/startup cycles. For shutdown: A+B, micro:bit power off, then pixel power off. For startup: pixels first, micro:bit second.
- Have another mentor repeat A, B, A+B, startup, and shutdown using only the labels.
- Record the set ID, strip model/count, interface used, battery type, code name, test date, tester, and any issue. Mark READY only after it passes.

Brightness 40 is a modest starting point from the program's 30-60 range; brightness alone does not establish electrical compatibility or a safe current budget. Keep the preview on the table.

## 7. Prepare the spare and video

Test the spare as a complete, separately labeled set. Keep its own board, strip, harness, and two holders together so a swap does not introduce untested parts.

Record a 30-60 second video of a physically working set: show the set label; point to the two power supplies, shared ground, P0/data path, and DIN arrow; demonstrate A, B, and A+B; then show shutdown. Save the clip locally on the presentation device and verify it plays without internet.

On Thursday, display the functional diagram and photograph of the actual tested wiring. Students operate buttons and explain the system. Any failed set goes to INSPECT as a whole; use the tested spare or video while an adult diagnoses it separately.

Program context: [existing student NeoPixel guide](../../meet-the-neopixels.html). Its direct-data sketch must be reconciled with the exact hardware before it is used as an assembly diagram.
