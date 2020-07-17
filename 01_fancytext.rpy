# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

python early:

    def slow_typewriter(st, gt, delay):
        return Transform()
    
    def slow_fade(st, gt, delay):
        t = Transform()
        
        t.alpha = 1.0

        if not gt == -1:
            
            if st < gt:
                t.alpha = 0.0
            
            elif st > gt + delay:
                t.alpha = 1.0
            
            else:
                t.alpha = float(st - gt) / float(delay)
        
        return t
    
    def _slow_slide(st, gt, delay, x = 0, y = 0):
        t = Transform()
        
        if not gt == -1:
            p = float(st - gt) / float(delay)
            
            if st < gt:
                t.alpha = 0.0
                t.xoffset = x
                t.yoffset = y
            
            elif st > gt + delay:
                t.alpha = 1.0
                t.xoffset = 0
                t.yoffset = 0
            
            else:
                t.alpha = p
                t.xoffset = x - (x * p)
                t.yoffset = y - (y * p)
        
        return t
    
    def slow_slide_up(y = 20):
        return renpy.partial(_slow_slide, y = y)
    def slow_slide_down(y = 20): 
        return renpy.partial(_slow_slide, y = -y)
    def slow_slide_right(x = 20):
        return renpy.partial(_slow_slide, x = -x)
    def slow_slide_left(x = 20): 
        return renpy.partial(_slow_slide, x = x)
    
    def _slow_shake(st, gt, delay, x = 0, y = 0):
        t = Transform()
        
        if not gt == -1:
            p = float(st - gt) / float(delay)
            
            if st < gt:
                t.alpha = 0.0
                t.xoffset = x
                t.yoffset = y
            
            elif st > gt + delay:
                t.alpha = 1.0
                t.xoffset = 0
                t.yoffset = 0
            
            else:
                t.alpha = 1.0
                t.xoffset = renpy.random.randint(-x, x)
                t.yoffset = renpy.random.randint(-y, y)
        
        return t
    
    def slow_shake(x = 0, y = 0):
        return renpy.partial(_slow_shake, x = x, y = y)
    
    def slow_rotate(st, gt, delay):
        t = Transform()
        
        if not gt == -1:
            p = float(st - gt) / float(delay)
            
            if st < gt:
                t.alpha  = 0.0
                t.rotate = 0.0
            
            elif st > gt + delay:
                t.alpha  = 1.0
                t.rotate = 0.0
            
            else:
                t.alpha  = 1.0
                t.rotate = 360.0 * p
        
        return t
    
    def _slow_shaking_slide(st, gt, delay, shake_x = 0, shake_y = 0, slide_x = 0, slide_y = 0):
        t = Transform()
        
        if not gt == -1:
            p = float(st - gt) / float(delay)
            
            if st < gt:
                t.alpha = 0.0
                t.xoffset = slide_x
                t.yoffset = slide_y
            
            elif st > gt + delay:
                t.alpha = 1.0
                t.xoffset = 0
                t.yoffset = 0
            
            else:
                t.alpha = p
                t.xoffset = slide_x - (slide_x * p) + renpy.random.randint(-shake_x, shake_x)
                t.yoffset = slide_y - (slide_y * p) + renpy.random.randint(-shake_y, shake_y)
        
        return t
    
    def slow_shaking_slide(shake_x = 0, shake_y = 0, slide_x = 0, slide_y = 0):
        return renpy.partial(_slow_shaking_slide, shake_x = shake_x, shake_y = shake_y, slide_x = slide_x, slide_y = slide_y)
    
    def slow_nonsense(st, gt, delay):
        t = Transform()
        
        if not gt == -1:
            p = float(st - gt) / float(delay)
            
            if st < gt:
                t.alpha  = 0.0
            
            elif st > gt + delay:
                t.alpha  = 1.0
            
            else:
                t.alpha = renpy.random.random()
                t.xoffset = renpy.random.randint(-10, 10)
                t.yoffset = renpy.random.randint(-10, 10)
                t.rotate  = renpy.random.randint(0, 360)
        
        return t

################################################################################
    
    def _always_shake(st, gt, delay, x = 0, y = 0):
        t = Transform()
        
        t.xoffset = renpy.random.randint(-x, x)
        t.yoffset = renpy.random.randint(-y, y)
        
        return t
    
    def always_shake(x = 0, y = 0):
        return renpy.partial(_always_shake, x = x, y = y)
    
    def always_pulse(st, gt, delay):
        import math
        return Transform(alpha = math.cos((st - gt - delay) * 2.0))

################################################################################
  
    class FancyText(renpy.text.text.Text):
    
        def __init__(self, text, slow_effect = slow_typewriter, slow_effect_delay = 0.0, always_effect = None, **properties):
            super(FancyText, self).__init__(text, **properties)
            
            self.slow_effect = slow_effect
            self.slow_effect_delay = slow_effect_delay
            self.always_effect = always_effect
      
        def render(self, width, height, st, at):
    
            import math

            if self.style.vertical:
                height, width = width, height

            # If slow is None, the style decides if we're in slow text mode.
            if self.slow is None:
                if self.style.slow_cps:
                    self.slow = True
                else:
                    self.slow = False

            if self.dirty or self.displayables is None:
                self.update()

            # Render all of the child displayables.
            renders = { }

            for i in self.displayables:
                renders[i] = renpy.render(i, width, self.style.size, st, at)

            # Find the virtual-resolution layout.
            virtual_layout = self.get_virtual_layout()

            if virtual_layout is None or virtual_layout.width != width or virtual_layout.height != height:

                virtual_layout = renpy.text.text.Layout(self, width, height, renders, drawable_res=False, size_only=True)

                if len(renpy.text.text.virtual_layout_cache_new) > renpy.text.text.LAYOUT_CACHE_SIZE:
                    renpy.text.text.virtual_layout_cache_new.clear()

                renpy.text.text.virtual_layout_cache_new[id(self)] = virtual_layout

            # Find the drawable-resolution layout.
            layout = self.get_layout()

            if layout is None or layout.width != width or layout.height != height:

                layout = renpy.text.text.Layout(self, width, height, renders, splits_from=virtual_layout)

                if len(renpy.text.text.layout_cache_new) > renpy.text.text.LAYOUT_CACHE_SIZE:
                    renpy.text.text.layout_cache_new.clear()

                renpy.text.text.layout_cache_new[id(self)] = layout

            # The laid-out size of this Text.
            vw, vh = virtual_layout.size
            w, h = layout.size

            # Get the list of blits we want to undertake.
            if not self.slow and not self.always_effect:
                blits = [ renpy.text.text.Blit(0, 0, w - layout.xborder, h - layout.yborder, left=True, right=True, top=True, bottom=True) ]
                redraw = None
            else:
                # TODO: Make this changeable.
                blits = self.blits_slow(layout, st)
                redraw = self.redraw_slow(layout, st)

            # Blit text layers.
            rv = renpy.Render(vw, vh)
            # rv = renpy.Render(*layout.unscale_pair(w, h))

            if renpy.config.draw_virtual_text_box:
                fill = renpy.Render(vw, vh)
                fill.fill((255, 0, 0, 32))
                fill.forward = layout.reverse
                fill.reverse = layout.forward

                rv.blit(fill, (0, 0))

            for o, color, xo, yo in layout.outlines:
                tex = layout.textures[o, color]

                if o:
                    oblits = outline_blits(blits, o)
                else:
                    oblits = blits

                for b in oblits:

                    b_x = b.x
                    b_y = b.y
                    b_w = b.w
                    b_h = b.h

                    # Bound to inside texture rectangle.
                    if b_x < 0:
                        b_w += b.x
                        b_x = 0

                    if b_y < 0:
                        b_h += b_y
                        b_y = 0

                    if b_w > w - b_x:
                        b_w = w - b_x
                    if b_h > h - b_y:
                        b_h = h - b_y

                    if b_w <= 0 or b_h <= 0:
                        continue

                    # Expand the blits and offset them as necessary.
                    if b.right:
                        b_w += layout.add_right
                        b_w += o

                    if b.bottom:
                        b_h += layout.add_bottom
                        b_h += o

                    if b.left:
                        b_w += layout.add_left
                    else:
                        b_x += layout.add_left

                    if b.top:
                        b_h += layout.add_top
                    else:
                        b_y += layout.add_top
                    
                    # We're cheating by using the alpha property to store a full
                    # Transform because other functions that use the Blit create
                    # them from scratch, so we'd lose anything we hacked in.
                    surf = tex.subsurface((b_x, b_y, b_w, b_h))
                    char = renpy.Render(b_w, b_h)
                    
                    if isinstance(b.alpha, Transform):
                        trans = b.alpha
                        
                        # Apply rotation
                        if trans.rotate:
                            theta = math.radians(trans.rotate)
                            c, s = math.cos(theta), math.sin(theta)
                            char.reverse = renpy.display.matrix.Matrix2D(c, -s, s, c)
                        
                        # Apply offset
                        char.absolute_blit(
                            surf,
                            (trans.xoffset, trans.yoffset)
                        )
                        
                        # Apply alpha
                        char.alpha = trans.alpha
                    
                    else:
                        char.absolute_blit(
                            surf,
                            (0, 0)
                        )

                    # Blit.
                    rv.absolute_blit(
                        char,
                        layout.unscale_pair(b_x + xo + layout.xoffset - o - layout.add_left,
                                            b_y + yo + layout.yoffset - o - layout.add_top)
                        )

            # Blit displayables.
            if layout.displayable_blits:

                self.displayable_offsets = [ ]

                drend = renpy.Render(w, h)
                drend.forward = layout.reverse
                drend.reverse = layout.forward

                for d, x, y, width, ascent, line_spacing, t in layout.displayable_blits:

                    if self.slow and t > st:
                        continue

                    xo, yo = renpy.display.core.place(
                        width,
                        ascent,
                        width,
                        line_spacing,
                        d.get_placement())

                    xo = x + xo + layout.xoffset
                    yo = y + yo + layout.yoffset

                    drend.absolute_blit(renders[d], (xo, yo))
                    self.displayable_offsets.append((d, xo, yo))

                rv.blit(drend, (0, 0))

            # Add in the focus areas.
            for hyperlink, hx, hy, hw, hh in layout.hyperlinks:

                h_x, h_y = layout.unscale_pair(hx + layout.xoffset, hy + layout.yoffset)
                h_w, h_h = layout.unscale_pair(hw, hh)

                rv.add_focus(self, hyperlink, h_x, h_y, h_w, h_h)

            # Figure out if we need to redraw or call slow_done.
            if self.slow and not self.always_effect:
                if redraw is not None:
                    renpy.display.render.redraw(self, redraw)
                else:
                    renpy.display.interface.timeout(0)
            
            elif self.always_effect:
                renpy.display.render.redraw(self, 0)

            rv.forward = layout.forward
            rv.reverse = layout.reverse

            if self.style.vertical:
                vrv = renpy.Render(rv.height, rv.width)
                vrv.forward = VERT_FORWARD
                vrv.reverse = VERT_REVERSE
                vrv.blit(rv, (rv.height, 0))
                rv = vrv

            return rv

################################################################################

        def blits_slow(self, layout, st):
            """
            Given a st and an outline, returns a list of blit objects that
            can be used to blit those objects.
            This also sets the extreme points when creating a Blit.
            """

            width, max_height = layout.size

            rv = [ ]

            if not layout.lines:
                return rv

            max_y = 0
            top = True
            
            if not self.always_effect:
                
                # First run through and blit any lines that are entirely complete.
                for l in layout.lines:

                    if l.max_time + self.slow_effect_delay > st:
                        break
                    
                    max_y = min(l.y + l.height + layout.line_overlap_split, max_height)
                
                else:
                    l = None

                if max_y:
                    rv.append(renpy.text.text.Blit(0, 0, width, max_y, top=top, left=True, right=True, bottom=(l is None)))
                    top = False
                
                if l is None:
                    return rv
            
            # Then go back through for any that *aren't* complete and blit as needed.
            for l in layout.lines:
                
                if not self.always_effect and st > l.max_time + self.slow_effect_delay:
                    continue

                for g in l.glyphs:
                    
                    if st < g.time and self.slow:
                        continue
                    
                    if self.slow_effect and self.slow and st < g.time + self.slow_effect_delay:
                        effect = self.slow_effect
                    elif self.always_effect:
                        effect = self.always_effect
                    else:
                        effect = self.slow_effect
                    
                    transform = None
                    if effect:
                        transform = effect(st, g.time, self.slow_effect_delay)
                    
                    left = False
                    right = False
                    if g is l.glyphs[0]:
                        left = True
                    
                    if g is l.glyphs[-1]:
                        right = True
                    
                    if transform is None:
                        continue
                    
                    rv.append(renpy.text.text.Blit(g.x, l.y, g.width, l.height + layout.line_overlap_split, alpha = transform, left=left, right=right, top=top, bottom=(l is layout.lines[-1])))

            return rv
        
        def redraw_slow(self, layout, st):
            """
            Return the time of the first glyph that should be shown after st.
            """

            for l in layout.lines:
                if not l.glyphs:
                    continue

                if l.max_time + self.slow_effect_delay > st:
                    break

            else:
                return None

            return 0

################################################################################

    renpy.register_sl_displayable("fancytext", FancyText, "text", 0, scope=True, replaces=True) \
        .add_positional("text") \
        .add_property("slow_effect") \
        .add_property("slow_effect_delay") \
        .add_property("always_effect") \
        .add_property("slow") \
        .add_property("slow_done") \
        .add_property("substitute") \
        .add_property("scope") \
        .add_property_group("text")

################################################################################