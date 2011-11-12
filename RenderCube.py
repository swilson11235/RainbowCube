'''Contains a class that renders the cube.'''

__author__ = "Stephen"
__date__ = "11 November 2011"

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Camera import Camera
import math

class RenderCube:
    '''This is the class that renders a rainbow cube
    Camera angles are handled by Camera.py.
    '''
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    MAP_SIZE =100

    def __init__(self):
        '''Sets up camera, modes, lighting, sounds, and objects.'''
        self.set_up_graphics()
        self.makeLights()
        self.camera = Camera(0,0,-5)

        glClearColor(.529,.8078,.980,0)

        glutIdleFunc(self.display)
        glutDisplayFunc(self.display)

        glutIgnoreKeyRepeat(GLUT_KEY_REPEAT_OFF)
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyUp)

        glutSetCursor(GLUT_CURSOR_NONE)
        glutPassiveMotionFunc(self.mouseMove)

        glutMainLoop()

    def set_up_graphics(self):
        '''Sets up OpenGL to provide double buffering, RGB coloring,
        depth testing, the correct window size, and a title.'''
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow('RainbowCube!')

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45,1,.15,100)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)

    def makeLights(self):
        '''Sets up the light sources and their positions. We have an
        ambient light and two sets of specular/diffuse lights.'''
        self.diffuse_pos1 = (50,5,0,1)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (.5, .5, .5, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

        glLightfv(GL_LIGHT1, GL_AMBIENT, (.2, .2, .2, 1))
        glLightfv(GL_LIGHT1, GL_POSITION, (0, 0, 1, 0))

        glLightfv(GL_LIGHT2, GL_SPECULAR, (.8, .8, .8, 1))
        glLightfv(GL_LIGHT2, GL_POSITION, self.diffuse_pos1)

        self.diffuse_pos2 = (0,1,0,1)
        glLightfv(GL_LIGHT3, GL_DIFFUSE, (.5, .5, .5, 1))
        glLightfv(GL_LIGHT3, GL_POSITION, self.diffuse_pos2)
        glLightfv(GL_LIGHT4, GL_SPECULAR, (.8, .8, .8, 1))
        glLightfv(GL_LIGHT4, GL_POSITION, self.diffuse_pos2)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)

    def display(self, x=0, y=0):
        '''Called for every refresh; redraws the cube at current position
        based on the camera angle.'''
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.camera.move()
        self.camera.renderCamera()
        self.renderLightSource()
        glPushMatrix()
        # Set the object shininess, ambient, diffuse, and
        # specular reflections.
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 75)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [.4, .4, .4, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [.9, .9, .9, .8])

        glTranslate(0,0,0)
        self.MakeCube()
        glPopMatrix()
        glutSwapBuffers()

    def mouseMove(self, x, y):
        '''Called when the mouse is moved.'''
        factor = 2
        
        tmp_x = (self.camera.mouse_x - x)/factor
        tmp_y = (self.camera.mouse_y - y)/factor
        if tmp_x > self.camera.ROTATE:
            tmp_x = self.camera.ROTATE
        self.camera.rotate(0, tmp_x, 0)
        x = self.WINDOW_WIDTH/2
        y = self.WINDOW_HEIGHT/2
        glutWarpPointer(x, y)
        self.camera.mouse_x = x
        self.camera.mouse_y = y
        
    def keyPressed(self, key, x, y):
        '''Called when a key is pressed.'''
        if key.lower() in self.camera.keys:
            self.camera.keys[key.lower()] = True
        if glutGetModifiers() == GLUT_ACTIVE_SHIFT:
            self.camera.keys["shift"] = True
        if key == 'j':
            self.camera.rotate(0,3,0)
        elif key == 'l':
            self.camera.rotate(0,-3,0)
        elif key == 'i':
            self.camera.rotate(3,0,0)
        elif key == 'k':
            self.camera.rotate(-3,0,0)
        elif key == ' ':
            self.camera.height(.1)
        elif key == 'c':
            self.camera.height(-.1)
        elif key == 'x':
            exit(0)

    def keyUp(self, key, x, y):
        '''Called when a key is released.'''
        self.camera.keys[key.lower()] = False
        if not glutGetModifiers() == GLUT_ACTIVE_SHIFT:
            self.camera.keys["shift"] = False

    def renderLightSource(self):
        '''Resets the light sources to the right position.'''
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)
        glLightfv(GL_LIGHT2, GL_POSITION, self.diffuse_pos2)
        glLightfv(GL_LIGHT3, GL_POSITION, self.diffuse_pos2)
        glLightfv(GL_LIGHT4, GL_POSITION, self.diffuse_pos2)

    def MakeCube(self):
        '''Makes the desired cube.'''
        glutSolidCube(2)
        # verts = [0,0,0,1,0,0,0,1,0,0,0,1]
        # color = [0,0,1,0,1,0,1,0,0,1,1,1]
        # ind = [0,1,2,3]
        # glVertexPointer(3, GL_FLOAT, 0,verts)
        # glColorPointer(3, GL_FLOAT, 0, color)
        # glBegin(GL_QUADS)
        # glArrayElement(0)
        # glArrayElement(1)
        # glArrayElement(2)
        # glArrayElement(3)
        # glEnd()
        # glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ind)
        # glDrawArrays(GL_QUADS, 0, 4)

    def get_visible(self, lst):
        '''Only draws the points sitting in front of the camera.
        Everything behind it is left undrawn.'''
        #works off a cube class that has all the points in it with methods to call information about dist, 
        to_use = []
        for point in lst:
            c = point.dist
            x,z = self.camera.project_move_other()
            b = self.camera.get_camera_distance(x, 0, z)
            a = point.get_dist(x, 0, z)
            angle = 0
            try:
                num = ((b**2)+(c**2)-(a**2))/(2*b*c)
                angle = math.acos(num)/math.pi*180
            except:
                pass
            if angle > 90:
                to_use.append(item)
        return to_use


if __name__=="__main__":
    cube = RenderCube()
