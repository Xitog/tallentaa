//=============================================================================
// Simple library to access SDL 1.2
//-----------------------------------------------------------------------------
//
// This work is heavily based on Lode Vandevenne's QuickCG library
// http://lodev.org/quickcg/
//
// QuickCG code source license :
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
//    * This library is a minimalist way to access to the main functionalities of SDL and to have support from drawing basic shapes.
//      Most of the code source is taken from the QuickCG library, all credits for it goes to Lode Vandevenne (thanks!).
//      QuickCG has support for PNG files, a basic font, and an embedded zip library and can be downloaded freely here: http://lodev.org/quickcg/ .
//      All of these was dropped here. I prefer to use standard SDL project (SDL_image, SDL_ttf) for these functionalities, but I still needed basic draw functions.
//      Here they come!
//
//=============================================================================

#ifndef MINISDL_H
#define MINISDL_H

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

//-----------------------------------------------------------------------------
// Syntax sugar
//-----------------------------------------------------------------------------

#ifndef NOT_KEYWORD
#define NOT_KEYWORD
#define not !
#endif

//-----------------------------------------------------------------------------
// Types
//-----------------------------------------------------------------------------

typedef struct {
    int red;
    int green;
    int blue;
} ColorRGB;

typedef enum {
    WHITE     = 255 * 256*256 + 255 * 256 + 255,
    YELLOW    = 255 * 256*256 + 255 * 256 +   0,
    BLUE      =   0 * 256*256 +   0 * 256 + 255,
    RED       = 255 * 256*256 +   0 * 256 +   0,
    GREEN     =   0 * 256*256 + 255 * 256 +   0,
    LIGHTGREY = 211 * 256*256 + 211 * 256 + 211,
    DARKGREY  = 169 * 256*256 + 169 * 256 + 169,
    FLOORGREY = 113 * 256*256 + 113 * 256 + 113,
    CEILGREY  =  56 * 256*256 +  56 * 256 +  56,
    BLACK     =   0 * 256*256 +   0 * 256 +   0,
    PURPLE    = 128 * 256*256 +  64 * 256 + 128,
} Colors;

//-----------------------------------------------------------------------------
// Public globals
//-----------------------------------------------------------------------------

extern SDL_Surface * screen;
extern SDL_Event event;

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

int init(char * title, int width, int height, int color, bool fullscreen);
int init_audio(int freq, Uint16 format, Uint8 channels, Uint16 samples);
int load_wav(const char * path);
void play_wav(void);
void stop_audio(void);
void display_info_on_surface(SDL_Surface * surf);
void render(void);
void fill(Uint32 color);
void pixel(int x, int y, Uint32 color);
Uint32 get(int x, int y);
void buffer(Uint32 (* pbuffer)[640]);
void line(int x1, int y1, int x2, int y2, Uint32 color);
void vertical(int x, int y1, int y2, Uint32 color);
void horizontal(int y, int x1, int x2, Uint32 color);
void circle(int x, int y, int radius, Uint32 color);
void disk(int x, int y, int radius, Uint32 color);
void rectangle(int x1, int y1, int x2, int y2, Uint32 color, bool filled);
SDL_Surface * load_bmp(const char * file_path);
bool file_exist(const char * file);
void blit(int x, int y, SDL_Surface * surf);

#endif
