
import numpy
import time

import Reader


def trilinear_interpolate(src, minInt, ssp, sra, grid):
    height = src.shape[0]
    width = src.shape[1]
    out = numpy.zeros(src.shape)
    for w in range(width):
        for h in range (height):
            d = src[h,w] -  minInt
            gh = (h/ssp)
            gw = (w/ssp)
            gd = (d/sra)
            ghh = gh+1
            gww = gw+1
            gdd = gd+1
            out[h,w] = round( (
                grid[gh,gw,gd,0]*(ghh*ssp - h)*(gww*ssp - w)*(gdd*sra - d)+
                grid[ghh,gw,gd,0]*(h - gh*ssp)*(gww*ssp - w)*(gdd*sra - d)+
                grid[gh,gww,gd,0]*(ghh*ssp - h)*(w - gw*ssp)*(gdd*sra - d)+
                grid[gh,gw,gdd,0]*(ghh*ssp - h)*(gww*ssp - w)*(d - gd*sra)+
                grid[ghh,gw,gdd,0]*(h - gh*ssp)*(gww*ssp - w)*(d - gd*sra)+
                grid[gh,gww,gdd,0]*(ghh*ssp - h)*(w - gw*ssp)*(d - gd*sra)+
                grid[ghh,gww,gd,0]*(h - gh*ssp)*(w - gw*ssp)*(gdd*sra - d)+
                grid[ghh,gww,gdd,0]*(h - gh*ssp)*(w - gw*ssp)*(d - gd*sra)
            )/ (ssp*ssp*sra) )

    return out


def filterImage(path, sspatial, srange):
    intMatrix, minInt = Reader.readImage(path)
    start_time = time.time()

    width = intMatrix.shape[1]
    height = intMatrix.shape[0]
    depth = 255
    grid = numpy.zeros(((height/sspatial)+2,
                        (width/sspatial)+2,
                        (depth/srange)+2,
                        2))                         # S * R -space 3D
    # Filling 3D-grid
    for i in range(height):
        for j in range(width):
            vector = numpy.array([intMatrix[i,j],
                                  1]);
            intensity = vector[0]
            x = (i/sspatial)
            y = (j/sspatial)
            z = (intensity - minInt)/srange
            grid[x, y, z] += vector
            #print x, y, z, grid[x, y, z]

    # Convolution
    buffer = numpy.zeros(grid.shape)

    grid, buffer = buffer, grid
    for x in range(2, grid.shape[0] - 2):
        for y in range(2, grid.shape[1] - 2):
            for z in range(2, grid.shape[2] - 2):
                grid[x, y, z, 0] = (
                    (buffer[x, y-2, z, 0] + 4 * buffer[x, y-1, z, 0] + 6 * buffer[x, y, z, 0] + 4 * buffer[x, y+1, z, 0] + buffer[x, y+2, z, 0]) / 16.0)
                grid[x, y, z, 1] = (
                    (buffer[x, y-2, z, 1] + 4 * buffer[x, y-1, z, 1] + 6 * buffer[x, y, z, 1] + 4 * buffer[x, y+1, z, 1] + buffer[x, y+2, z, 1]) / 16.0)
                grid[x, y, z, 0] = (
                    (buffer[x-2, y, z, 0] + 4 * buffer[x-1, y, z, 0] + 6 * buffer[x, y, z, 0] + 4 * buffer[x+1, y, z, 0] + buffer[x+2, y, z, 0]) / 16.0)
                grid[x, y, z, 1] = (
                    (buffer[x-2, y, z, 1] + 4 * buffer[x-1, y, z, 1] + 6 * buffer[x, y, z, 1] + 4 * buffer[x+1, y, z, 1] + buffer[x+2, y, z, 1]) / 16.0)
                grid[x, y, z, 0] = (
                    (buffer[x, y, z - 2, 0] + 4 * buffer[x, y, z-1, 0] + 6*buffer[x, y, z, 0] + 4 * buffer[x, y, z+1, 0] + buffer[x, y, z+2, 0]) / 16.0)
                grid[x, y, z, 1] = (
                    (buffer[x, y, z - 2, 1] + 4 * buffer[x, y, z-1, 1] + 6*buffer[x, y, z, 1] + 4 * buffer[x, y, z+1, 1] + buffer[x, y, z+2, 1]) / 16.0)


    # Normilize grid
    for x in range(grid.shape[0]):
            for y in range (grid.shape[1]):
                for z in range(grid.shape[2]):
                    if (grid[x, y, z, 1] != 0):
                        grid[x, y, z] /= grid[x, y, z, 1]

    out = trilinear_interpolate(intMatrix, minInt, sspatial, srange, grid)

    print("--- %s seconds ---" % (time.time() - start_time))

    Reader.makeImage(out, "output.jpg");

filterImage("input.jpg", 10, 15)

#
# a = numpy.array([[1,2],[3,4]]);
# b = numpy.zeros(a.shape);
# print a
# print b
# a, b = b, a
# print a
# print b