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

double player_x;
double player_y;
double direction_x;
double direction_y;
double camera_x;
double camera_y;

int map[10][10] = {
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
};

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

// Il faut un buffer et ne pas ecrire directement sur le screen !
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
    camera_x = 0;
    camera_y = 0.66;
    Uint32 RED = SDL_MapRGB(screen->format, 255, 0, 0);
    Uint32 GREEN = SDL_MapRGB(screen->format, 0, 255, 0);
    Uint32 BLUE = SDL_MapRGB(screen->format, 0, 0, 255);
    Uint32 BLACK = SDL_MapRGB(screen->format, 0, 0, 0);
    Uint32 YELLOW = SDL_MapRGB(screen->format, 255, 255, 0);
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;
    double move_modifier = 0.2;
    double rot_modifier = 0.01;
    int ZOOM = 10;

    SDL_Surface * my_bitmap = SDL_LoadBMP("..\\..\\assets\\graphic\\textures\\woolfy_wall\\noni_a_006.bmp");
    SDL_Surface * my_bitmap_conv = SDL_DisplayFormat(my_bitmap);
    SDL_FreeSurface(my_bitmap);

    SDL_Rect rect;
    rect.x = 0;
    rect.y = 0;
    rect.w = my_bitmap->w;
    rect.h = my_bitmap->h;

    SDL_Surface * my_bitmap_key = SDL_LoadBMP("..\\..\\assets\\graphic\\sprites\\woolfy\\mguard_s_1.bmp");
    SDL_Surface * my_bitmap_key_conv = SDL_DisplayFormat(my_bitmap_key);
    SDL_FreeSurface(my_bitmap_key);

    Uint32 key = SDL_MapRGB(screen->format, 152, 0, 136);
    SDL_SetColorKey(my_bitmap_key_conv, SDL_SRCCOLORKEY | SDL_RLEACCEL, key);

    SDL_Rect rect2;
    rect2.x = my_bitmap_key->w;
    rect2.y = my_bitmap_key->h;
    rect2.w = my_bitmap_key->w;
    rect2.h = my_bitmap_key->h;
    
    while(!done) {
        //---------------------------------------------------------------------
        // Calculations
        //---------------------------------------------------------------------
        int posdirx = player_x + direction_x * ZOOM;
        int posdiry = player_y + direction_y * ZOOM;
        //---------------------------------------------------------------------
        // Rendering
        //---------------------------------------------------------------------
        fill(BLACK);
        for (int x = 0; x < screen->w; x++) {
            vertical(x, 0, screen->h - 1, RED);
            SDL_BlitSurface(my_bitmap_conv, NULL, screen, &rect);
            SDL_BlitSurface(my_bitmap_key_conv, NULL, screen, &rect2);
            line(player_x, player_y, posdirx, posdiry, BLUE);
            line(posdirx, posdiry, posdirx + camera_x * ZOOM, posdiry + camera_y * ZOOM, YELLOW);
            line(posdirx, posdiry, posdirx - camera_x * ZOOM, posdiry - camera_y * ZOOM, YELLOW);
            line(player_x, player_y, posdirx + camera_x * ZOOM, posdiry + camera_y * ZOOM, YELLOW);
            line(player_x, player_y, posdirx - camera_x * ZOOM, posdiry - camera_y * ZOOM, YELLOW);
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
            double old_cam_x = camera_x;
            camera_x = camera_x * cos(rot_modifier * frame_time) - camera_y * sin(rot_modifier * frame_time);
            camera_y = old_cam_x * sin(rot_modifier * frame_time) + camera_y * cos(rot_modifier * frame_time);
        }
        if (left) {
            double old_dir_x = direction_x;
            direction_x = direction_x * cos(-rot_modifier * frame_time) - direction_y * sin(-rot_modifier * frame_time);
            direction_y = old_dir_x * sin(-rot_modifier * frame_time) + direction_y * cos(-rot_modifier * frame_time);
            double old_cam_x = camera_x;
            camera_x = camera_x * cos(-rot_modifier * frame_time) - camera_y * sin(-rot_modifier * frame_time);
            camera_y = old_cam_x * sin(-rot_modifier * frame_time) + camera_y * cos(-rot_modifier * frame_time);
        }
        //printf("%f.%f %f\n", player_x, player_y, frame_time); 
    }
    SDL_FreeSurface(my_bitmap_conv);
    SDL_FreeSurface(my_bitmap_key_conv);
    quit();
    return EXIT_SUCCESS;
}
