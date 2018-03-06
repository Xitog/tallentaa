#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <math.h>
#include "SDL.h"

//-----------------------------------------------------------------------------
// Globals
//-----------------------------------------------------------------------------

SDL_Surface * screen;
SDL_Event event = {0};
Uint8 * inkeys;

typedef struct {
    int red;
    int green;
    int blue;
} ColorRGB;

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

void buffer(Uint32 * buffer) {
    Uint32 * bufp = (Uint32*) screen->pixels;
    for (int y = 0; y < screen->h; y++) {
        for (int x = 0; x < screen->w; x++) {
            *bufp = buffer[y * screen->w + x];
            bufp++;
        }
        bufp += screen->pitch << 2;
        bufp -= screen->w;
    }
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
        y2 = screen->h -1;
    }
    Uint32 * bufp = (Uint32*)screen->pixels + y1 * (screen->pitch >> 2) + x;
    for (int y = y1; y <= y2; y++) {
        *bufp = color;
        bufp += screen->pitch >> 2;
    }
    return;
}

void quit(void) {
    SDL_Quit();
}

/*
void input(void) {
    SDL_PollEvent(&event);
    inkeys = SDL_GetKeyState(NULL);
}
*/

bool down;
bool up;
bool right;
bool left;
bool done = false;
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
            }
       } else if (event.type == SDL_QUIT ) {
            done = true;
       }
    }
}

/*
bool close(bool quit_if_esc, bool delay) {
    if (delay) {
        SDL_Delay(5);
    }
    int done = false;
    if (!SDL_PollEvent(&event)) {
        // done = 0;
    } else {
        input();
        if(quit_if_esc && inkeys[SDLK_ESCAPE]) {
            done = true;
        }
        if(event.type == SDL_QUIT) {
            done = true;
        }
    }
    return done;
}
*/

double player_x;
double player_y;
double direction_x;
double direction_y;

void display_info_on_surface(SDL_Surface * surf) {
    // https://www.libsdl.org/release/SDL-1.2.15/docs/html/sdlsurface.html

    printf("Uint32 flags = %d\n", surf->flags);
    //SDL_PixelFormat *format;
    //SDL_Palette *palette;
    printf("Uint8  BitsPerPixel = %d\n", surf->format->BitsPerPixel);
    printf("Uint8  BytesPerPixel = %d\n", surf->format->BytesPerPixel);
    //Uint8  Rloss, Gloss, Bloss, Aloss;
    //Uint8  Rshift, Gshift, Bshift, Ashift;
    //Uint32 Rmask, Gmask, Bmask, Amask;
    printf("Uint32 colorkey = %d\n", surf->format->colorkey);
    printf("Uint8  alpha = %d\n", surf->format->alpha);

    printf("int w, h = %d, %d\n", surf->w, surf->h);
    printf("Uint16 pitch = %d\n", surf->pitch);
    printf("void *pixels"); // writable
    //SDL_Rect clip_rect;
    printf("int refcount  = %d\n", surf->refcount); // read mostly
    int mustlock = SDL_MUSTLOCK(screen); 
    printf("Do I have to lock? %d\n", mustlock); // 0 = No. Software surface don't need.
}

// Il faut un buffer et ne pas écrire directement sur le screen !
int main(int argc, char * argv[]) {
    int err = init("Test Simple SDL 1", 640, 400, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }
    Uint32 buffer[screen->h][screen->w];
    // Info
    display_info_on_surface(screen);
    // Colors
    player_x = screen->w / 2;
    player_y = screen->h / 2;
    direction_x = -1;
    direction_y = 0;
    Uint32 RED = SDL_MapRGB(screen->format, 255, 0, 0);
    Uint32 GREEN = SDL_MapRGB(screen->format, 0, 255, 0);
    Uint32 BLUE = SDL_MapRGB(screen->format, 0, 0, 255);
    Uint32 BLACK = SDL_MapRGB(screen->format, 0, 0, 0);
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;
    double move_modifier = 0.2;
    double rot_modifier = 0.01;
    while(!done) {
        //---------------------------------------------------------------------
        // Rendering
        //---------------------------------------------------------------------
        fill(BLACK);
        for (int x = 0; x < screen->w; x++) {
            vertical(x, 0, screen->h - 1, RED);
            line(player_x, player_y, player_x + direction_x * 5, player_y + direction_y * 5, BLUE);
            pixel(player_x, player_y, GREEN);
        }
        render();
        //---------------------------------------------------------------------
        // Time and input
        //---------------------------------------------------------------------
        input();
        tick_previous = tick_current;
        tick_current = SDL_GetTicks();
        frame_time = (tick_current - tick_previous);
        if (up) {
            player_x += direction_x * move_modifier * frame_time;
            player_y += direction_y * move_modifier * frame_time;
        }
        if (down) {
            player_x -= direction_x * move_modifier * frame_time;
            player_y -= direction_y * move_modifier * frame_time;
        }
        if (right) {
            double old_dir_x = direction_x;
            direction_x = direction_x * cos(rot_modifier * frame_time) - direction_y * sin(rot_modifier * frame_time);
            direction_y = old_dir_x * sin(rot_modifier * frame_time) + direction_y * cos(rot_modifier * frame_time);
        }
        if (left) {
            double old_dir_x = direction_x;
            direction_x = direction_x * cos(-rot_modifier * frame_time) - direction_y * sin(-rot_modifier * frame_time);
            direction_y = old_dir_x * sin(-rot_modifier * frame_time) + direction_y * cos(-rot_modifier * frame_time);
        }
        //printf("%f.%f %f\n", player_x, player_y, frame_time); 
    }
    quit();
    return EXIT_SUCCESS;
}
