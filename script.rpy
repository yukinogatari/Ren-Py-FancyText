# The script of the game goes in this file.


init -1:
    # FancyText: To use this say screen, you need to add the three parameters exactly as given!
    screen say(who, what, slow_effect = slow_typewriter, slow_effect_delay = 0, always_effect = None):
        style_prefix "say"

        window:
            id "window"

            if who is not None:

                window:
                    id "namebox"
                    style "namebox"
                    text who id "who"
            
            # FancyText: Here's where all the magic happens.
            # Replace your usual "text" statement with "fancytext" to enable
            # some fancy effects on text display.
            fancytext what id "what" slow_effect slow_effect slow_effect_delay slow_effect_delay always_effect always_effect

define e = Character("Eileen")
define s = Character("Shaky", show_always_effect = always_shake(x = 1, y = 1))
define n = Character("", show_slow_effect = slow_fade, show_slow_effect_delay = 0.5)
define p = Character("Pulse", show_slow_effect = slow_slide_up(15), show_slow_effect_delay = 0.5, show_always_effect = always_pulse)
define r = Character("Rotate", show_slow_effect = slow_rotate, show_slow_effect_delay = 1.0)
define aah = Character("AAAA", show_slow_effect = slow_nonsense, show_slow_effect_delay = 1.0)

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "Here's a regular character, like you'd use in default Ren'Py."
    
    "To see the effects of FancyText in action, make sure reduce the text speed in the preferences menu before proceeding!"
    
    n "This is a narrator whose text gently fades in as it displays, instead of popping into existence like the normal typewriter display."
    
    s "And here's a shaky character, whose text is always shaking.\nIt's kind of like the dialogue in Celeste, except it only works on the whole line."
    
    r "Every letter in the dialogue of this character rotates 360 degrees after appearing, which is really annoying! I was unable to figure out how to change the origin of the rotation, so it only rotates around the top-left."
    
    p "This character's dialogue slides up into place, and then slowly pulses in and out. I don't know what you'd use it for, but it's kind of cool!"
    
    aah "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

    # This ends the game.

    return
