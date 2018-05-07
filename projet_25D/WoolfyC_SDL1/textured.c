//=============================================================================
// Simple Wolfenstein-like 2.5D grid based engine
//-----------------------------------------------------------------------------
//
// Code source modified from original Lode Vandevenne's Computer Graphics Tutorial
// http://lodev.org/cgtutor/
//
// Base code source license :
// Copyright (c) 2004-2007, Lode Vandevenne
// 
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
//
//    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
//    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//-----------------------------------------------------------------------------
//
// Modifications contributed by Damien Gouteux in 2018, are:
//
//    * Removal of QuickGraph dependency using direct access to SDL 1 now through minisdl.h
//
//=============================================================================

#ifdef TEXTURED

//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <math.h>
#include <io.h>
#include "SDL.h"
#include "minisdl.h"

//-----------------------------------------------------------------------------
// Syntax sugar
//-----------------------------------------------------------------------------

#ifndef NOT_KEYWORD
#define NOT_KEYWORD
#define not !
#endif

//-----------------------------------------------------------------------------
// Constants
//-----------------------------------------------------------------------------

// OPTIONS
// #define FOG
#define MAX_FOG 25 // 12 15 20 25
// #define DEBUG 
#define SHODAN
// #define ENABLE_FLOOR
// #undef ENABLE_FLOOR

#ifdef SHODAN
  #define TEXTURE_PATH "..\\..\\assets\\graphic\\textures\\woolfy_wall\\noni_a_006.bmp"
  #define ENEMY_PATH "..\\..\\assets\\graphic\\sprites\\woolfy\\mguard_s_1.bmp"
  #define SOUND_PATH "..\\..\\assets\\audio\\sounds\\blip.wav"
#endif

#ifndef SHODAN
  //#define TEXTURE_PATH "perso_basic_tex.bmp"
  #define TEXTURE_PATH "noni_a_006.bmp"
  #define ENEMY_PATH "mguard_s_1.bmp"
  #define SOUND_PATH "blip.wav"
#endif

#define MAP_WIDTH 20
#define MAP_HEIGHT 20

#define MOVE_SPEED 0.004 // 0.002 0.2
#define ROT_SPEED 0.001 // 0.01;
#define UP_DOWN_SPEED 4 // 1 2

#define MINIMAP_FACTOR 20
#define MINIMAP_ZOOM 10

int WALL_HEIGHT = 3; //1 //2 //5

#define TEX_WIDTH 64 //32
#define TEX_HEIGHT 64 //32

#define R 1
#define Y 2
#define B 3
#define G 4
#define W 5
#define P 6

//-----------------------------------------------------------------------------
// Globals
//-----------------------------------------------------------------------------

bool down;
bool up;
bool right;
bool left;
bool done = false;
bool show_map = false;
bool debug = false;
FILE * debug_file;
bool write_debug = false;
bool z_down = false;
bool z_up = false;

int map[MAP_WIDTH][MAP_HEIGHT] = {
    {R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, -1, -2, 0, 0, 0, 0, R, 0, Y, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, -1, 0, G, 0, B, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, B, 0, P, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
};

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

void input(void) {
    if (SDL_PollEvent(&event)) {
        if (event.type == SDL_KEYDOWN) {
            switch (event.key.keysym.sym) {
                case SDLK_UP:
                    up = true;
                    break;
                case SDLK_DOWN:
                    down = true;
                    break;
                case SDLK_LEFT:
                    left = true;
                    break;
                case SDLK_RIGHT:
                    right = true;
                    break;
                case SDLK_ESCAPE:
                    done = true;
                    break;
                case SDLK_h:
                    z_down = true;
                    break;
                case SDLK_g:
                    z_up = true;
                    break;
            }
       } else if (event.type == SDL_KEYUP) {
            switch (event.key.keysym.sym) {
                case SDLK_UP:
                    up = false;
                    break;
                case SDLK_DOWN:
                    down = false;
                    break;
                case SDLK_LEFT:
                    left = false;
                    break;
                case SDLK_RIGHT:
                    right = false;
                    break;
                case SDLK_TAB:
                    show_map = not show_map;
                    break;
                case SDLK_SPACE:
                    debug = true;
                    debug_file = fopen("out.txt", "w");
                    break;
                case SDLK_PAGEUP:
                    WALL_HEIGHT += 1;
                    break;
                case SDLK_PAGEDOWN:
                    if (WALL_HEIGHT > 1) {
                        WALL_HEIGHT -= 1;
                    }
                    break;
                case SDLK_h:
                    z_down = false;
                    break;
                case SDLK_g:
                    z_up = false;
                    break;
            }
       } else if (event.type == SDL_QUIT ) {
            done = true;
       }
    }
}

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480
#define MID_SCREEN_HEIGHT 240

// Collision with a wall which is :
#define VERTICAL 0
#define HORIZONTAL 1
// used in side variable

Uint32 screen_buffer[SCREEN_HEIGHT][SCREEN_WIDTH];

// Il faut un buffer et ne pas ecrire directement sur le screen !
int main(int argc, char * argv[]) {
    // Player 2.5D Coordinates
    double player_x = 5.5;
    double player_y = 5.5;
    double player_z = 0.0;
    double direction_x = -1;
    double direction_y = 0;
    double camera_x = 0;
    double camera_y = 0.66;
    
    // Init and screen
    int err = init("Woolfy 2.5 TEXTURED", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }

    // Info
    display_info_on_surface(screen);

    // Colors
    Uint32 RED = SDL_MapRGB(screen->format, 255, 0, 0);
    Uint32 GREEN = SDL_MapRGB(screen->format, 0, 255, 0);
    Uint32 BLUE = SDL_MapRGB(screen->format, 0, 0, 255);
    Uint32 BLACK = SDL_MapRGB(screen->format, 0, 0, 0);
    Uint32 YELLOW = SDL_MapRGB(screen->format, 255, 255, 0);
    Uint32 WHITE = SDL_MapRGB(screen->format, 255, 255, 255);
    Uint32 PURPLE = SDL_MapRGB(screen->format, 128, 64, 128);

    // Time
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;

    // Moves
    double move_modifier = MOVE_SPEED;
    double rot_modifier = ROT_SPEED;
    double next_x = 0.0;
    double next_y = 0.0;
    float hitbox = 0.3;
    
    // Normal BMP
    SDL_Surface * my_bitmap_conv = load_bmp(TEXTURE_PATH);
    SDL_Rect rect;
    rect.x = 500;
    rect.y = 0;
    rect.w = my_bitmap_conv->w;
    rect.h = my_bitmap_conv->h;
    
    Uint32 tex[TEX_WIDTH][TEX_HEIGHT];
    for (int x = 0; x < my_bitmap_conv->w; x++) {
        for (int y = 0; y < my_bitmap_conv->h; y++) {
            tex[x][y] = *((Uint32 *)((Uint8 *)my_bitmap_conv->pixels + y * my_bitmap_conv->pitch + x * my_bitmap_conv->format->BytesPerPixel));
        }
    }

    // With colorkey
    SDL_Surface * my_bitmap_key_conv = load_bmp(ENEMY_PATH);

    Uint32 key = SDL_MapRGB(screen->format, 152, 0, 136);
    SDL_SetColorKey(my_bitmap_key_conv, SDL_SRCCOLORKEY | SDL_RLEACCEL, key);

    SDL_Rect rect2;
    rect2.x = 500;
    rect2.y = 200;
    rect2.w = my_bitmap_key_conv->w;
    rect2.h = my_bitmap_key_conv->h;

    //---------------------------------------------------------------------
    // Sound test
    //---------------------------------------------------------------------
    char name[32];
    printf("Using audio driver: %s\n", SDL_AudioDriverName(name, 32));
    init_audio(22050, AUDIO_U8, 1, 4096);
    load_wav(SOUND_PATH);
    play_wav();
    
    //---------------------------------------------------------------------

    // test 1
    double intersections[SCREEN_WIDTH][2]; //t1
    for (int i=0; i < SCREEN_WIDTH; i++) { //t1
        intersections[i][0] = 0;           //t1
        intersections[i][1] = 0;           //t1
    }                                      //t1
    
    while(!done) {

        int player_map_x = (int) player_x;
        int player_map_y = (int) player_y;

        //---------------------------------------------------------------------
        // Rendering
        //---------------------------------------------------------------------
        fill(BLACK);
        
        for (int x = 0; x < screen->w; x++) {
            double raycast_cpt = 2 * x / (double) screen->w - 1; 
            // On va parcourir tout le projection plane en avançant d'une fraction du vecteur caméra
            // La fraction est donné par [x / screen->w]. On convertir double screen->w pour ne pas perdre en précision.
            // Les fractions iront de 0 à 1. Or le vecteur caméra est orienté et on va le parcourir deux fois mais de -1 à +1.
            // On passe de (0 à 1) à (0 à 2) puis on soustrait 1 donc de (-1 à 1).

            double ray_dir_x = direction_x + camera_x * raycast_cpt;
            double ray_dir_y = direction_y + camera_y * raycast_cpt;

            int ray_map_x = player_map_x;
            int ray_map_y = player_map_y;
            
            double ray_x = player_x;
            double ray_y = player_y;

            double sideDistX;
            double sideDistY;

            double deltaDistX = fabs(1 / ray_dir_x);
            double deltaDistY = fabs(1 / ray_dir_y);
            double perpWallDist;

            int stepX;
            int stepY;

            int hit = 0;
            int side;

            if (ray_dir_x < 0) {
                stepX = -1;
                sideDistX = (player_x - ray_map_x) * deltaDistX;
            } else {
                stepX = 1;
                sideDistX = (ray_map_x + 1.0 - player_x) * deltaDistX;
            }
            if (ray_dir_y < 0) {
                stepY = -1;
                sideDistY = (player_y - ray_map_y) * deltaDistY;
            } else {
                stepY = 1;
                sideDistY = (ray_map_y + 1.0 - player_y) * deltaDistY;
            }   
#ifdef DEBUG 
            int itercount = 0; //d
            printf("-- Start DDA --\n"); //d
#endif

            while (hit == 0) {
                
#ifdef DEBUG
                itercount += 1; //d
                printf("-- %d -- \n", itercount); //d
                printf("sideDistX = %f, sideDistY = %f\n", sideDistX, sideDistY); //d
                printf("deltaDistX = %f, deltaDistY = %f\n", deltaDistX, deltaDistY); //d
                printf("ray_dir_x = %f, ray_dir_y = %f\n", ray_dir_x, ray_dir_y); //d
                printf("ray_map_x = %d, ray_map_y = %d\n", ray_map_x, ray_map_y); //d
                printf("ray_x = %f, ray_y = %f\n", ray_x, ray_y); //d
                printf("\n\n"); //d
#endif
    
                if (sideDistX < sideDistY) {
                    sideDistX += deltaDistX;
                    ray_map_x += stepX;
                    ray_x += stepX * deltaDistX; //d
                    side = VERTICAL;
                } else {
                    sideDistY += deltaDistY;
                    ray_map_y += stepY;
                    ray_y += stepY * deltaDistY; //d
                    side = HORIZONTAL;
                }
                if (map[ray_map_x][ray_map_y] > 0) hit = 1;
            }
            
#ifdef DEBUG
            if (side == VERTICAL) {
                ray_x = ray_map_x - stepX;
                ray_y -= stepY * deltaDistY;
            } else {
                ray_y = ray_map_y - stepY;
                ray_x -= stepX * deltaDistX;
            }

            printf("-- End of DDA -- \n", itercount); //d
            printf("sideDistX = %f, sideDistY = %f\n", sideDistX, sideDistY); //d
            printf("deltaDistX = %f, deltaDistY = %f\n", deltaDistX, deltaDistY); //d
            printf("ray_dir_x = %f, ray_dir_y = %f\n", ray_dir_x, ray_dir_y); //d
            printf("ray_map_x = %d, ray_map_y = %d\n", ray_map_x, ray_map_y); //d
            printf("ray_x = %f, ray_y = %f\n", ray_x, ray_y); //d
            printf("\n\n"); //d            
#endif    

            // Si VERTICAL : perpWallDist =
            // (
            //     ray_map_x - player_x + (1 - stepX) / 2
            //  ) / ray_dir_x;
            // C'est une "projection sur un vecteur".
            // Il calcule la simple différence entre le X map de l'intersection et le X map du joueur (avec (1-stepX) / 2 qui sert à départager si on touche à gauche ou à droite).
            // Cela donne une ligne horizontale. PB : l'angle du joueur.
            // En divisant par RAY_DIR_X, on a LA DISTANCE PERPENDICULAIRE (PERPWALLDIST).
            // Si RAY_DIR_X = 1, le mur est VERTICAL, le joueur est pile en face de lui donc PERPWALLDIST = TRUE DIST.
            // Cette simplification ne marche que si les murs sont à 90 degrés horizontaux ou verticaux
            if (side == VERTICAL) {
                perpWallDist = (ray_map_x - player_x + (1 - stepX) / 2) / ray_dir_x;
            } else {
                perpWallDist = (ray_map_y - player_y + (1 - stepY) / 2) / ray_dir_y;
            }
            
#ifdef DEBUG
            double xwalldist = sqrt(pow(ray_x - player_x , 2) + pow(ray_y - player_y, 2)); //d
            //perpWallDist = xwalldist; //d

            printf("xwalldist = %f, perpWallDist = %f\n", xwalldist, perpWallDist); //d
            exit(0); //d
#endif
#ifdef FOG
            double fog_factor = 0.0;
            if (perpWallDist < MAX_FOG) {
                fog_factor = 1 - perpWallDist / MAX_FOG;
            }
#endif
            int lineHeight = (int) ((screen->h / perpWallDist) * WALL_HEIGHT);
            double trueLineHeight = screen->h / perpWallDist;
            int midLineHeight = lineHeight / 2;

            int drawStart = MID_SCREEN_HEIGHT - midLineHeight + player_z;
            int drawEnd = MID_SCREEN_HEIGHT + midLineHeight + player_z;
            int trueDrawStart = drawStart; // + player_z; c'est ne pas changer ça qui fait regarder en haut et en bas. Hum...

            if (drawStart < 0) {
                drawStart = 0;
            }
            if (drawEnd >= screen->h) {
                drawEnd = screen->h - 1;
            }
            
            double wallX; //where exactly the wall was hit
            if (side == VERTICAL) {
                wallX = player_y + perpWallDist * ray_dir_y;
            } else {
                wallX = player_x + perpWallDist * ray_dir_x;
            }
            if (side == VERTICAL) {                                    //t1
                intersections[x][0] = ray_map_x + (1 - stepX) / 2;     //t1
                intersections[x][1] = wallX;                           //t1
            } else {                                                   //t1
                intersections[x][0] = wallX;                           //t1
                intersections[x][1] = ray_map_y + (1 - stepY) / 2;     //t1
            }                                                          //t1
            wallX -= floor((wallX));
            
            //x coordinate on the texture
            int texX = (int)(wallX * (double) TEX_WIDTH);
            if(side == VERTICAL && ray_dir_x > 0) texX = TEX_WIDTH - texX - 1; // (inverse)
            if(side == HORIZONTAL && ray_dir_y < 0) texX = TEX_WIDTH - texX - 1;
            
            for(int y = drawStart; y < drawEnd; y++)
            {
                int d = y - trueDrawStart;
                int texY = (int) (d * ( (double) TEX_HEIGHT / trueLineHeight)) % TEX_HEIGHT; //lineHeight); // Ajout de (double) pour éviter le flottement sur trueLineHeight

                //int d = (int) (y * 2 - screen-> h + lineHeight);
                //int texY = ((d * TEX_HEIGHT) / lineHeight) % TEX_HEIGHT; // ajout de % TEX_HEIGHT pour éviter bug de la dernière colonne;
                
                //make color darker for y-sides
                Uint32 color = tex[texX][texY];
                //if(side == 1) {
                //    color = (color >> 1) & 8355711;
                //}
                // DEBUG
                if (y == drawStart || y == drawEnd - 1) {
                    color = WHITE;
                }
                //if (x == 0) {
                //    color = PURPLE;
                //}
                // END DEBUG
#ifdef FOG
                Uint8 r;
                Uint8 g;
                Uint8 b;
                SDL_GetRGB(color, screen->format, &r, &g, &b);
                color = SDL_MapRGB(screen->format, r * fog_factor, g * fog_factor, b * fog_factor);
#endif
                screen_buffer[y][x] = color;
                if (debug) {
                    fprintf(debug_file, "x, %d, y, %d, d, %d, texX, %d, texY, %d, color, %d\n", x, y, d, texX, texY, color);
                }
            }

            #ifdef ENABLE_FLOOR
            //FLOOR CASTING
            double floorXWall, floorYWall; //x, y position of the floor texel at the bottom of the wall

            //4 different wall directions possible
            if(side == 0 && ray_dir_x > 0)
            {
                floorXWall = ray_map_x;
                floorYWall = ray_map_y + wallX;
            }
            else if(side == 0 && ray_dir_x < 0)
            {
                floorXWall = ray_map_x + 1.0;
                floorYWall = ray_map_y + wallX;
            }
            else if(side == 1 && ray_dir_y > 0)
            {
                floorXWall = ray_map_x + wallX;
                floorYWall = ray_map_y;
            }
            else
            {
                floorXWall = ray_map_x + wallX;
                floorYWall = ray_map_y + 1.0;
            }

            // 0. Base
            for(int count = 0;; count++)
            {
                int y = drawEnd + 1 + count;
                if (y >= screen->h) {
                    break;
                }
                double currentDist = screen->h / (2.0 * y - screen->h); //you could make a small lookup table for this instead

                double weight = currentDist / (perpWallDist / WALL_HEIGHT);

                double currentFloorX = weight * floorXWall + (1.0 - weight) * player_x;
                double currentFloorY = weight * floorYWall + (1.0 - weight) * player_y;

                int floorTexX, floorTexY;
                floorTexX = ((int)(currentFloorX * TEX_WIDTH)) % TEX_WIDTH;
                floorTexY = ((int)(currentFloorY * TEX_HEIGHT)) % TEX_HEIGHT;

                int val = map[(int)currentFloorX][(int)currentFloorY];
                Uint32 color = PURPLE;
                switch (val) {
                    case 0:
                        color = tex[floorTexX][floorTexY];
                        break;
                    case -1:
                        color = BLACK;
                        break;
                    case -2:
                        color = RED;
                        break;
                }
#ifdef FOG // DON'T WORK
                fog_factor = 0.0;
                if (currentDist * weight < MAX_FOG) {
                    fog_factor = 1 - currentDist * weight / MAX_FOG;
                }
                Uint8 r;
                Uint8 g;
                Uint8 b;
                SDL_GetRGB(color, screen->format, &r, &g, &b);
                color = SDL_MapRGB(screen->format, r * fog_factor, g * fog_factor, b * fog_factor);
#endif
                //darker floor
                //screen_buffer[y][x] = (color >> 1) & 8355711;
                screen_buffer[y][x] = color;
                // ceiling
                //int y_ceiling = MID_SCREEN_HEIGHT - midLineHeight - lineHeight - count -1;
                int y_ceiling = drawStart - count - 1;
                /*
                if (y_ceiling - lineHeight > 0) {
                    y_ceiling -= lineHeight;
                } else {
                    y_ceiling = 0;
                }
                */

                /*
                currentDist = screen->h / (2.0 * y_ceiling - screen->h); //you could make a small lookup table for this instead

                weight = currentDist / perpWallDist;

                currentFloorX = weight * floorXWall + (1.0 - weight) * player_x;
                currentFloorY = weight * floorYWall + (1.0 - weight) * player_y;

                floorTexX = ((int)(currentFloorX * TEX_WIDTH)) % TEX_WIDTH;
                floorTexY = ((int)(currentFloorY * TEX_HEIGHT)) % TEX_HEIGHT;

                val = map[(int)currentFloorX][(int)currentFloorY];
                color = PURPLE;
                switch (val) {
                    case 0:
                        color = tex[floorTexX][floorTexY];
                        break;
                    case -1:
                        color = BLACK;
                        break;
                    case -2:
                        color = RED;
                        break;
                }
                */
                if (y_ceiling > 0) {
                    screen_buffer[y_ceiling][x] = color;
                }
                
                /*
                if (debug) {
                    if (color == 16711680 && not write_debug) {
                        fprintf(debug_file, "x = %d, y_floor = %d, y_ceiling = %d, lineHeight = %d, count= %d, color = %d, currentFloorX = %f, currentFloorY = %f\n", x, y, y_ceiling, lineHeight, count, color, currentFloorX, currentFloorY);
                        write_debug = true;
                    }
                    if (color != 16711680 && write_debug) {
                        fprintf(debug_file, "x = %d, y_floor = %d, y_ceiling = %d, lineHeight = %d, count= %d, color = %d, currentFloorX = %f, currentFloorY = %f\n", x, y, y_ceiling, lineHeight, count, color, currentFloorX, currentFloorY);
                        write_debug = false;
                    }
                }
                */
            }

            /*
            // BASE : draw the floor from drawEnd to the bottom of the screen
            for(int y = drawEnd + 1; y < screen->h; y++)
            {
                currentDist = screen->h / (2.0 * y - screen->h); //you could make a small lookup table for this instead

                double weight = (currentDist - distPlayer) / (distWall - distPlayer); // no need of distPlayer, distWall is perpWallDist

                double currentFloorX = weight * floorXWall + (1.0 - weight) * player_x;
                double currentFloorY = weight * floorYWall + (1.0 - weight) * player_y;

                int floorTexX, floorTexY;
                floorTexX = ((int)(currentFloorX * TEX_WIDTH)) % TEX_WIDTH;
                floorTexY = ((int)(currentFloorY * TEX_HEIGHT)) % TEX_HEIGHT;

                //floor
                //1 buffer[y][x] = (texture[3][TEX_WIDTH * floorTexY + floorTexX] >> 1) & 8355711;
                //2 pixel(x, y, tex[floorTexX][floorTexY]);
                int val = map[(int)currentFloorX][(int)currentFloorY];
                Uint32 color = PURPLE;
                switch (val) {
                    case 0:
                        color = tex[floorTexX][floorTexY];
                        break;
                    case -1:
                        color = BLACK;
                        break;
                    case -2:
                        color = RED;
                        break;
                }
                screen_buffer[y][x] = color;
                int ceiling = drawStart - (y - drawEnd) - lineHeight;
                if (ceiling >= 0) {
                    screen_buffer[ceiling][x] = color;
                }

                //ceiling (symmetrical!)
                //1 buffer[h - y][x] = texture[6][TEX_WIDTH * floorTexY + floorTexX];
                //2 pixel(x, screen->h - y - (WALL_HEIGHT - 1) * lineHeight, tex[floorTexX][floorTexY]);
                */
                /*
                // Ceiling 1 bug
                if (map[(int)currentFloorX][(int)currentFloorY] == 0) {
                    //int yy = screen->h - y;
                    //int yy = screen->h - y - (WALL_HEIGHT - 1) * lineHeight;
                    //int yy = drawStart - (y - drawEnd); // OK
                    int yy = drawStart - (y - drawEnd) - (WALL_HEIGHT - 1) * lineHeight; // KO
                    if (yy >= 0)
                        screen_buffer[yy][x] = tex[floorTexX][floorTexY];
                    //else
                    //    screen_buffer[0][x] = 16777215;
                }
                */
                    
            /*}*/

            /*
            // Ceiling 2 (no bug but parallax + megatex + holes in tex)
            int highFactor = lineHeight * (WALL_HEIGHT - 1);
            int maxDrawStart = drawStart - highFactor;
            for(int y = maxDrawStart - 1; y >= 0; y--) {
                // This line provokes the problem
                currentDist = screen->h / (2.0 * y - screen->h); //you could make a small lookup table for this instead

                double weight = (currentDist - distPlayer) / (distWall - distPlayer);

                double currentFloorX = weight * floorXWall + (1.0 - weight) * player_x;
                double currentFloorY = weight * floorYWall + (1.0 - weight) * player_y;

                int floorTexX, floorTexY;
                floorTexX = ((int)(currentFloorX * TEX_WIDTH)) % TEX_WIDTH;
                floorTexY = ((int)(currentFloorY * TEX_HEIGHT)) % TEX_HEIGHT;
                
                int val = map[(int)currentFloorX][(int)currentFloorY];
                switch (val) {
                    case 0:
                        screen_buffer[y][x] = tex[floorTexX][floorTexY];
                        break;
                    case -1:
                        break;
                    case -2:
                        screen_buffer[y][x] = RED;
                }
            }
            */

            #endif
        }
        
        if (debug) {
            debug = false;
            fclose(debug_file);
            printf("End of dump\n");
        }

        buffer(screen_buffer);
        
        if (show_map) {
            int minimap_player_x = player_x * MINIMAP_FACTOR;
            int minimap_player_y = player_y * MINIMAP_FACTOR;
            int minimap_posdirx = minimap_player_x + direction_x * MINIMAP_ZOOM;
            int minimap_posdiry = minimap_player_y + direction_y * MINIMAP_ZOOM;
            int minimap_sideleft_x = minimap_player_x + camera_x * MINIMAP_ZOOM * hitbox;
            int minimap_sideleft_y = minimap_player_y + camera_y * MINIMAP_ZOOM * hitbox;
            int minimap_sideright_x = minimap_player_x - camera_x * MINIMAP_ZOOM * hitbox;
            int minimap_sideright_y = minimap_player_y - camera_y * MINIMAP_ZOOM * hitbox;

            line(minimap_player_x, minimap_player_y, minimap_posdirx, minimap_posdiry, BLUE);
            line(minimap_player_x, minimap_player_y, minimap_sideleft_x, minimap_sideleft_y, WHITE);
            line(minimap_player_x, minimap_player_y, minimap_sideright_x, minimap_sideright_y, WHITE);

            line(minimap_posdirx, minimap_posdiry, minimap_posdirx + camera_x * MINIMAP_ZOOM, minimap_posdiry + camera_y * MINIMAP_ZOOM, YELLOW);
            line(minimap_posdirx, minimap_posdiry, minimap_posdirx - camera_x * MINIMAP_ZOOM, minimap_posdiry - camera_y * MINIMAP_ZOOM, YELLOW);
            line(minimap_player_x, minimap_player_y, minimap_posdirx + camera_x * MINIMAP_ZOOM, minimap_posdiry + camera_y * MINIMAP_ZOOM, YELLOW);
            line(minimap_player_x, minimap_player_y, minimap_posdirx - camera_x * MINIMAP_ZOOM, minimap_posdiry - camera_y * MINIMAP_ZOOM, YELLOW);
            pixel(minimap_player_x, minimap_player_y, GREEN);
            circle(minimap_player_x, minimap_player_y, MINIMAP_ZOOM * 4, WHITE);

            for(int y = 0; y < MAP_HEIGHT; y++) {
                for(int x = 0; x < MAP_WIDTH; x++) {
                    if (map[x][y] > 0) {
                        rectangle(x * MINIMAP_FACTOR, y * MINIMAP_FACTOR, (x + 1) * MINIMAP_FACTOR, (y + 1) * MINIMAP_FACTOR, WHITE, false);
                    }
                }
            }
            // Player square
            rectangle(player_map_x * MINIMAP_FACTOR, player_map_y * MINIMAP_FACTOR, (player_map_x + 1) * MINIMAP_FACTOR, (player_map_y + 1) * MINIMAP_FACTOR, GREEN, false);

            SDL_BlitSurface(my_bitmap_conv, NULL, screen, &rect);
            //SDL_BlitSurface(my_bitmap_key_conv, NULL, screen, &rect2);
            for (int y = 0; y < my_bitmap_key_conv->w; y++) {
                for (int x = 0; x < my_bitmap_key_conv->h; x++) {
                    pixel(x + 500, y + 200, tex[x][y]);
                }
            }

            //deb t1
            for(int x=0; x < screen->w; x++) {
                line(minimap_player_x, minimap_player_y, intersections[x][0] * MINIMAP_FACTOR, intersections[x][1] * MINIMAP_FACTOR, PURPLE);
            }
            //end t1
        }
        render();

        //---------------------------------------------------------------------
        // Time and input
        //---------------------------------------------------------------------
        input();
        tick_previous = tick_current;
        tick_current = SDL_GetTicks();
        frame_time = (tick_current - tick_previous);

        //---------------------------------------------------------------------
        // Update
        //---------------------------------------------------------------------
        if (up || down) {
            if (up) {
                next_x = player_x + direction_x * move_modifier * frame_time;
                next_y = player_y + direction_y * move_modifier * frame_time;
            }
            if (down) {
                next_x = player_x - direction_x * move_modifier * frame_time;
                next_y = player_y - direction_y * move_modifier * frame_time;
            }
            if (map[(int)next_x][(int)next_y] <= 0 && 
                map[(int)(next_x - hitbox)][(int)(next_y - hitbox)] <= 0 && // up, left
                map[(int)(next_x + hitbox)][(int)(next_y + hitbox)] <= 0 && // down, right
                map[(int)(next_x - hitbox)][(int)(next_y + hitbox)] <= 0 && // down, left
                map[(int)(next_x + hitbox)][(int)(next_y - hitbox)] <= 0) { // up, right
                player_x = next_x;
                player_y = next_y;
            } else if (map[(int)next_x][(int)player_y] <= 0 &&  // gliding on x
                map[(int)(next_x - hitbox)][(int)(player_y - hitbox)] <= 0 && // up, left
                map[(int)(next_x + hitbox)][(int)(player_y + hitbox)] <= 0 && // down, right
                map[(int)(next_x - hitbox)][(int)(player_y + hitbox)] <= 0 && // down, left
                map[(int)(next_x + hitbox)][(int)(player_y - hitbox)] <= 0) { // up, right
                player_x = next_x;
            } else if (map[(int)player_x][(int)next_y] <= 0 &&  // gliding on y
                map[(int)(player_x - hitbox)][(int)(next_y - hitbox)] <= 0 && // up, left
                map[(int)(player_x + hitbox)][(int)(next_y + hitbox)] <= 0 && // down, right
                map[(int)(player_x - hitbox)][(int)(next_y + hitbox)] <= 0 && // down, left
                map[(int)(player_x + hitbox)][(int)(next_y - hitbox)] <= 0) { // up, right
                player_y = next_y; 
            }
        }
        if (left) {
            double old_dir_x = direction_x;
            direction_x = direction_x * cos(rot_modifier * frame_time) - direction_y * sin(rot_modifier * frame_time);
            direction_y = old_dir_x * sin(rot_modifier * frame_time) + direction_y * cos(rot_modifier * frame_time);
            double old_cam_x = camera_x;
            camera_x = camera_x * cos(rot_modifier * frame_time) - camera_y * sin(rot_modifier * frame_time);
            camera_y = old_cam_x * sin(rot_modifier * frame_time) + camera_y * cos(rot_modifier * frame_time);
        }
        if (right) {
            double old_dir_x = direction_x;
            direction_x = direction_x * cos(-rot_modifier * frame_time) - direction_y * sin(-rot_modifier * frame_time);
            direction_y = old_dir_x * sin(-rot_modifier * frame_time) + direction_y * cos(-rot_modifier * frame_time);
            double old_cam_x = camera_x;
            camera_x = camera_x * cos(-rot_modifier * frame_time) - camera_y * sin(-rot_modifier * frame_time);
            camera_y = old_cam_x * sin(-rot_modifier * frame_time) + camera_y * cos(-rot_modifier * frame_time);
        }
        if (z_down) {
            player_z -= UP_DOWN_SPEED;
            printf("%f\n", player_z);
        }
        if (z_up) {
            player_z += UP_DOWN_SPEED;
            printf("%f\n", player_z);
        }
    }

    //---------------------------------------------------------------------
    // Cleaning
    //---------------------------------------------------------------------
    SDL_FreeSurface(my_bitmap_conv);
    SDL_FreeSurface(my_bitmap_key_conv);
    stop_audio();
    SDL_Quit();
    return EXIT_SUCCESS;
}

#endif
