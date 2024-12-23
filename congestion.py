import matplotlib.pyplot as plt
import numpy as np
import shapely

import config
import generator
import generator as g


# TODO this is a work in progress.
def fun(x, y, z):
    sum = 0;
    for xidx in range(len(x) - 1):
        for yidx in range(len(y) - 1):
            xval = x[xidx][0]
            yval = y[yidx][0]
            zval = z[xidx][yidx]
            z[xidx][yidx] = zval


def inject_c_in_congestion(z, l, r, rows, cols, dx, dy):
    for row_idx in range(rows):
        bot = row_idx * dy
        for col_idx in range(cols):
            left = col_idx * dx
            box = shapely.box(left, bot, left + dx, bot + dy)
            if shapely.intersects(l, box):
                z[row_idx][col_idx] = z[row_idx][col_idx] + 1
    return z


def determine_congestion(a_db):
    cfg = config.Config()
    ds = cfg.get_pin_ds()
    box = a_db.die.rect.to_shapely_box()
    rows = round(a_db.die.rect.width() / ds);
    cols = round(a_db.die.rect.height() / ds);
    z = np.zeros(shape=(rows, cols), dtype=np.float64)

    for c in a_db.connections:
        inject_c_in_congestion(z, c.line, box, rows, cols, ds, ds)
    return z


def make_data(a_db, z):
    cfg = config.Config()
    ds = cfg.get_pin_ds()
    box = a_db.die.rect

    X = np.arange(box.left(), box.right(), ds)
    Y = np.arange(box.bottom(), box.top(), ds)
    X, Y = np.meshgrid(X, Y)
    fun(X, Y, z)
    return X, Y, z


a_db, drawing = generator.lattice_generator(0)
g.draw_db(drawing, a_db)
drawing.save_svg("foo.svg")
z = determine_congestion(a_db)

X, Y, Z = make_data(a_db, z)
# Z = function (X,Y)

fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, Z, cmap='cool', alpha=0.8)

ax.set_title('3D Contour Plot of Congestion', fontsize=14)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_zlabel('congestion', fontsize=12)
plt.show()

print("done")
