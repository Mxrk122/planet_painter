from asyncio.windows_events import NULL
from typing import Counter
from camera import Camera
import render
# importing the sys module
import sys

import color
import random

from Obj import *
 
# the setrecursionlimit function is
# used to modify the default recursion
# limit set by python. Using this,
# we can increase the recursion limit
# to satisfy our needs
 
sys.setrecursionlimit(10**8)


class gl(object):

    def __init__(self, filename):
        self.filename = filename
        self.r = render.Render()
    
    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width
        self.r.setSize(width, height)
    
    def glClearColor(self, r, g, b):
        self.r.set_clear_color(r, g, b)
    
    def glClear(self):
        self.r.clear()
    
    def glFinish(self):
        self.r.write(self.filename)

    def glViewPort(self, x, y, width, height):
        self.r.createViewPort(x, y, width, height)

    def glVertex(self, x, y):
        self.r.point(x, y)
    
    def glColor(self, r, g, b):
        self.r.set_vertex_color(r, g, b)

    def glClearViewPort(self):
        self.r.clearViewPort()
    
    def simplyPoint(self, x, y):
        self.r.simply_point(x,y)
    
    def glLine(self, x_0, y_0, x_1, y_1):
        self.r.line(x_0, y_0, x_1, y_1)
    
    def glLineNormal(self, x_0, y_0, x_1, y_1):
        self.r.line_normal(x_0, y_0, x_1, y_1)
    
    def glFill(self, x, y):
        oldColor = self.r.extractColor(x, y)
        self.r.fill(x, y, oldColor)
    
    def glSetFillColor(self, r, g, b):
        self.r.set_vertex_color(r, g, b)
    
    def glSetObject(self, objname):
        self.object = Obj(objname)

        return self.object
    
    def setShader(self, shader):
        sh = color.color_RGB_to_GBR(shader[0], shader[1], shader[2])
        self.r.shader = sh
    
    def glObjectMode(self, object: Obj, camera: Camera, scale, translate, rotate, current_color, texture=None):

        self.r.giveTexture(texture)

        o = object

        c = camera

        o.loadModelMatrix(scale, translate, rotate)

        for face in o.faces:
            if len(face) == 4:
                # Extraer caras
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                # REcibir coordenadas transformadas
                v1 = o.transform_vertex(o.vertex[f1], c.Viewport, c.projection, c.viewMatrix)
                v2 = o.transform_vertex(o.vertex[f2], c.Viewport, c.projection, c.viewMatrix)
                v3 = o.transform_vertex(o.vertex[f3], c.Viewport, c.projection, c.viewMatrix)
                v4 = o.transform_vertex(o.vertex[f4], c.Viewport, c.projection, c.viewMatrix)

                # Solo realizar si el usuario mando una textura
                if texture:
                    
                    # Extraer caras
                    
                    f1 = face[0][1] - 1
                    f2 = face[1][1] - 1
                    f3 = face[2][1] - 1
                    f4 = face[3][1] - 1


                    # REcibir coordenadas transformadas
                    vt1 = V3(
                        *o.texture_vertex[f1]
                    )
                    vt2 = V3(
                        *o.texture_vertex[f2]
                    )
                    vt3 = V3(
                        *o.texture_vertex[f3]
                    )
                    vt4 = V3(
                        *o.texture_vertex[f4]
                    )

                    # Shaders
                    if len(o.normal_vertex) > 0:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1
                        fn4 = face[3][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )
                        vn4 = V3(
                            *o.normal_vertex[fn3]
                        )

                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3), (vn1, vn2, vn3))

                        self.r.triangle((v1, v4, v3), current_color, (vt1, vt4, vt3), (vn1, vn4, vn3))
                    
                    else:
                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3))

                        self.r.triangle((v1, v4, v3), current_color, (vt1, vt4, vt3))
                else:

                    #Si no hay textura, solo pintar con colores
                    # Shaders
                    if len(o.normal_vertex) > 0:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1
                        fn4 = face[2][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )
                        vn4 = V3(
                            *o.normal_vertex[fn4]
                        )

                        self.r.triangle((v1, v2, v3), current_color, None, (vn1, vn2, vn3))

                        self.r.triangle((v1, v4, v3), current_color, None, (vn1, vn4, vn3))
                    
                    else:
                        self.r.triangle((v1, v2, v3), current_color)

                        self.r.triangle((v1, v4, v3), current_color)
                
                #print(f1, f2, f3, f4)


            if len(face) == 3:
                
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = o.transform_vertex(o.vertex[f1], c.Viewport, c.projection, c.viewMatrix)
                v2 = o.transform_vertex(o.vertex[f2], c.Viewport, c.projection, c.viewMatrix)
                v3 = o.transform_vertex(o.vertex[f3], c.Viewport, c.projection, c.viewMatrix)
                
                # Solo realizar si el usuario mando una textura
                if texture:
                    
                    # Extraer caras
                    f1 = face[0][1] - 1
                    f2 = face[1][1] - 1
                    f3 = face[2][1] - 1


                    # REcibir coordenadas transformadas
                    vt1 = V3(
                        *o.texture_vertex[f1]
                    )
                    vt2 = V3(
                        *o.texture_vertex[f2]
                    )
                    vt3 = V3(
                        *o.texture_vertex[f3]
                    )

                    # Shaders
                    if len(o.normal_vertex) > 0:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )

                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3), (vn1, vn2, vn3))
                    
                    else:
                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3))  

                else:

                    # si no hay textura, simplemente pintar el triangulo con colores
                    # Shaders
                    if len(o.normal_vertex) > 0:

                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )

                        self.r.triangle((v1, v2, v3), current_color, None, (vn1, vn2, vn3))
                    else:
                        self.r.triangle((v1, v2, v3), current_color)
        return o
    
    def glPlanetMode(self, object: Obj, camera: Camera, scale, translate, rotate, current_color, texture=None):

        self.r.giveTexture(texture)

        o = object

        c = camera

        o.loadModelMatrix(scale, translate, rotate)

        for face in o.faces:

            self.r.counter += 1

            if len(face) == 4:
                # Extraer caras
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                # REcibir coordenadas transformadas
                v1 = o.transform_vertex(o.vertex[f1], c.Viewport, c.projection, c.viewMatrix)
                v2 = o.transform_vertex(o.vertex[f2], c.Viewport, c.projection, c.viewMatrix)
                v3 = o.transform_vertex(o.vertex[f3], c.Viewport, c.projection, c.viewMatrix)
                v4 = o.transform_vertex(o.vertex[f4], c.Viewport, c.projection, c.viewMatrix)

                # Solo realizar si el usuario mando una textura
                if texture:
                    
                    # Extraer caras
                    
                    f1 = face[0][1] - 1
                    f2 = face[1][1] - 1
                    f3 = face[2][1] - 1
                    f4 = face[3][1] - 1


                    # REcibir coordenadas transformadas
                    vt1 = V3(
                        *o.texture_vertex[f1]
                    )
                    vt2 = V3(
                        *o.texture_vertex[f2]
                    )
                    vt3 = V3(
                        *o.texture_vertex[f3]
                    )
                    vt4 = V3(
                        *o.texture_vertex[f4]
                    )

                    # Shaders
                    if len(o.normal_vertex) > 0:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1
                        fn4 = face[3][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )
                        vn4 = V3(
                            *o.normal_vertex[fn3]
                        )

                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3), (vn1, vn2, vn3))

                        self.r.triangle((v1, v4, v3), current_color, (vt1, vt4, vt3), (vn1, vn4, vn3))
                    
                    else:
                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3))

                        self.r.triangle((v1, v4, v3), current_color, (vt1, vt4, vt3))
                else:

                    #Si no hay textura, solo pintar con colores
                    # Shaders
                    if len(o.normal_vertex) > 0:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1
                        fn4 = face[2][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )
                        vn4 = V3(
                            *o.normal_vertex[fn4]
                        )

                        self.r.triangle((v1, v2, v3), current_color, None, (vn1, vn2, vn3))

                        self.r.triangle((v1, v4, v3), current_color, None, (vn1, vn4, vn3))
                    
                    else:
                        self.r.triangle((v1, v2, v3), current_color)

                        self.r.triangle((v1, v4, v3), current_color)
                
                #print(f1, f2, f3, f4)


            if len(face) == 3:
                
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = o.transform_vertex(o.vertex[f1], c.Viewport, c.projection, c.viewMatrix)
                v2 = o.transform_vertex(o.vertex[f2], c.Viewport, c.projection, c.viewMatrix)
                v3 = o.transform_vertex(o.vertex[f3], c.Viewport, c.projection, c.viewMatrix)
                
                # Solo realizar si el usuario mando una textura
                if texture:
                    
                    # Extraer caras
                    f1 = face[0][1] - 1
                    f2 = face[1][1] - 1
                    f3 = face[2][1] - 1


                    # REcibir coordenadas transformadas
                    vt1 = V3(
                        *o.texture_vertex[f1]
                    )
                    vt2 = V3(
                        *o.texture_vertex[f2]
                    )
                    vt3 = V3(
                        *o.texture_vertex[f3]
                    )

                    # Shaders
                    if len(o.normal_vertex) > 0:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )

                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3), (vn1, vn2, vn3))
                    
                    else:
                        self.r.triangle((v1, v2, v3), current_color, (vt1, vt2, vt3))  

                else:

                    # si no hay textura, simplemente pintar el triangulo con colores
                    # Shaders
                    if len(o.normal_vertex) > 0:

                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1

                        vn1 = V3(
                            *o.normal_vertex[fn1]
                        )
                        vn2 = V3(
                            *o.normal_vertex[fn2]
                        )
                        vn3 = V3(
                            *o.normal_vertex[fn3]
                        )

                        self.r.triangle((v1, v2, v3), current_color, None, (vn1, vn2, vn3))
                    else:
                        self.r.triangle((v1, v2, v3), current_color)
        return o
    
    def glTriangle(self, A, B, C):
        print("Debuggeo en el triángulo")
        self.r.triangle(A, B, C)

    def glGiveTexture(self, texture):
        self.r.giveTexture(texture)

    def glPaintTexture(self, texture):
        self.r.framebuffer = texture

    
