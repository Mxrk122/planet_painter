from mathstuff import cross_p
from vector3 import *
import MarkMatrix
import math

class Obj(object):
    def __init__(self, filename) -> None:
        #with abre una variable o un archivo y cuando termina lo cierra
        with open(filename) as f:
            self.lines = f.read().splitlines()
        
        self.vertex = []
        self.texture_vertex = []
        self.faces = []
        self.normal_vertex = []
        self.modelMatrix = None

        for line in self.lines:
            # Ignorar espacios en blanco
            if len(line) <= 1:
                continue
            # REcordar convertir strings a ints
            else:
                tp, value = line.split(' ', 1)

            if tp == 'v':

                self.vertex.append(
                    list(
                        map(
                            float, value.strip().split(' ')
                        )
                    )
                )
                """v = value.strip().split(' ')
                for i in range(len(v)):
                    v[i] = (float(v[i]))
                
                self.vertex.append(v)"""
            
            if tp == "vt":
                """vt = value.strip().split(' ')
                print("texture vertex: ", vt)
                for i in range(len(vt)):
                    vt[i] = int(float(v[i]))"""

                self.texture_vertex.append(
                    list(
                        map(float, value.split(' '))
                    )
                )

            if tp == 'f':
                self.faces.append(
                    [
                        list(
                            map(int, face.strip().split('/'))
                        )
                        for face in value.strip().split(' ')
                    ]
                )
                """faces = []
                #separar los valores
                va = value.strip().split(' ')
                for i in range(len(va)):
                    #array de faces para guardar la linea del archivo spliteada
                    face_splitted = va[i].split('/')

                    for f in range(len(face_splitted)):
                        face_splitted[f] = int(face_splitted[f])
                    
                    faces.append(face_splitted)
                    
                self.faces.append(faces)"""

            if tp == 'vn':

                self.normal_vertex.append(
                    list(
                        map(
                            float, value.strip().split(' ')
                        )
                    )
                )

    # Funcion para manipular la model matrix
    def loadModelMatrix(self, scale=(1, 1, 1), translate=(0, 0, 0), rotate=(0, 0, 0)):
        scale = V3(*scale)
        translate = V3(*translate)
        rotate = V3(*rotate)

        translation_matrix = MarkMatrix.Matrix([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
        ])

        scalation_matrix = MarkMatrix.Matrix([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        angle_x = rotate.x
        angle_y = rotate.y
        angle_z = rotate.z

        rotation_x = MarkMatrix.Matrix([
            [1, 0, 0, 0],
            [0, math.cos(angle_x), -math.sin(angle_x), 0],
            [0, math.sin(angle_x), math.cos(angle_x), 0],
            [0, 0, 0, 1]
        ])

        rotation_y = MarkMatrix.Matrix([
            [math.cos(angle_y), 0, math.sin(angle_y), 0],
            [0, 1, 0, 0],
            [-math.sin(angle_y), 0, math.cos(angle_y), 0],
            [0, 0, 0, 1]
        ])

        rotation_z = MarkMatrix.Matrix([
            [math.cos(angle_z), -math.sin(angle_z), 0, 0],
            [math.sin(angle_z), math.cos(angle_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        rotation_matrix = rotation_x * rotation_y * rotation_z
        
        self.modelMatrix = translation_matrix * rotation_matrix * scalation_matrix
    
    def transform_vertex(self, vertex, Viewport: MarkMatrix, projection: MarkMatrix, viewMatrix: MarkMatrix):
        augmented_vertex = MarkMatrix.Matrix([
            [vertex[0]],
            [vertex[1]],
            [vertex[2]],
            [1]
        ])

        transformed_vertex =  Viewport * projection * self.modelMatrix * viewMatrix * augmented_vertex


        return V3(
            transformed_vertex.get_matrix()[0][0] / transformed_vertex.get_matrix()[3][0],
            transformed_vertex.get_matrix()[1][0] / transformed_vertex.get_matrix()[3][0],
            transformed_vertex.get_matrix()[2][0] / transformed_vertex.get_matrix()[3][0]
        )
