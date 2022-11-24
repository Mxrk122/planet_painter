import gl
import texture
from vector3 import *
import camera
import math
import Obj


filename = 'result.bmp'


nvidia = gl.gl(filename)

nvidia.glCreateWindow(1000, 1000)

nvidia.glClearColor(0, 0, 0)

nvidia.glClear()


#Estas constantes se quedan asi
scale = (0.01, 0.01, 0.01)
translate = (2, 2, 0)
rotate = (0, 0, 0)
object_color = (0, 1, 1)

face = Obj.Obj("earth.obj")

#Correr textura
#t = texture.Texture("Nutella-milkshake.bmp")

# Definir las propiedades de la camara - Viewport y angulos de vision
# El viewport debe ser mas pequeño que el tamaño de imagen jeje
Camera = camera.Camera()

Camera.loadViewportMatrix(100, 100, 100, 100)

# Setear el shader
shader = (1, 0, 0)
nvidia.setShader(shader)

#High angle

Camera.lookAt(V3(0, 0, 20), V3(0, 0, 0), V3(0, 1, 0))
nvidia.glPlanetMode(face, Camera, scale, translate, rotate, object_color)


# Se escribio en prueba.bmp
nvidia.glFinish()
