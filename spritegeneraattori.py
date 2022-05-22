"""
Generoi miinaharavakirjaston käyttämät grafiikat.

@author: Mika Oja, Oulun yliopisto

Käyttää Pycairoa

https://www.cairographics.org/documentation/pycairo/3/index.html
"""

import cairocffi as cairo

W = 40
H = 40

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surface)

ctx.select_font_face("serif", weight=cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(32)

ctx.rectangle(0, 0, 40, 40)
ctx.set_source_rgb(190 / 255, 190 / 255, 190 / 255)
ctx.fill()

surface.write_to_png("spritet/ruutu_tyhja.png")

ctx.rectangle(2, 2, 36, 36)
ctx.set_source_rgb(230 / 255, 230 / 255, 230 / 255)
ctx.fill()

surface.write_to_png("spritet/ruutu_selka.png")

ctx.set_source_rgb(230 / 255, 20 / 255, 0 / 255)
x, y, tw, th, dx, dy = ctx.text_extents("!")
ctx.move_to(W / 2 - tw / 2 - 2, H / 2 + th / 2)
ctx.show_text("!")

surface.write_to_png("spritet/ruutu_lippu.png")

for i in range(1, 9): 
    ctx.rectangle(0, 0, 40, 40) 
    ctx.set_source_rgb(190 / 255, 190 / 255, 190 / 255)
    ctx.fill()
    
    if i in (1, 2):
        ctx.set_source_rgb(0 / 255, 20 / 255, 230 / 255)
    elif i in (3, 4):
        ctx.set_source_rgb(30 / 255, 100 / 255, 44 / 255)
    elif i in (5, 6): 
        ctx.set_source_rgb(230 / 255, 130 / 255, 0 / 255)
    else:
        ctx.set_source_rgb(230 / 255, 20 / 255, 0 / 255)
    
    x, y, tw, th, dx, dy = ctx.text_extents(str(i))
    ctx.move_to(W / 2 - tw / 2 - 2, H / 2 + th / 2)
    ctx.show_text(str(i))
        
    surface.write_to_png("spritet/ruutu_{}.png".format(i))
    
ctx.rectangle(0, 0, 40, 40)
ctx.set_source_rgb(190 / 255, 190 / 255, 190 / 255)
ctx.fill()

ctx.set_source_rgb(0 / 255, 0 / 255, 0 / 255)
x, y, tw, th, dx, dy = ctx.text_extents("X")
ctx.move_to(W / 2 - tw / 2, H / 2 + th / 2)
ctx.show_text("X")
    
surface.write_to_png("spritet/ruutu_miina.png".format(i))
