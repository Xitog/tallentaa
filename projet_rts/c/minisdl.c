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

//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

#include "minisdl.h"

//-----------------------------------------------------------------------------
// Public globals
//-----------------------------------------------------------------------------

SDL_Surface * screen;
SDL_Event event = {0};

//-----------------------------------------------------------------------------
// Globals
//-----------------------------------------------------------------------------

SDL_AudioSpec audiospec;
Uint8 * audio_chunk; // wav_buffer
Uint32 audio_len; // wav_length
Uint8 * audio_pos;

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

int init(char * title, int width, int height, int color, bool fullscreen) {
    if (SDL_Init(SDL_INIT_EVERYTHING) < 0) {
        perror("Error when initializing SDL");
        return EXIT_FAILURE;
    }
    if (fullscreen) {
        screen = SDL_SetVideoMode(width, height, color, SDL_SWSURFACE | SDL_FULLSCREEN);
    } else {
        screen = SDL_SetVideoMode(width, height, color, SDL_SWSURFACE | SDL_HWPALETTE);
    }
    if (screen == NULL) {
        printf("Error when setting video mode : %s\n", SDL_GetError());
        SDL_Quit();
        return EXIT_FAILURE;
    }
    SDL_WM_SetCaption(title, NULL);
    SDL_EnableUNICODE(true);
    return EXIT_SUCCESS;
}

void fill_audio(void *udata, Uint8 *stream, int len) {
    // Only play if we have data left
    if ( audio_len == 0 ) {
        return;
    }
    printf("fill_audio : %d\n", audio_len);
    // Mix as much data as possible = cap
    if (len > (int) audio_len) {
        len = audio_len;
    }
    SDL_MixAudio(stream, audio_pos, len, SDL_MIX_MAXVOLUME);
    audio_pos += len;
    audio_len -= len;
}

int load_wav(const char * path) {
    if(SDL_LoadWAV(path, &audiospec, &audio_chunk, &audio_len) == NULL ){
      fprintf(stderr, "Could not open audio file: %s\n", SDL_GetError());
      exit(-1);
    } else {
        printf("Audio len = %d\n", audio_len);
    }
    return EXIT_SUCCESS;
}

void play_wav(void) {
    audio_pos = audio_chunk;
    SDL_PauseAudio(0); // Start playing
}

int init_audio(int freq, Uint16 format, Uint8 channels, Uint16 samples) {
    audiospec.freq = freq;
    audiospec.format = format;
    audiospec.channels = channels;
    audiospec.samples = samples;
    audiospec.callback = fill_audio;
    audiospec.userdata = NULL;

    SDL_OpenAudio(&audiospec, NULL);
    return EXIT_SUCCESS;
}

void stop_audio(void) {
    SDL_FreeWAV(audio_chunk);
    SDL_PauseAudio(1);
    SDL_CloseAudio();
}

void display_info_on_surface(SDL_Surface * surf) {
    printf("-- SDL_Surface Info\n");
    printf("Uint32 flags = %d\n", surf->flags);
    printf("int w, h = %d, %d\n", surf->w, surf->h);
    printf("Uint16 pitch = %d\n", surf->pitch);
    printf("void *pixels"); // writable
    //SDL_Rect clip_rect;
    printf("int refcount  = %d\n", surf->refcount); // read mostly

    printf("-- SDL_PixelFormat Info\n");
    printf("SDL_Palette * palette = %d\n", (int) surf->format->palette);
    printf("Uint8  BitsPerPixel = %d\n", surf->format->BitsPerPixel);
    printf("Uint8  BytesPerPixel = %d\n", surf->format->BytesPerPixel);
    printf("Uint8  Rloss = %d, Gloss = %d, Bloss = %d, Aloss = %d\n", surf->format->Rloss, surf->format->Gloss, surf->format->Bloss, surf->format->Aloss);
    printf("Uint8  Rshift = %d, Gshift = %d, Bshift = %d, Ashift = %d\n", surf->format->Rshift, surf->format->Gshift, surf->format->Bshift, surf->format->Ashift);
    printf("Uint8  Rmask = %d, Gmask = %d, Bmask = %d, Amask = %d\n", surf->format->Rmask, surf->format->Gmask, surf->format->Bmask, surf->format->Amask);
    printf("Uint32 colorkey = %d\n", surf->format->colorkey);
    printf("Uint8  alpha = %d\n", surf->format->alpha);

    int mustlock = SDL_MUSTLOCK(screen); 
    printf("Do I have to lock? %d\n", mustlock); // 0 = No. Software surface don't need.
}

// slow
void render(void) {
    SDL_UpdateRect(screen, 0, 0, 0, 0);
}

void fill(Uint32 color) {
    SDL_FillRect(screen, NULL, color); //65536 * color->red + 256 * color->green + color->blue);
}

void pixel(int x, int y, Uint32 color) {
    if (x < 0 || y < 0 || x >= screen->w || y >= screen->h) {
        return;
    }
    //Uint32 * bufp = (Uint32*)screen->pixels + y * (screen->pitch >> 2) + x;
    int bpp = screen->format->BytesPerPixel;
    Uint8 *bufp = (Uint8 *)screen->pixels + y * screen->pitch + x * bpp;
    *(Uint32*)bufp = color;
}

Uint32 get(int x, int y) {
    if (x < 0 || y < 0 || x >= screen->w || y >= screen->h) {
        return 0;
    }
    //int bpp = 0;
    //int bpp = screen->format->BytesPerPixel;
    //Uint8 * bufp = (Uint8 *)screen->pixels + y * screen->pitch + x * bpp;
    Uint32 * bufp = (Uint32*)screen->pixels + y * (screen->pitch >> 2) + x;
    // Debug
    /*
    Uint8 red;
    Uint8 green;
    Uint8 blue;
    printf("Value BUFP = %d, BPP = %d, x = %d, y = %d\n", *bufp, bpp, x, y);
    SDL_GetRGB(*bufp, screen->format, &red, &green, &blue);
    printf("RED %d GREEN %d BLUE %d\n", red, green, blue);
    */
    // End debug
    return *bufp;
}

void buffer(Uint32 (* pbuffer)[640]) {
    for(int x = 0; x < screen->w; x++) {
        for(int y = 0; y < screen->h; y++) {
            pixel(x, y, pbuffer[y][x]);
            pbuffer[y][x] = 0; //clear the buffer instead of cls()
        }
    }
    /*
    Uint32 * bufp = (Uint32*) screen->pixels;
    for (int y = 0; y < screen->h; y++) {
        for (int x = 0; x < screen->w; x++) {
            *bufp = buffer[y * screen->w + x];
            bufp++;
        }
        bufp += screen->pitch << 2;
        bufp -= screen->w;
    }
    */
}

// Use Bresenham algorithm
void line(int x1, int y1, int x2, int y2, Uint32 color) {
    int deltax = abs(x2 - x1);
    int deltay = abs(y2 - y1);
    int x = x1;
    int y = y1;
    int modx1;
    int modx2;
    int mody1;
    int mody2;
    int num;
    int den;
    int numadd;
    int numpixels;
    if (x2 >= x1) {
        modx1 = 1;
        modx2 = 1;
    } else {
        modx1 = -1;
        modx2 = -1;
    }
    if (y2 >= y1) {
        mody1 = 1;
        mody2 = 1;
    } else {
        mody1 = -1;
        mody2 = -1;
    }
    if (deltax >= deltay) {
        modx1 = 0;
        mody2 = 0;
        den = deltax;
        num = deltax >> 1;
        numadd = deltay;
        numpixels = deltax;
    } else {
        modx2 = 0;
        mody1 = 0;
        den = deltay;
        num = deltay >> 1;
        numadd = deltax;
        numpixels = deltay;
    }
    for (int pix = 0; pix <= numpixels; pix++) {
        pixel(x, y, color);
        num += numadd;
        if (num >= den) {
            num -= den;
            x += modx1;
            y += mody1;
        }
        x += modx2;
        y += mody2;
    }
}

void vertical(int x, int y1, int y2, Uint32 color) {
    // swap
    if (y2 < y1) {
        y1 += y2;
        y2 = y1 - y2;
        y1 -= y2;
    }
    if (y2 < 0 || y1 >= screen->h || x < 0 || x >= screen->w) {
        return;
    }
    // clip
    if (y1 < 0) {
        y1 = 0;
    }
    if (y2 >= screen->h) {
        y2 = screen->h - 1;
    }
    Uint32 * bufp = (Uint32*)screen->pixels + y1 * (screen->pitch >> 2) + x;
    for (int y = y1; y <= y2; y++) {
        *bufp = color;
        bufp += screen->pitch >> 2;
    }
    return;
}

void horizontal(int y, int x1, int x2, Uint32 color) {
    // swap
    if (x2 < x1) {
        x1 += x2;
        x2 = x1 - x2;
        x1 -= x2;
    }
    if (x2 < 0 || x1 >= screen->w || y < 0 || y >= screen->h) {
        return;
    }
    // clip
    if (x1 < 0) {
        x1 = 0;
    }
    if (x2 >= screen->w) {
        x2 = screen->w - 1;
    }
    Uint32 * bufp = (Uint32*)screen->pixels + y * (screen->pitch >> 2) + x1;
    for (int x = x1; x <= x2; x++) {
        *bufp = color;
        bufp++;
    }
}

void circle(int x, int y, int radius, Uint32 color) {
    if (x - radius < 0 || x + radius >= screen->w || y - radius < 0 || y + radius >= screen->h) {
        return;
    }
    int i = 0;
    int j = radius;
    int p = 3 - (radius << 1);
    int a, b, c, d, e, f, g, h;
    while (i <= j) {
        a = x + i;
        b = y + j;
        c = x - i;
        d = y - j;
        e = x + j;
        f = y + i;
        g = x - j;
        h = y - i;
        pixel(a, b, color);
        pixel(c, d, color);
        pixel(e, f, color);
        pixel(g, f, color);
        if (i > 0) {
            pixel(a, d, color);
            pixel(c, b, color);
            pixel(e, h, color);
            pixel(g, h, color);
        }
        if (p < 0) {
            p += (i++ << 2) + 6;
        } else {
            p += ((i++ - j--) << 2) + 10;
        }
    }
}

void disk(int x, int y, int radius, Uint32 color) {
    if (x - radius < 0 || x + radius >= screen->w || y - radius < 0 || y + radius >= screen->h) {
        return;
    }
    int i = 0;
    int j = radius;
    int p = 3 - (radius << 1);
    int a, b, c, d, e, f, g, h;
    int pb = y + radius + 1;
    int pd = y + radius + 1;
    while (i <= j) {
        a = x + i;
        b = y + j;
        c = x - i;
        d = y - j;
        e = x + j;
        f = y + i;
        g = x - j;
        h = y - i;
        if (b != pb) {
            horizontal(b, a, c, color);
        }
        if (d != pd) {
            horizontal(d, a, c, color);
        }
        if (f != b) {
            horizontal(f, e, g, color);
        }
        if (h != d && h != f) {
            horizontal(h, e, g, color);
        }
        pb = b;
        pd = d;
        if (p < 0) {
            p += (i++ << 2) + 6;
        } else {
            p += ((i++ - j--) << 2) + 10;
        }
    }
}

void rectangle(int x1, int y1, int x2, int y2, Uint32 color, bool filled) {
    //if (x1 < 0 || x1 > screen->w - 1 || x2 < 0 || x2 > screen->w - 1 || y1 < 0 || y1 > screen->h -1 || y2 < 0 || y2 > screen->h - 1) {
    //    return ;
    //}
    if (filled) {
        SDL_Rect rect;
        rect.x = x1;
        rect.y = y1;
        rect.w = x2 - x1 + 1;
        rect.h = y2 - y1 + 1;
        //printf("%d %d %d %d\n", rect.x, rect.y, rect.w, rect.h);
        SDL_FillRect(screen, &rect, color);
    } else {
        vertical(x1, y1, y2, color);
        vertical(x2, y1, y2, color);
        horizontal(y1, x1, x2, color);
        horizontal(y2, x1, x2, color);
    }
}

SDL_Surface * load_bmp(const char * file_path) {
    if (not file_exist(file_path)) {
        printf("[ERROR] File not found: %s\n", file_path);
        return NULL;
    }
    SDL_Surface * my_bitmap = SDL_LoadBMP(file_path);
    SDL_Surface * my_bitmap_conv = SDL_DisplayFormat(my_bitmap);
    SDL_FreeSurface(my_bitmap);
    return my_bitmap_conv;
}

bool file_exist(const char * file) {
    return  (_access(file, 0) != -1);
}

void blit(int x, int y, SDL_Surface * surf) {
    SDL_Rect rect;
    rect.x = x;
    rect.y = y;
    rect.w = surf->w;
    rect.h = surf->h;
    SDL_BlitSurface(surf, NULL, screen, &rect);
}
