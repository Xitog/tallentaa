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

#ifdef FLAT

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

// #define TEXTURE_PATH "..\\..\\assets\\graphic\\textures\\woolfy_wall\\noni_a_006.bmp"
// #define ENEMY_PATH "..\\..\\assets\\graphic\\sprites\\woolfy\\mguard_s_1.bmp"
#define SOUND_PATH "blip.wav"
#define TEXTURE_PATH "noni_a_006.bmp"
#define ENEMY_PATH "mguard_s_1.bmp"

#define MAP_WIDTH 20
#define MAP_HEIGHT 20

#define MOVE_SPEED 0.004 // 0.002 0.2
#define ROT_SPEED 0.001 // 0.01;

#define MINIMAP_FACTOR 20
#define MINIMAP_ZOOM 10

#define WALL_HEIGHT 2

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

int map[MAP_WIDTH][MAP_HEIGHT] = {
    {R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y, R, Y},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {G, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, R, 0, Y, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {W, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
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
            }
       } else if (event.type == SDL_QUIT ) {
            done = true;
       }
    }
}

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480
// Il faut un buffer et ne pas ecrire directement sur le screen !
int main(int argc, char * argv[]) {
    // Player 2.5D Coordinates
    double player_x = 5.5;
    double player_y = 5.5;
    double direction_x = -1;
    double direction_y = 0;
    double camera_x = 0;
    double camera_y = 0.66;
    
    // Init and screen
    int err = init("Woolfy 2.5 FLAT", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }
    Uint32 buffer[screen->h][screen->w];

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
    
    while(!done) {

        int player_map_x = (int) player_x;
        int player_map_y = (int) player_y;

        //---------------------------------------------------------------------
        // Rendering
        //---------------------------------------------------------------------
        fill(BLACK);
        
        for (int x = 0; x < screen->w; x++) {
            double raycast_cpt = 2 * x / (float) screen->w - 1;
            double ray_x = direction_x + camera_x * raycast_cpt;
            double ray_y = direction_y + camera_y * raycast_cpt;

            int ray_map_x = player_map_x;
            int ray_map_y = player_map_y;

            double sideDistX;
            double sideDistY;

            double deltaDistX = fabs(1 / ray_x);
            double deltaDistY = fabs(1 / ray_y);
            double perpWallDist;

            int stepX;
            int stepY;

            int hit = 0;
            int side;

            if (ray_x < 0) {
                stepX = -1;
                sideDistX = (player_x - ray_map_x) * deltaDistX;
            } else {
                stepX = 1;
                sideDistX = (ray_map_x + 1.0 - player_x) * deltaDistX;
            }
            if (ray_y < 0) {
                stepY = -1;
                sideDistY = (player_y - ray_map_y) * deltaDistY;
            } else {
                stepY = 1;
                sideDistY = (ray_map_y + 1.0 - player_y) * deltaDistY;
            }

            while (hit == 0) {
                if (sideDistX < sideDistY) {
                    sideDistX += deltaDistX;
                    ray_map_x += stepX;
                    side = 0;
                } else {
                    sideDistY += deltaDistY;
                    ray_map_y += stepY;
                    side = 1;
                }
                if (map[ray_map_x][ray_map_y] > 0) hit = 1;
            }
            if (side == 0) {
                perpWallDist = (ray_map_x - player_x + (1 - stepX) / 2) / ray_x;
            } else {
                perpWallDist = (ray_map_y - player_y + (1 - stepY) / 2) / ray_y;
            }

            int lineHeight = (int) (screen->h / perpWallDist);
            int drawStart = drawStart = -lineHeight / 2 + screen->h / 2;
            int drawEnd = lineHeight / 2 + screen->h / 2;
            if (WALL_HEIGHT > 1) {
                drawStart -= lineHeight * WALL_HEIGHT; 
            }
            if (drawStart < 0) {
                drawStart = 0;
            }
            if (drawEnd >= screen->h) {
                drawEnd = screen->h - 1;
            }
            
            Uint32 color = RED; // for 1
            switch(map[ray_map_x][ray_map_y]) {
                case 1:
                    color = RED;
                    break;
                case 2:
                    color = YELLOW;
                    break;
                case 3:
                    color = BLUE;
                    break;
                case 4:
                    color = GREEN;
                    break;
                case 5:
                    color = WHITE;
                    break;
                case 6:
                    color = PURPLE;
            }
            
            vertical(x, drawStart, drawEnd, color);
        }
        
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
            SDL_BlitSurface(my_bitmap_key_conv, NULL, screen, &rect2);
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
