import matplotlib.pyplot as plt
import numpy as np
import connector


conn = connector.Connector()
rows, result = conn.select_latest()

def drow_graph():
    xs, ys, zs, cs= [], [], [], []
    for row in rows:
        if (row == rows[104]) | (row == rows[113]) | (row == rows[139]) | (row == rows[143]) | (row == rows[150]) :
    #     xs, ys, zs, cs, bs =[], [], [], [], []
            x, y, cnt = 0, 0, 0
            ex = 0
            for char in row[0]:
                if char == "P":
                    x = x + 1
                elif char == "B":
                    y = y + 1
                cnt = cnt + 0.5 + 0.5
                if ex != x:   # x 중복 안되도록
                    ex = x
                    xs.append(x)
                    ys.append(y)
                    cs.append(cnt)

        xp = np.arange(0, 40, 0.5)
        a11 = sum([xx ** 2 for xx in xs])
        a12 = sum([xx for xx in xs])
        a21 = sum([xx for xx in xs])
        a22 = sum([1 for xx in xs])
        b2 = sum([yy for yy in ys])
        b1 = 0.0
        for ii in range(len(xs)):
            b1 = b1 + xs[ii] * ys[ii]
        A = np.array(((a11, a12), (a21, a22)))
        b = np.reshape(np.array((b1, b2)), (2, 1))
        X = np.linalg.solve(A, b)
        # print(X[0], X[1])
        yp = [X[0] * xx + X[1] for xx in xp]
        fig = plt.figure(0)
        ax = fig.add_subplot(111)
        plt.plot(xs, ys, 'o', xp, yp)
        ax.axis([-1, 40, -1, 40])
    plt.show()
        # plt.plot(xs, ys)
        # plt.plot(cs, bs)

drow_graph()