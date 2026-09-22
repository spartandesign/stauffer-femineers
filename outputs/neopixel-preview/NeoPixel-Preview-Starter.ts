// Add the Microsoft "neopixel" extension in MakeCode before pasting.
// W-labeled micro:bit only. Default: 12 standard GRB-order RGB pixels on P0.
// Bench-test on the completed, verified harness before student use.
let PIXEL_COUNT = 12
let strip = neopixel.create(DigitalPin.P0, PIXEL_COUNT, NeoPixelMode.RGB)
strip.setBrightness(40)
strip.clear()
strip.show()

input.onButtonPressed(Button.A, function () {
    strip.showColor(neopixel.rgb(255, 0, 255))
})

input.onButtonPressed(Button.B, function () {
    strip.clear()
    for (let i = 0; i < PIXEL_COUNT; i++) {
        if (i % 2 == 0) {
            strip.setPixelColor(i, neopixel.rgb(0, 255, 255))
        } else {
            strip.setPixelColor(i, neopixel.rgb(0, 0, 255))
        }
    }
    strip.show()
})

input.onButtonPressed(Button.AB, function () {
    strip.clear()
    strip.show()
})
