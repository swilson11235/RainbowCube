'''Stores and changes the camera position'''
__author__ = "Stephen"
__date__ = "11 November 2011"
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class Camera:
    '''Stores and changes the camera position
    while detecting collision'''

    SPEED = 0
    WALK = .3
    SPRINT = 1
    ROTATE = 2
    WIDTH = .8

    def __init__(self, x=0, y=0, z=0):
        '''Initializes everything, including sound'''
        self.pos_X = x
        self.pos_Y = y
        self.pos_Z = z
        self.start_pos=(x,y,z)
        self.rot_X = 0
        self.rot_Y = 0
        self.rot_Z = 0
        self.mouse_x = 0
        self.mouse_y = 0

        self.keys = {}
        self.keys["w"] = False
        self.keys["a"] = False
        self.keys["s"] = False
        self.keys["d"] = False
        self.keys["shift"] = False
        
    def renderCamera(self):
        '''Translates and rotates the camera to the correct position'''
        glRotatef(-self.rot_X , 1.0, 0.0, 0.0)
        glRotatef(-self.rot_Y , 0.0, 1.0, 0.0)
        glRotatef(-self.rot_Z , 0.0, 0.0, 1.0)
        glTranslatef(-self.pos_X, -self.pos_Y, -self.pos_Z)

    def move(self):
        '''Controls the movement of the camera.'''
        tmp_keys = self.keys.copy()

        #Check for sprint
        if tmp_keys["shift"] == True:
            self.SPEED = self.SPRINT
        else:
            self.SPEED = self.WALK

        moved = self.move_by_keys(tmp_keys, 1)
        if moved[0]:
            self.pos_X = moved[1]
            self.pos_Y = moved[2]
            self.pos_Z = moved[3]

    def rotate(self, x, y, z):
        '''Rotates by x, y, and z'''
        self.rot_X += x
        self.rot_Y += y
        self.rot_Z += z

    def strafe(self, amt):
        '''Strafes left or right, bassed on the angle'''
        tmp_Z = math.cos(self.rot_X*math.pi/180)*math.sin(-self.rot_Y*math.pi/180)*amt
        tmp_X = math.cos(self.rot_X*math.pi/180)*math.cos(self.rot_Y*math.pi/180)*amt
        self.pos_Y += math.cos(self.rot_X*math.pi/180)*math.sin(-self.rot_Z*math.pi/180)*amt
        return (tmp_X, tmp_Z)

    def walk(self, amt):
        '''Walks forward and back based on the angle you're facing'''
        tmp_Z = math.cos(self.rot_X*math.pi/180)*math.cos(self.rot_Y*math.pi/180)*amt
        tmp_X = math.cos(self.rot_X*math.pi/180)*math.sin(self.rot_Y*math.pi/180)*amt
        #Use to allow for change in height based on angle
        self.pos_Y += math.cos(self.rot_Z*math.pi/180)*math.sin(-self.rot_X*math.pi/180)*amt
        return (tmp_X, tmp_Z)

    def height(self, amt):
        '''Goes up or down. Always along the y axis'''
        self.pos_Y += amt

    def get_sides(self, side):
        '''Returns points of given side of bounding box'''
        tmp_X = 0
        tmp_Z = 0
        
        if side == 1:
            tmp_Z = math.cos(self.rot_X*math.pi/180)*math.cos(self.rot_Y*math.pi/180)*(-self.WIDTH/2)
            tmp_X = math.cos(self.rot_X*math.pi/180)*math.sin(self.rot_Y*math.pi/180)*(-self.WIDTH/2)
        if side == 2:
            tmp_Z = math.cos(self.rot_X*math.pi/180)*math.sin(-self.rot_Y*math.pi/180)*(self.WIDTH/2)
            tmp_X = math.cos(self.rot_X*math.pi/180)*math.cos(self.rot_Y*math.pi/180)*(self.WIDTH/2)
        if side == 3:
            tmp_Z = math.cos(self.rot_X*math.pi/180)*math.cos(self.rot_Y*math.pi/180)*(-self.WIDTH/2)
            tmp_X = math.cos(self.rot_X*math.pi/180)*math.sin(self.rot_Y*math.pi/180)*(-self.WIDTH/2)
        if side == 4:
            tmp_Z = math.cos(self.rot_X*math.pi/180)*math.sin(-self.rot_Y*math.pi/180)*(self.WIDTH/2)
            tmp_X = math.cos(self.rot_X*math.pi/180)*math.cos(self.rot_Y*math.pi/180)*(self.WIDTH/2)

        #Use to allow for change in height based on angle
        self.pos_Y += math.cos(self.rot_X*math.pi/180)*math.sin(-self.rot_Z*math.pi/180)*amt
        return (tmp_X, tmp_Z)

    def move_by_keys(self, tmp_keys, direction):
        '''returns the projected coordinates of the player,
        and takes a direction -- 1 = forward, 2 = reverse,
        also returns true upon movement'''
        tmp_X = self.pos_X
        tmp_Y = self.pos_Y
        tmp_Z = self.pos_Z
        moved = False
        if tmp_keys['a']:
            x, z = self.strafe(-self.SPEED*direction)
            tmp_Z += z
            tmp_X += x
            moved = True
        if tmp_keys['d']:
            x, z = self.strafe(self.SPEED*direction)
            tmp_Z += z
            tmp_X += x
            moved = True
        if tmp_keys['w']:
            x, z = self.walk(-self.SPEED*direction)
            tmp_Z += z
            tmp_X += x
            moved = True
        if tmp_keys['s']:
            x, z = self.walk(self.SPEED*direction)
            tmp_Z += z
            tmp_X += x
            moved = True
        return (moved, tmp_X, tmp_Y, tmp_Z)
    
    '''def project_move_other(self):
        tmp_X = self.pos_X
        tmp_Y = self.pos_Y
        tmp_Z = self.pos_Z
        x, z = self.walk(self.SPEED)
        tmp_Z += z
        tmp_X += x
        return (tmp_X, tmp_Z)'''

    def get_camera_distance(self, x2, y2, z2):
        '''Returns the distance from given point'''
        tmp_x = (self.pos_X - x2)**2
        tmp_y = (self.pos_Y - y2)**2
        tmp_z = (self.pos_Z - z2)**2
        return math.sqrt(tmp_x+tmp_y+tmp_z)