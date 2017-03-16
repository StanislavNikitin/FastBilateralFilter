
import numpy as np
import math, time
import Reader


def gaussFunction(x, mu, sgm):
    return 1 / (math.sqrt(2*math.pi)*sgm) * math.e**(-0.5*(float(x-mu)/sgm)**2)


def filterImage(path, diam, sigmaspatial, sigmagrey):
    intMatrix, minInt = Reader.readImage(path)

    start_time = time.time()

    width = intMatrix.shape[1]
    height = intMatrix.shape[0]
    out = np.zeros(intMatrix.shape)

    for h in range(diam, height - diam):
        for w in range(diam, width - diam):
            # neighborjood in d
            intSum = 0.0
            norm = 0.0
            for hh in range(h - diam, h + diam):
                for ww in range(w - diam, w + diam):
                    dist = math.sqrt((h - hh) ** 2 + (w - ww) ** 2)
                    intDiff = math.fabs(intMatrix[h, w] - intMatrix[hh, ww])
                    weight = gaussFunction(dist, 0.0, sigmaspatial) * gaussFunction(intDiff, 0.0, sigmagrey)
                    intSum += weight * intMatrix[hh, ww]
                    norm += weight
            out[h, w] = round((intSum / norm))
            #if (intMatrix[h, w] != out[h, w]): print h, w, intMatrix[h, w], out[h, w], intSum, norm

    print("--- %s seconds ---" % (time.time() - start_time))

    Reader.makeImage(out, "slow.jpg")

filterImage("input.jpg", 15, 10, 10)