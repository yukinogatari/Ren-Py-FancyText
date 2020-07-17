# Ren'Py FancyText Module

FancyText is a drop-in module for Ren'Py 7.3.5 that lets you display text on screens with a little more pizazz than vanilla.

![Sample](./example.gif)

### How to Use

Simply drop `01_fancytext.rpy` into your game's directory and you'll have access to the new `fancytext` screen language statement. `fancytext` is identical to the built-in `text`, but with three new parameters added.

* `slow_effect`: An effect that applies to each character of text as it's being displayed.
* `slow_effect_delay`: The time, in seconds, `slow_effect` will take to complete.
* `always_effect`: An effect that applies to each character of text for the duration that it's on-screen, after `slow_effect` has completed.

In simpler terms, this allows you to make your text gently fade in or slide in instead of the default "typewriter" effect in Ren'Py.

For specific examples and to see the effects in action, check out `script.rpy`, or drop the whole file into a new project.

#### Included Effects

Effects that begin with `slow_` are for use with the `slow_effect` parameter. Effects that have parameters must have those parameters provided.

* `slow_typewriter`: A non-effect that replicates the built-in typewriter effect.
* `slow_fade`: Slowly fades characters in over `slow_effect_delay` seconds.
* `slow_slide_up(y = 20)`: Slides the text up `y` pixels into place over `slow_effect_delay` seconds.
* `slow_slide_down(y = 20)`: Slides the text down `y` pixels into place over `slow_effect_delay` seconds.
* `slow_slide_right(x = 20)`: Slides the text right `x` pixels into place over `slow_effect_delay` seconds.
* `slow_slide_left(x = 20)`: Slides the text left `x` pixels into place over `slow_effect_delay` seconds.
* `slow_shake(x = 0, y = 0)`: Causes each character to shake for `slow_effect_delay` seconds with an intensity of `x` horizontal pixels and `y` vertical pixels.
* `slow_rotate`: Causes each character to rotate 360 degrees over `slow_effect_delay` seconds.
* `slow_shaking_slide(shake_x = 0, shake_y = 0, slide_x = 0, slide_y = 0)`: A combination of `slow_shake` and the `slow_slide` functions.
* `slow_nonsense`: Changes the position, alpha, and angle of every character wildly over `slow_effect_delay` seconds.

Effects that begin with `always_` are for use with the `always_effect` parameter, and will affect the text for as long as it's on screen

* `always_shake(x = 0, y = 0)`: Causes each character to shake with an intensity of `x` horizontal pixels and `y` vertical pixels.
* `always_pulse`: Causes the text to slowly cycle between visible and invisible.

Not all of these effects are practically useful, nor do I endorse them being used in games, but you do you.

### Advanced Usage

To create your own effects, all you have to do is write a function with the signature of `def slow_fade(st, gt, delay)` that returns a `Transform` object.

`st` is the current time. `gt` is the time at which the current glyph is expected to start displaying. And `delay` is the value of `slow_effect_delay` passed into the displayable, which is the amount of time the glyph has allotted to finish displaying.

In other words, when `st >= gt + delay`, the glyph is required to be in its final location (typically given by a default `Transform` object), otherwise slow display may not work as expected.

Right now, we only support a few transform parameters:

* alpha
* xoffset
* yoffset
* rotate

### License

The majority of the code used here is copied/modified from the Ren'Py source code, and as such, FancyText is released under the same license as Ren'Py itself. See LICENSE for more details.