/**********************************************************************

  OpenGL-Introduction

  June, 7th, 2000

  This tutorial was written by Philipp Crocoll
  Contact: 
	philipp.crocoll@web.de
	www.codecolony.de

  Every comment would be appreciated.

  If you want to use parts of any code of mine:
	let me know and
	use it!

***********************************************************************/

// Helping library to make the bridge between the OS and OpenGL API
#include "glut.h"
#include <stdio.h>
#include <stdbool.h>

// Test C
int a, b, c = 0;


int integer1 = 5;
typedef int new_int;
new_int integer2 = 5;

typedef int (*ptr_fun) (int, int);

int add(int a, int b)
{
	return a+b;
}

ptr_fun ptr_instance1 = &add;
ptr_fun ptr_instance2 = add;

typedef struct _Pair
{
	int x;
	int y;
} Pair;

Pair pair1;

//

typedef struct _Color 
{
	float red;
	float blue;
	float green;
	float alpha;
} Color;

Color getColor(int red, int blue, int green, int alpha)
{
	Color c;
	c.red = red / 255;
	c.blue = blue / 255;
	c.green = green / 255;
	c.alpha = alpha / 255;
	return c;
}

void setColor(Color c)
{
	glColor3f(c.red, c.green, c.blue);
}

// Syntax of OpenGL API objects:
// GLtype
// GL_CONSTANT  GLUT_CONSTANT
// glFunc       glutFunc
// glVertex+NumberOfDim+Type : glVertex3f

// func
void graph(int x, int y)
{
	// Set Projection
	glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glViewport(0, 0, x, y); // Gosu put it here...
	glOrtho(0, x, y, 0, -1, 1);
	// Set ModelView
 	glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glEnable(GL_BLEND);
}

// 15h46 : un truc s'affiche !!!! 15h49 : ça marche !

// 15h51
void rect(int x, int y, int w, int h, Color c)
{
	glBegin(GL_POLYGON);
	  setColor(c);
	  //glColor3f(1.0, 0.0, 0.0);
	  glVertex3i(x, y, 0);
	  glVertex3i(x+w, y, 0);
	  glVertex3i(x+w, y+h, 0);
	  glVertex3i(x, y+h, 0);
	glEnd();
}

void line(int x1, int y1, int x2, int y2, Color c)
{
	glBegin(GL_LINES);
	  setColor(c);
	  glVertex3i(x1, y1, 0);
	  glVertex3i(x2, y2, 0);
	glEnd();
}

// Display func
// cannot render concave polygons
void Display(void)
{
	printf("display\n");
	glClear(GL_COLOR_BUFFER_BIT);
	glLoadIdentity(); // Erase current matrix
	glBegin(GL_POLYGON);//(GL_POLYGON); // Start Drawing
		glColor3f(0.0,1.0,0.0); // Vert
	    glVertex3f(50.0,50.0,0.0);
		//glVertex3f(-0.5,-0.5,-3.0); // x, y, z
		glColor3f(1.0,0.0,0.0); // Rouge
		glVertex3f(50.0,25.0,0.0);
	    //glVertex3f(0.5,-0.5,-3.0);
		glColor3f(0.0,0.0,1.0); // Bleu
		glVertex3f(25.0,25.0,0.0);
		//glVertex3f(0.5,0.5,-3.0);
		glVertex3f(25.0, 50.0, 0.0);
	glEnd();

	Color red = getColor(255, 0, 0, 0);
	rect(100, 100, 50, 50, red);
	Color green = getColor(0, 0, 255, 0);
	line(150, 150, 200, 200, green);

	glFlush();			//Finish rendering
}

// Reshape func
void Reshape(int x, int y)
{
	if (y == 0 || x == 0) return;  //Nothing is visible then, so return

	// Me
	printf("Reshape\n");
	graph(x, y);
}

// Main func
int main (int argc, char **argv)
{
	printf("%d\n", (*ptr_instance1)(5,5));
	printf("%d\n", ptr_instance2(5,5));

	int i1 = 22;
	int i2 = 34;
	printf("%p\n", &i1);
	printf("%p\n", &i2);
	printf("%d\n", sizeof(int));
	// 8 9 a  b  c  d
	// 8 9 10 11 12 13
	// C'est ca !!! Ils sont l'un sur l'autre.
	printf("%d\n", sizeof(bool));

	//-------------------------------------------
	int x = 300;
	int y = 300;

	//Initialize GLUT
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize(300,300);
	
	//Create a window with rendering context and everything else we need
	glutCreateWindow("Intro");
	glClearColor(0.0,0.0,0.0,0.0); // Color of Clear : R G B Alpha from 0.0 to 1.0
	
	// Me
	glViewport(0, 0, x, y);
	GLint coords[4] = {0 , 0, 0, 0};
	glGetIntegerv(GL_VIEWPORT, coords);
	printf("%d %d %d %d\n", coords[0], coords[1], coords[2], coords[3]);
	printf("%d %d %d\n", sizeof(GLint), sizeof(GLsizei), sizeof(GLfloat)); // same size (4)

	graph(x, y);

	//Assign the two used Msg-routines
	glutDisplayFunc(Display);
	glutReshapeFunc(Reshape);
	
	//Let GLUT get the msgs
	glutMainLoop();
	return 0;
}
