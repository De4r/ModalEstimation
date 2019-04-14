from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
'''
Ten skrypt wspolpracuje ze skrpytem Wizualizacja_postaci_drgan
'''

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().

    Source : stackoverflow.com
    Funkcja umożliwiająca wyrównanie skali na osiach wykresów 3D
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def obiekt(nodes, zapis='n', nazwa='obiekt', rzut=0):

    a = 1

    nodes = nodes
    print(nodes)

    noga1 = np.zeros((7, 3))
    noga2 = np.copy(noga1)
    noga3 = np.copy(noga1)
    noga4 = np.copy(noga1)

    rama1 = np.zeros((5, 3))
    rama2 = np.copy(rama1)
    rama3 = np.copy(rama2)
    rama4 = np.copy(rama3)
    rama5 = np.copy(rama1)
    rama6 = np.copy(rama2)
    rama7 = np.copy(rama3)

    ramie1 = np.zeros((4, 3))
    ramie2 = np.copy(ramie1)
    ramie3 = np.copy(ramie1)
    ramie4 = np.copy(ramie1)

    wspor1 = np.zeros((2, 3))
    wspor2 = np.copy(wspor1)
    wspor3 = np.copy(wspor1)
    wspor4 = np.copy(wspor1)
    wspor5 = np.copy(wspor1)
    wspor6 = np.copy(wspor1)
    wspor7 = np.copy(wspor1)
    wspor8 = np.copy(wspor1)

    [x, y] = np.shape(noga1)
    for i in range(x):
        noga1[i, :] = nodes[0 + i * 4, 1:4]
        noga2[i, :] = nodes[1 + i * 4, 1:4]
        noga3[i, :] = nodes[2 + i * 4, 1:4]
        noga4[i, :] = nodes[3 + i * 4, 1:4]

    [x, y] = np.shape(rama1)
    for i in range(x):
        if i < x - 1:
            rama1[i, :] = nodes[i, 1:4]
            rama2[i, :] = nodes[i + 4, 1:4]
            rama3[i, :] = nodes[i + 8, 1:4]
            rama4[i, :] = nodes[i + 12, 1:4]
            rama5[i, :] = nodes[i + 16, 1:4]
            rama6[i, :] = nodes[i + 20, 1:4]
            rama7[i, :] = nodes[i + 24, 1:4]
        else:
            rama1[i, :] = nodes[0, 1:4]
            rama2[i, :] = nodes[4, 1:4]
            rama3[i, :] = nodes[8, 1:4]
            rama4[i, :] = nodes[12, 1:4]
            rama5[i, :] = nodes[16, 1:4]
            rama6[i, :] = nodes[20, 1:4]
            rama7[i, :] = nodes[24, 1:4]

    ramie1[0, :] = nodes[12, 1:4]
    ramie1[1, :] = nodes[28, 1:4]
    ramie1[2, :] = nodes[31, 1:4]
    ramie1[3, :] = nodes[15, 1:4]

    ramie2[0, :] = nodes[13, 1:4]
    ramie2[1, :] = nodes[29, 1:4]
    ramie2[2, :] = nodes[30, 1:4]
    ramie2[3, :] = nodes[14, 1:4]

    ramie3[0, :] = nodes[20, 1:4]
    ramie3[1, :] = nodes[32, 1:4]
    ramie3[2, :] = nodes[35, 1:4]
    ramie3[3, :] = nodes[23, 1:4]

    ramie4[0, :] = nodes[21, 1:4]
    ramie4[1, :] = nodes[33, 1:4]
    ramie4[2, :] = nodes[34, 1:4]
    ramie4[3, :] = nodes[22, 1:4]

    wspor1[0, :] = nodes[28, 1:4]
    wspor1[1, :] = nodes[16, 1:4]

    wspor2[0, :] = nodes[31, 1:4]
    wspor2[1, :] = nodes[19, 1:4]

    wspor3[0, :] = nodes[29, 1:4]
    wspor3[1, :] = nodes[17, 1:4]

    wspor4[0, :] = nodes[30, 1:4]
    wspor4[1, :] = nodes[18, 1:4]

    wspor5[0, :] = nodes[32, 1:4]
    wspor5[1, :] = nodes[24, 1:4]

    wspor6[0, :] = nodes[35, 1:4]
    wspor6[1, :] = nodes[27, 1:4]

    wspor7[0, :] = nodes[33, 1:4]
    wspor7[1, :] = nodes[25, 1:4]

    wspor8[0, :] = nodes[34, 1:4]
    wspor8[1, :] = nodes[26, 1:4]

    fig = plt.figure(dpi=100, figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')
    ax.set_zticks([0, 200, 720, 1240, 1760, 2060, 2360])
    ax.tick_params(axis='both', which='major', labelsize=10, pad=6)
    ax.plot(xs=noga1[:, 0], ys=noga1[:, 1], zs=noga1[:, 2], color='b', linewidth=a)
    ax.plot(xs=noga2[:, 0], ys=noga2[:, 1], zs=noga2[:, 2], color='b', linewidth=a)
    ax.plot(xs=noga3[:, 0], ys=noga3[:, 1], zs=noga3[:, 2], color='b', linewidth=a)
    ax.plot(xs=noga4[:, 0], ys=noga4[:, 1], zs=noga4[:, 2], color='b', linewidth=a)

    ax.plot(xs=rama1[:, 0], ys=rama1[:, 1], zs=rama1[:, 2], color='b', linewidth=a)
    ax.plot(xs=rama2[:, 0], ys=rama2[:, 1], zs=rama2[:, 2], color='b', linewidth=a)
    ax.plot(xs=rama3[:, 0], ys=rama3[:, 1], zs=rama3[:, 2], color='b', linewidth=a)
    ax.plot(xs=rama4[:, 0], ys=rama4[:, 1], zs=rama4[:, 2], color='b', linewidth=a)
    ax.plot(xs=rama5[:, 0], ys=rama5[:, 1], zs=rama5[:, 2], color='b', linewidth=a)
    ax.plot(xs=rama6[:, 0], ys=rama6[:, 1], zs=rama6[:, 2], color='b', linewidth=a)
    ax.plot(xs=rama7[:, 0], ys=rama7[:, 1], zs=rama7[:, 2], color='b', linewidth=a)

    ax.plot(xs=ramie1[:, 0], ys=ramie1[:, 1], zs=ramie1[:, 2], color='b', linewidth=a)
    ax.plot(xs=ramie2[:, 0], ys=ramie2[:, 1], zs=ramie2[:, 2], color='b', linewidth=a)
    ax.plot(xs=ramie3[:, 0], ys=ramie3[:, 1], zs=ramie3[:, 2], color='b', linewidth=a)
    ax.plot(xs=ramie4[:, 0], ys=ramie4[:, 1], zs=ramie4[:, 2], color='b', linewidth=a)

    ax.plot(xs=wspor1[:, 0], ys=wspor1[:, 1], zs=wspor1[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor2[:, 0], ys=wspor2[:, 1], zs=wspor2[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor3[:, 0], ys=wspor3[:, 1], zs=wspor3[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor4[:, 0], ys=wspor4[:, 1], zs=wspor4[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor5[:, 0], ys=wspor5[:, 1], zs=wspor5[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor6[:, 0], ys=wspor6[:, 1], zs=wspor6[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor7[:, 0], ys=wspor7[:, 1], zs=wspor7[:, 2], color='b', linewidth=a)
    ax.plot(xs=wspor8[:, 0], ys=wspor8[:, 1], zs=wspor8[:, 2], color='b', linewidth=a)

    [x, y] = np.shape(nodes)
    for i in range(x):
        ax.scatter(xs=nodes[i, 1], ys=nodes[i, 2], zs=nodes[i, 3], color='b', alpha=0.8, s=2)
        ax.text(x=nodes[i, 1], y=nodes[i, 2], z=nodes[i, 3], s=str(i + 1), size=8, zorder=1, color='k')

    ax.set_xlabel('$X[mm]$', fontsize=10, labelpad=0)
    ax.set_ylabel('$Y[mm]$', fontsize=10, labelpad=0)
    ax.set_zlabel('$Z[mm]$', fontsize=10, labelpad=0) #rotation=0
    set_axes_equal(ax)
    # aktywowanie jednego z poniższych w celu zapisu rzutu:
    if rzut == 0:
        ax.view_init(elev=27, azim=-34) # ukośny
    elif rzut == 1:
        ax.view_init(elev=90, azim=0) # z gory
    elif rzut == 2:
        ax.view_init(elev=0, azim=0) # z przodu
    elif rzut == 3:
        ax.view_init(elev=0, azim=-90) # z boku

    if zapis == 'n':
        plt.show()
    elif zapis == 'y':
        plt.savefig(f'{nazwa}-{rzut}.png', format='png', dpi=300)