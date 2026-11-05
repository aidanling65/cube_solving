import numpy as np
import ipywidgets as widgets
from IPython.display import display

COLOURS = {'W': '#ffffff', 'Y': '#ffd500', 'B': '#0046ad',
           'O': '#ff5800', 'R': '#c41e3a', 'G': '#009b48', 'K': '#000000'}
ORDER = list(COLOURS)                       # W, Y, B, O, R, G, K
FACES = ['U', 'L', 'F', 'R', 'B', 'D']
CENTRE = {'U': 'Y', 'L': 'G', 'F': 'O', 'R': 'R', 'B': 'B', 'D': 'W'}
COLOUR_CODE = {'W': 1, 'Y': 2, 'B': 3, 'O': 4, 'R': 5, 'G': 6, 'K': 0}


def sticker_pos(axis, a, b, c):
    if axis == 0:
        return ('U', b, c) if a == 0 else ('D', 2 - b, c)
    if axis == 1:
        return ('B', a, 2 - c) if b == 0 else ('F', a, c)
    return ('L', a, b) if c == 0 else ('R', a, 2 - b)


def start_widget():
    active = {'colour': 'W'}
    buttons, palette_buttons = {}, {}
    result = {'cube': None, 'cubie_mask': None}

    status = widgets.HTML("Active colour: <b>W</b>")
    out = widgets.Output()
    strict = widgets.Checkbox(value=True, description='Strict (full, valid cube)', indent=False)

    # ---------- palette ----------
    def select_colour(b):
        active['colour'] = b.colour
        for k, pb in palette_buttons.items():
            pb.layout.border = '3px solid #e91e63' if k == b.colour else '1px solid #888'
        status.value = f"Active colour: <b>{b.colour}</b>"

    for k in ORDER:
        pb = widgets.Button(tooltip=k, layout=widgets.Layout(width='42px', height='42px', margin='2px'))
        pb.colour = k
        pb.style.button_color = COLOURS[k]
        pb.on_click(select_colour)
        palette_buttons[k] = pb
    palette_buttons['W'].layout.border = '3px solid #e91e63'
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
                b.colour = CENTRE[face] if (r, c) == (1, 1) else CENTRE[face]
                b.style.button_color = COLOURS[b.colour]
                b.on_click(paint)               # centres are paintable too (needed for masking)
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

    # ---------- conversion ----------
    def net_to_cube():
        cube = np.zeros((3, 3, 3), dtype=int)
        cubie_mask = np.zeros((3, 3, 3), dtype=bool)   # True = every sticker on this cubie is coloured
        weights = [100, 10, 1]
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    idx, val, stickers = (a, b, c), 0, []
                    for axis in range(3):
                        if idx[axis] == 1:
                            continue
                        face, r, col = sticker_pos(axis, a, b, c)
                        colour = buttons[(face, r, col)].colour
                        stickers.append(colour != 'K')
                        val += weights[axis] * COLOUR_CODE[colour]
                    cube[a, b, c] = val
                    cubie_mask[a, b, c] = bool(stickers) and all(stickers)
        return cube, cubie_mask

    def on_convert(_):
        with out:
            out.clear_output()
            colours = [b.colour for b in buttons.values()]
            if strict.value:
                if 'K' in colours:
                    print("Strict mode: black stickers aren't allowed. Untick Strict to mask pieces.")
                    return
                if any(buttons[(f, 1, 1)].colour != CENTRE[f] for f in FACES):
                    print("Strict mode: centres must keep their standard colours.")
                    return
                counts = {k: colours.count(k) for k in ORDER if k != 'K'}
                if any(v != 9 for v in counts.values()):
                    print("Strict mode: each colour must appear exactly 9 times. Counts:", counts)
                    return
            cube, cubie_mask = net_to_cube()
            result['cube'], result['cubie_mask'] = cube, cubie_mask
            print("Stored in result['cube'] and result['cubie_mask']")
            print(cube)
            print("Fully known cubies:", int(cubie_mask.sum()), "of 27")
            if strict.value:
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

    def on_black_all(_):
        for b in buttons.values():
            b.colour = 'K'
            b.style.button_color = COLOURS['K']

    convert = widgets.Button(description='Convert', button_style='success')
    reset = widgets.Button(description='Reset to solved', button_style='warning')
    black_all = widgets.Button(description='Blacken all')
    convert.on_click(on_convert)
    reset.on_click(on_reset)
    black_all.on_click(on_black_all)

    display(widgets.HBox([widgets.HTML("<b>Palette:</b>&nbsp;"), palette, status]),
            net, widgets.HBox([convert, reset, black_all, strict]), out)
    return result


if __name__ == "__main__":
    start_widget()