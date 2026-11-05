import numpy as np
import ipywidgets as widgets
from IPython.display import display

# ---------- settings (edit to match your cube) ----------
COLOURS = {'W': '#ffffff', 'Y': '#ffd500', 'R': '#c41e3a',
           'O': '#ff5800', 'G': '#009b48', 'B': '#0046ad'}
ORDER = list(COLOURS)
FACES = ['U', 'L', 'F', 'R', 'B', 'D']
CENTRE = {'U': 'Y', 'L': 'G', 'F': 'O', 'R': 'B', 'B': 'R', 'D': 'W'}
# my inference from your solved array: layer0=U(2), layer2=D(1), row0=B(3), row2=F(4), col0=L(6), col2=R(5)
FACE_LABEL = {'D': 1, 'U': 2, 'B': 3, 'F': 4, 'R': 5, 'L': 6}

active = {'colour': 'W'}
buttons = {}
palette_buttons = {}
result = {'cube': None}          # read the converted cube from result['cube']

# ---------- palette ----------
status = widgets.HTML("Active colour: <b>W</b>")

def select_colour(b):
    active['colour'] = b.colour
    for k, pb in palette_buttons.items():
        pb.layout.border = '3px solid black' if k == b.colour else '1px solid #888'
    status.value = f"Active colour: <b>{b.colour}</b>"

for k in ORDER:
    pb = widgets.Button(tooltip=k, layout=widgets.Layout(width='42px', height='42px', margin='2px'))
    pb.colour = k
    pb.style.button_color = COLOURS[k]
    pb.on_click(select_colour)
    palette_buttons[k] = pb
palette_buttons['W'].layout.border = '3px solid black'
palette = widgets.HBox(list(palette_buttons.values()))

# ---------- net ----------
def paint(b):
    b.colour = active['colour']
    b.style.button_color = COLOURS[b.colour]

def make_face(face):
    rows = []
    for r in range(3):
        row = []
        for c in range(3):
            b = widgets.Button(layout=widgets.Layout(width='38px', height='38px', margin='1px'))
            b.colour = CENTRE[face]
            b.style.button_color = COLOURS[b.colour]
            if (r, c) != (1, 1):               # centres are fixed
                b.on_click(paint)
            buttons[(face, r, c)] = b
            row.append(b)
        rows.append(widgets.HBox(row))
    return widgets.VBox(rows, layout=widgets.Layout(margin='3px'))

faces = {f: make_face(f) for f in FACES}
blank = widgets.Box(layout=widgets.Layout(width='126px'))
net = widgets.VBox([
    widgets.HBox([blank, faces['U']]),
    widgets.HBox([faces['L'], faces['F'], faces['R'], faces['B']]),
    widgets.HBox([blank, faces['D']]),
])

# ---------- conversion to your 3x3x3 format ----------
def sticker_pos(axis, a, b, c):
    if axis == 0:
        return ('U', b, c) if a == 0 else ('D', 2 - b, c)
    if axis == 1:
        return ('B', a, 2 - c) if b == 0 else ('F', a, c)
    return ('L', a, b) if c == 0 else ('R', a, 2 - b)

def net_to_cube():
    colour_to_label = {buttons[(f, 1, 1)].colour: FACE_LABEL[f] for f in FACES}
    cube = np.zeros((3, 3, 3), dtype=int)
    weights = [100, 10, 1]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                idx, val = (a, b, c), 0
                for axis in range(3):
                    if idx[axis] == 1:
                        continue
                    face, r, col = sticker_pos(axis, a, b, c)
                    val += weights[axis] * colour_to_label[buttons[(face, r, col)].colour]
                cube[a, b, c] = val
    return cube

# ---------- buttons ----------
out = widgets.Output()
convert = widgets.Button(description='Convert', button_style='success')
reset = widgets.Button(description='Reset to solved', button_style='warning')

def on_convert(_):
    with out:
        out.clear_output()
        counts = np.bincount([ORDER.index(b.colour) for b in buttons.values()], minlength=6)
        if not (counts == 9).all():
            print("Invalid: each colour must appear exactly 9 times. Counts:", dict(zip(ORDER, counts)))
            return
        cube = net_to_cube()
        result['cube'] = cube
        print("Stored in result['cube']:")
        print(cube)
        try:
            print("Matches create_cube() (solved)?", np.array_equal(cube, create_cube()))
        except NameError:
            pass

def on_reset(_):
    for (f, r, c), b in buttons.items():
        b.colour = CENTRE[f]
        b.style.button_color = COLOURS[b.colour]
    with out:
        out.clear_output()
        print("Net reset to solved colours.")

convert.on_click(on_convert)
reset.on_click(on_reset)

def start_widget():
  display(widgets.HBox([widgets.HTML("<b>Palette:</b>&nbsp;"), palette, status]),
        net, widgets.HBox([convert, reset]), out)