from asyncio.windows_events import NULL
from operator import truediv
import random
from typing import Counter
from mathstuff import *
from vector3 import *
import writeutilities as wu
import color


class Render(object):

    clear_color = color.color_RGB_to_GBR(0, 0, 0)
    vertex_color = color.color_RGB_to_GBR(1, 1, 1)
    fill_color = color.color_RGB_to_GBR(1, 1, 1)
    height = 1024
    width = 1024
    shader = None
    texture = None

    planet_size = 4096
    counter = 0
    

    def __init__(self):
        self.clear()

    # establecer el tamaño de nuestra imagen 
    def setSize(self, height, width):
        # self -> referencia a la propiedad de la clase
        self.height = height
        self.width = width
        self.vp_height = height
        self.vp_width = width

    # funcion para elegir el color del pincel
    def set_clear_color(self, r, g, b):

        self.clear_color = color.color_RGB_to_GBR(r, g, b)
    
    # funcion para elegir el color del pincel
    def set_color(self, r, g, b):
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)

        self.vertex_color = color.color_RGB_to_GBR(red, green, blue)
    
    # funcion para elegir el color del pincel
    def set_clear_vp_color(self, r, g, b):
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)

        self.clearvp_color = color.color_RGB_to_GBR(red, green, blue)

    # funcion para pintar todo el mapa de bits de un color
    def clear(self):
        self.framebuffer = [
            # for para rellenar el array -> generador
            # se pinta del color que indique clear_color
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

        self.z_framebuffer = [
            [-9999 for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # funcion para elegir el color del pincel
    def set_vertex_color(self, r, g, b):
        self.vertex_color = color.color_RGB_to_GBR(r, g, b)
    
    # Funcion para pintar un punto en el viewport
    def simply_point(self, x, y):
        if x < 0 or y < 0: 
            return NULL
        try: 
            self.framebuffer[y][x] = self.vertex_color
        except:
            return
    
    # Funcion para pintar en el zbuffer
    def simply_z(self, x, y, z):

        if x < 0 or y < 0:
            return False

        if len(self.z_framebuffer[0]) <= x or len(self.z_framebuffer) <= y:
            return False
        
        if (self.z_framebuffer[y][x] < z):
            self.z_framebuffer[y][x] = z
            return True

    # Funcion para pintar una linea dadas las coordenadas
    def line_normal(self, x0, y0, x1, y1):

        x0 = int(x0)
        x1 = int(x1)
        y0 = int(y0)
        y1 = int(y1)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx

        if steep:
            # Si la linea tiende a ser mas vertical, cambiar coordenadas
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            # si la linea va hacia "atras", darle la vuelta a los puntos
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        threshold = dx

        y = y0
        for x in range(x0, x1):
            if steep:
                self.simply_point(y, x)
            else:
                self.simply_point(x, y)

            offset += dy * 2

            if offset >= threshold:
                # si la linea va hacia arriba, aumentar una unidad
                if y0 < y1:
                    y += 1
                else:
                # si la linea va hacia abajo, disminuir una unidad
                    y -= 1
                # Aumentar el threshold cada vez
                threshold += dx * 2
    
    #Funcion para definir una textura a nuestro siguiente objeto a dibujar
    def giveTexture(self, texture):
        
        self.texture = texture
    
    def triangle(self, vertex, object_color, tvertex=(), nvertex=None):

        A, B, C = vertex

        nA, nB, nC = 0, 0, 0

        tA, tB, tC = 0, 0, 0

        if self.texture:
            tA, tB, tC = tvertex
        
        if nvertex:
            nA, nB, nC = nvertex

        Bmin, Bmax = bounding_box(A, B, C)

        Bmin.round()
        Bmax.round()

    
        for x in range(Bmin.x, Bmax.x + 1):
            for y in range(Bmin.y, Bmax.y + 1):
                    w, u, v = barycentric(A, B, C, V2(x, y))

                    if (w < 0 or v < 0 or u < 0):
                        continue

                    z = A.z * w + B.z * v + C.z * u
                    

                    if(self.simply_z(x, y, z)):

                        #Mandar variables al shader
                        self.vertex_color = self.paint_shader(
                            object_color = object_color,
                            barycentrics = (w, u, v),
                            vertices = (A, B, C),
                            t_vertices = (tA, tB, tC),
                            normals = (nA, nB, nC),
                            cords = (x, y)
                        )
                            
                        self.simply_point(x, y)

    
    # Emmbellecer detalles
    def paint_shader(render, **kwargs ):
        object_color = kwargs["object_color"]

        #292
        if render.counter > 1755 and render.counter < 2340:
            object_color = (random.uniform(0.1,0.3), 0, 0)

        elif render.counter > 2340 and render.counter < 2500:
            object_color = (random.uniform(0.1,0.3), 0, 0)
        
        elif render.counter > 2500 and render.counter < 2632:
            object_color = (random.uniform(0.1,0.3), 0, 0)

        elif render.counter > 2632 and render.counter < 2934:
            object_color = (random.uniform(0.4,0.6), 0, 0)

        elif render.counter > 2934 and render.counter < 3216:
            object_color = (random.uniform(0.4,0.6), random.uniform(0.4,0.6), random.uniform(0.4,0.6))

        elif render.counter > 3216 and render.counter < 3508:
            object_color = (random.uniform(0.6,0.8), random.uniform(0.2,0.3), 0)

        elif render.counter > 3508 and render.counter < 3800:
            object_color = (random.uniform(0.8, 1), random.uniform(0.2, 0.4), 0)

        elif render.counter > 3800 and render.counter < 4092:
            object_color = (1, random.uniform(0.4,0.8), random.uniform(0.8, 1))

        A, B, C = kwargs["vertices"]
        w, u, v, = kwargs["barycentrics"]
        tA, tB, tC = kwargs["t_vertices"]
        nA, nB, nC = kwargs["normals"]

        L = V3(0, 0, 1)

        iA = L.normalize() @ nA.normalize()
        iB = L.normalize() @ nB.normalize()
        iC = L.normalize() @ nC.normalize()

        i = iA * w + iB * v + iC * u

        if i < 0:
            i = abs(i)

        elif i > 1:
            i = 1
        
        #self.vertex_color = color.color_RGB_to_GBR(255 * i, 255 * i, 255 * i)

        if render.texture:
                                
            tX = tA.x * w + tB.x * v + tC.x * u
            tY = tA.y * w + tB.y * v + tC.y * u
            
            return render.texture.get_intensity(tX, tY, i)
        
        return color.color_RGB_to_GBR(
            object_color[0] * i,
            object_color[1] * i,
            object_color[2] * i
        )

    # Metodo dedicado a escribir la informacion que especificamos
    # a lo largo de la creacion de la imagen
    def write(self, filename):
        file = open(filename, 'bw')

        """ Pixel Header -> debe ocupar 14 bytes """
        # Escribir b y m
        file.write(wu.char('B'))
        file.write(wu.char('M'))
        # tamaño del archivo
        file.write(wu.dword(14 + 40 + self.width * self.height * 3))
        # unknown
        file.write(wu.word(0))
        file.write(wu.word(0))
        # puntero del inicio
        file.write(wu.dword(14 + 40))

        """ info header -> 40 pixeles """
        file.write(wu.dword(40))
        file.write(wu.dword(self.width))
        file.write(wu.dword(self.height))
        file.write(wu.word(1))
        # RGB
        file.write(wu.word(24))
        file.write(wu.dword(0))
        file.write(wu.dword(self.width * self.height * 3))
        file.write(wu.dword(0))
        file.write(wu.dword(0))
        file.write(wu.dword(0))
        file.write(wu.dword(0))

        """ Pixel data -> la imagen en si """
        for y in range(self.height):
            for x in range(self.width):
                file.write(self.framebuffer[y][x])
        
        file.close()