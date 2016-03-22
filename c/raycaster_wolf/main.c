#include "./SDL/include/SDL.h"
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#define TICK_INTERVAL    30

static Uint32 next_time;

Uint32 time_left(void)
{
    Uint32 now;

    now = SDL_GetTicks();
    if(next_time <= now)
        return 0;
    else
        return next_time - now;
}

int main(int argc, char *argv[]) {
    //int gogogo = 1;
    //SDL_Event event;

	//Screen dimension constants
	const int SCREEN_WIDTH = 640;
	const int SCREEN_HEIGHT = 480;
	//const int SCREEN_FPS = 60;
	//const int SCREEN_TICKS_PER_FRAME = 1000 / SCREEN_FPS;
	
	int area[24][24] = {
	  {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1},
	  {1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1},
	  {1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1},
	  {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1},
	  {1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
	  {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}
	};
	printf("Area 23,23 = %d\n", area[23][23]);
	
	float position[2] = {22.0,12.0};      // position vector (point)
	float direction[2] = {-1.0,0.0};      // direction vector
	float camera[2] = {0.0, 0.66};        // camera plane (orthogonal to direction vector) 2 * atan(0.66/1.0)=66
	
    //The window we'll be rendering to
    SDL_Window* window = NULL;
    SDL_Renderer * renderer;

    //The surface contained by the window
    //SDL_Surface* screenSurface = NULL;

    //Initialize SDL
    if( SDL_Init( SDL_INIT_VIDEO ) < 0 )
    {
        printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
    }
    else
    {
        //Create window
        //window = SDL_CreateWindow( "SDL Tutorial", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN );
		SDL_CreateWindowAndRenderer(SCREEN_WIDTH, SCREEN_HEIGHT, 0, &window, &renderer);
        if( window == NULL )
        {
            printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
        }
        else
        {
  			//Main loop flag
           	bool quit = false;

            //Event handler
            SDL_Event event;

    		float frameTime = 0.10;
    		float rotSpeed = frameTime * 3.0;
    		float moveSpeed = frameTime * 5.0;
    		
			bool right = false;
			bool left = false;
			bool up = false;
			bool down = false;
			
			float oldDirX = 0.0;
			float oldPlaneX = 0.0;

			next_time = SDL_GetTicks() + TICK_INTERVAL;

			//While application is running
            while( !quit )
            {
				//Handle events on queue
                while( SDL_PollEvent( &event ) != 0 )
                {
                    //User requests quit
                    if( event.type == SDL_QUIT )
                    {
                        quit = true;
                    } else if (event.type == SDL_KEYDOWN) {
            			if (event.key.keysym.sym == SDLK_RIGHT) {
                			right = true;
						} 
						if (event.key.keysym.sym == SDLK_LEFT) {
			               left = true;
						}
			            if (event.key.keysym.sym == SDLK_UP) {
                			up = true;
						}
            			if (event.key.keysym.sym == SDLK_DOWN) {
                			down = true;
						}
        			} else if (event.type == SDL_KEYUP) {
            			if (event.key.keysym.sym == SDLK_RIGHT) {
                			right = false;
						}
            			if (event.key.keysym.sym == SDLK_LEFT) {
                			left = false;
						}
            			if (event.key.keysym.sym == SDLK_UP) {
                			up = false;
						}
            			if (event.key.keysym.sym == SDLK_DOWN) {
                			down = false;
						}
					}
                }
				
			    // rotate to the right
			    if (right) {
			        // both camera direction and camera plane must be rotated
					printf("before direction : %f, %f\n", direction[0], direction[1]);
					printf("before camera : %f, %f\n", camera[0], camera[1]);
			        oldDirX = direction[0];
			        direction[0] = direction[0] * cos(-rotSpeed) - direction[1] * sin(-rotSpeed);
			        direction[1] = oldDirX * sin(-rotSpeed) + direction[1] * cos(-rotSpeed);
			        oldPlaneX = camera[0];
			        camera[0] = camera[0] * cos(-rotSpeed) - camera[1] * sin(-rotSpeed);
			        camera[1] = oldPlaneX * sin(-rotSpeed) + camera[1] * cos(-rotSpeed);
					printf("after direction : %f, %f\n", direction[0], direction[1]);
					printf("after camera : %f, %f\n", camera[0], camera[1]);
				}
			    if (left) {
			        // both camera direction and camera plane must be rotated
					printf("before direction : %f, %f\n", direction[0], direction[1]);
					printf("before camera : %f, %f\n", camera[0], camera[1]);
			        oldDirX = direction[0];
			        direction[0] = direction[0] * cos(rotSpeed) - direction[1] * sin(rotSpeed);
			        direction[1] = oldDirX * sin(rotSpeed) + direction[1] * cos(rotSpeed);
			        oldPlaneX = camera[0];
			        camera[0] = camera[0] * cos(rotSpeed) - camera[1] * sin(rotSpeed);
			        camera[1] = oldPlaneX * sin(rotSpeed) + camera[1] * cos(rotSpeed);
					printf("after direction : %f, %f\n", direction[0], direction[1]);
					printf("after camera : %f, %f\n", camera[0], camera[1]);
				}
			    if (up) {
					printf("before position : %f, %f\n", position[0], position[1]);
			        if (area[(int) (position[0] + direction[0] * moveSpeed)][(int) (position[1])] == 0) { position[0] += direction[0] * moveSpeed; }
			        if (area[(int) (position[0])][(int) (position[1] + direction[1] * moveSpeed)] == 0) { position[1] += direction[1] * moveSpeed; }
					printf("after position : %f, %f\n", position[0], position[1]);
				}
			    if (down) {
					printf("before position : %f, %f\n", position[0], position[1]);
			        if (area[(int) (position[0] - direction[0] * moveSpeed)][(int) (position[1])] == 0) { position[0] -= direction[0] * moveSpeed; }
			        if (area[(int) (position[0])][(int) (position[1] - direction[1] * moveSpeed)] == 0) { position[1] -= direction[1] * moveSpeed; }
					printf("after position : %f, %f\n", position[0], position[1]);
			    }
				
				// RENDER
				//-------------------------------------------------------------
				SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
				SDL_RenderClear(renderer);
				SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
				
				//Get window surface
            	//screenSurface = SDL_GetWindowSurface( window );

            	//Fill the surface white
            	//SDL_FillRect( screenSurface, NULL, SDL_MapRGB( screenSurface->format, 0x00, 0x00, 0x00 ) );
				
				for(int s = 0; s < SCREEN_WIDTH; s++) {
					
		   	    	// calculate ray position and direction 
		        	float cameraX = 2 * s / (float) SCREEN_WIDTH - 1; // x-coordinate in camera space
		        	float rayPosX = position[0];
		        	float rayPosY = position[1];
			        float rayDirX = direction[0] + camera[0] * cameraX;
		        	float rayDirY = direction[1] + camera[1] * cameraX;
		        
		        	// which box of the map we're in  
		        	int mapX = (int) rayPosX;
		        	int mapY = (int) rayPosY;
		        
		        	// length of ray from current position to next x or y-side
		        	float sideDistX = 0.0;
		        	float sideDistY = 0.0;
		        
		        	// Added by me. Is it still useful?
		        	if (rayDirX == 0) { rayDirX = 0.00001; }
		        	if (rayDirY == 0) { rayDirY = 0.00001; }
		        
		        	// Length of ray from one x or y-side to next x or y-side
		        	float deltaDistX = sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX));
		        	float deltaDistY = sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY));
		        	float perpWallDist = 0.0;
		       		
		        	// What direction to step in x or y-direction (either +1 or -1)
		        	int stepX = 0;
		        	int stepY = 0;
		        
		        	int hit = 0; // was there a wall hit?
		        	int side = 0; // was a NS or a EW wall hit?
		        
		        	// calculate step and initial sideDist
		        	if (rayDirX < 0) {
		            	stepX = -1;
		            	sideDistX = (rayPosX - mapX) * deltaDistX;
					} else {
		        		stepX = 1;
		            	sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX;
		        	}
					if (rayDirY < 0) {
		            	stepY = -1;
		            	sideDistY = (rayPosY - mapY) * deltaDistY;
					} else {
		            	stepY = 1;
		            	sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY;
					}
		        
		    	    // perform DDA
		        	while (hit == 0) {
		            	// jump to next map square, OR in x-direction, OR in y-direction
		            	if (sideDistX < sideDistY) {
		                	sideDistX += deltaDistX;
		                	mapX += stepX;
		                	side = 0;
						} else {
		            	    sideDistY += deltaDistY;
		                	mapY += stepY;
		                	side = 1;
						}
		     	       	// Check if ray has hit a wall
		            	if (area[mapX][mapY] > 0) {
							hit = 1;
						}
		        	}
		        	
					// Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
		       		if (side == 0) {
		  	         	perpWallDist = fabs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX); // fabs
					} else {
				        perpWallDist = fabs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY); // fabs
		       		}
		       		// Calculate height of line to draw on screen
		       		//int lineHeight = (int) fabs(((float) SCREEN_HEIGHT / (float) perpWallDist)); // float
		       		int lineHeight = (int) ( ((float) SCREEN_HEIGHT) / perpWallDist); // me marche pas
					
		       		// Calculate lowest and highest pixel to fill in current stripe
		       		int drawStart = -lineHeight / 2 + SCREEN_HEIGHT / 2;
		       		if (drawStart < 0) { drawStart = 0; }
		       		int drawEnd = lineHeight / 2 + SCREEN_HEIGHT / 2;
		       		if (drawEnd >= SCREEN_HEIGHT) { drawEnd = SCREEN_HEIGHT - 1; }
		        
		       		// choose wall color
		       		//color = ccolor(area[mapX][mapY])
            		
					SDL_RenderDrawLine(renderer, s, drawStart, s, drawEnd);
				}

				SDL_RenderPresent(renderer);
				
            	//Update the surface
            	SDL_UpdateWindowSurface( window );

				SDL_Delay(time_left());
   		     	next_time += TICK_INTERVAL;
			}
			
            //Wait two seconds
            //SDL_Delay( 2000 );
        }
    }
	SDL_DestroyRenderer(renderer);
    //Destroy window
    SDL_DestroyWindow( window );

    //Quit SDL subsystems
    SDL_Quit();

    return 0;
}
