from mathstuff import cross_p
from vector3 import *
import MarkMatrix
import math

class Camera(object):

    #Encargada de dirigir el Viewport y el movimiento de la imagen
    #Propiedades
    
    Viewport = MarkMatrix.Matrix([
        [400, 0, 0, 400],
        [0, 500, 0, 500],
        [0, 0, 128, 128],
        [0, 0, 0, 1],
    ])

    viewMatrix = MarkMatrix.Matrix([
        [400, 0, 0, 400],
        [0, 500, 0, 500],
        [0, 0, 128, 128],
        [0, 0, 0, 1],
    ])

    projection = MarkMatrix.Matrix([
        [400, 0, 0, 400],
        [0, 500, 0, 500],
        [0, 0, 128, 128],
        [0, 0, 0, 1],
    ])




    # Funcion para manipular la viewmatrix
    def loadViewMatrix(self, x, y, z, center):
        Mi = MarkMatrix.Matrix([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1],
        ])

        Op = MarkMatrix.Matrix([
            [1, 0, 0, -center.x],
            [0, 1,0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1],
        ])

        self.viewMatrix = Mi * Op

    # Funcion para manipular la viewmatrix
    def loadProjectionMatrix(self, eye: V3, center: V3):
        cf = -1/(eye.length() - center.length())

        print("hola", cf)
        self.projection = MarkMatrix.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, cf, 1],
        ])

    # Funcion para manipular la viewmatrix
    def loadViewportMatrix(self, x, y, w, h):

        self.Viewport = MarkMatrix.Matrix([
            [w, 0, 0, x + w],
            [0, h, 0, y + h],
            [0, 0, 128, 128],
            [0, 0, 0, 1],
        ])

    def lookAt(self, eye: V3, center: V3, up: V3):
        z = (eye - center).normalize()
        x = cross_p(up, z).normalize()
        y = cross_p(z, x).normalize()


        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(eye, center)