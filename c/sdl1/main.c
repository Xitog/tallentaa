#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <math.h>
#include <io.h>
#include "SDL.h"
#include "SDL_image.h"

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

void rectangle(int x1, int y1, int x2, int y2, Uint32 color) {
    if (x1 < 0 || x1 > screen->w - 1 || x2 < 0 || x2 > screen->w - 1 || y1 < 0 || y1 > screen->h -1 || y2 < 0 || y2 > screen->h - 1) {
        return ;
    }
    SDL_Rect rect;
    rect.x = x1;
    rect.y = y1;
    rect.w = x2 - x1 + 1;
    rect.h = y2 - y1 + 1;
    //printf("%d %d %d %d\n", rect.x, rect.y, rect.w, rect.h);
    SDL_FillRect(screen, &rect, color);
}

/*
void quit(void) {
    SDL_Quit();
}
*/

/*
void input(void) {
    SDL_PollEvent(&event);
    inkeys = SDL_GetKeyState(NULL);
}
*/

bool file_exist(char * file) {
    return  (_access(file, 0) != -1);
}

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

#define TEST 1
#define WOOLFY 5

int MODE = WOOLFY;

#define MAP_WIDTH 20
#define MAP_HEIGHT 20

int map[MAP_WIDTH][MAP_HEIGHT] = {
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
};

int map_height[MAP_WIDTH][MAP_HEIGHT] = {
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
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

#define TEXTURES

#ifdef TEXTURES
#define TEX_WIDTH 64
#define TEX_HEIGHT 64
Uint32 textures[8][TEX_WIDTH * TEX_HEIGHT];

void generate_textures(void) {
    for(int x = 0; x < TEX_WIDTH; x++) {
        for(int y = 0; y < TEX_HEIGHT; y++) {
            int xorcolor = (x * 256 / TEX_WIDTH) ^ (y * 256 * TEX_HEIGHT);
            int ycolor = y * 256 / TEX_HEIGHT;
            int xycolor = y * 128 / TEX_HEIGHT + x * 128 / TEX_WIDTH;
            textures[0][TEX_WIDTH * y + x] = 65536 * 254 * (x != y && x != TEX_WIDTH - y);
            textures[1][TEX_WIDTH * y + x] = xycolor + 256 * xycolor + 65536 * xycolor;
            textures[2][TEX_WIDTH * y + x] = 256 * xycolor + 65536 * xycolor;
            textures[3][TEX_WIDTH * y + x] = xorcolor + 256 * xorcolor + 656536 * xorcolor;
            textures[4][TEX_WIDTH * y + x] = 256 * xorcolor;
            textures[5][TEX_WIDTH * y + x] = 65536 * 192 * (x % 16 & y % 16);
            textures[6][TEX_WIDTH * y + x] = 65536 * ycolor;
            textures[7][TEX_WIDTH * y + x] = 128 + 256 * 128 + 65536 * 128; 
        }
    }
}
#endif

#define not !

static Uint8 *audio_chunk; // wav_buffer
static Uint32 audio_len; // wav_length
static Uint8 *audio_pos;

void fill_audio(void *udata, Uint8 *stream, int len) {
    // Only play if we have data left
    if ( audio_len == 0 ) {
        return;
    }
    printf("fill_audio : %d\n", audio_len);
    // Mix as much data as possible = cap
    //len = ( len > (int) audio_len ? audio_len : len );
    if (len > (int) audio_len) {
        len = audio_len;
    }
    SDL_MixAudio(stream, audio_pos, len, SDL_MIX_MAXVOLUME);
    audio_pos += len;
    audio_len -= len;
}

SDL_Surface * load_image(char * filename ) {
    SDL_Surface * loadedImage = NULL;
    SDL_Surface * optimizedImage = NULL;
    loadedImage = IMG_Load(filename);
    if( loadedImage != NULL ) {
        optimizedImage = SDL_DisplayFormat( loadedImage );
        SDL_FreeSurface( loadedImage ); 
    }
    return optimizedImage;
}

// Il faut un buffer et ne pas ecrire directement sur le screen !
// tex width & height = 64
int main(int argc, char * argv[]) {
    int err = init("Test Simple SDL 1", 640, 400, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }
    Uint32 buffer[screen->h][screen->w];
    // Info
    display_info_on_surface(screen);
    // Colors
    player_x = 5; // screen->w / 2;
    player_y = 5; // screen->h / 2;
    direction_x = -1;
    direction_y = 0;
    camera_x = 0;
    camera_y = 0.66;
    Uint32 RED = SDL_MapRGB(screen->format, 255, 0, 0);
    Uint32 GREEN = SDL_MapRGB(screen->format, 0, 255, 0);
    Uint32 BLUE = SDL_MapRGB(screen->format, 0, 0, 255);
    Uint32 BLACK = SDL_MapRGB(screen->format, 0, 0, 0);
    Uint32 YELLOW = SDL_MapRGB(screen->format, 255, 255, 0);
    Uint32 WHITE = SDL_MapRGB(screen->format, 255, 255, 255);
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;
    double move_modifier = 0.002; //0.2;
    double rot_modifier = 0.001; // 0.01;
    int ZOOM = 10;
    
    #ifdef TEXTURES
    generate_textures();
    #endif

    // Normal BMP
    char * file_path = "..\\..\\assets\\graphic\\textures\\woolfy_wall\\noni_a_006.bmp";
    if (not file_exist(file_path)) {
        printf("[ERROR] File not found: %s\n", file_path);
        return EXIT_FAILURE;
    }
    SDL_Surface * my_bitmap = SDL_LoadBMP(file_path);
    SDL_Surface * my_bitmap_conv = SDL_DisplayFormat(my_bitmap);
    SDL_FreeSurface(my_bitmap);

    SDL_Rect rect;
    rect.x = 0;
    rect.y = 0;
    rect.w = my_bitmap->w;
    rect.h = my_bitmap->h;

    // With colorkey
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
    
    // Another format
    SDL_Surface *  my_png_conv = load_image("..\\..\\assets\\graphic\\textures\\woolfy_wall\\noni_a_006_dg.png");
    SDL_Rect rect3;
    rect3.x = 400;
    rect3.y = 5;
    rect3.w = my_png_conv->w;
    rect3.h = my_png_conv->h;
    
    //---------------------------------------------------------------------
    // Sound test
    //---------------------------------------------------------------------
    
    char name[32];
    printf("Using audio driver: %s\n", SDL_AudioDriverName(name, 32));

    SDL_AudioSpec desired;
    SDL_AudioSpec obtained;
    
    desired.freq = 22050;
    desired.format = AUDIO_S16LSB;
    desired.channels = 0; // mono
    desired.samples = 8192;
    //desired.callback = fill_audio;
    desired.userdata = NULL;
    
    /* Load the WAV */
    if(SDL_LoadWAV("blip.wav", &obtained, &audio_chunk, &audio_len) == NULL ){
      fprintf(stderr, "Could not open test.wav: %s\n", SDL_GetError());
      exit(-1);
    } else {
        printf("Audio len = %d\n", audio_len);
    }
    audio_pos = audio_chunk;
    obtained.callback = fill_audio;
    SDL_OpenAudio(&obtained, NULL);
    SDL_PauseAudio(0); // Start playing

    //---------------------------------------------------------------------
    
    while(!done) {
        //---------------------------------------------------------------------
        // Rendering
        //---------------------------------------------------------------------
        fill(BLACK);
        if (MODE == WOOLFY) {
            for (int x = 0; x < screen->w; x++) {
                //vertical(x, 0, screen->h - 1, RED);
                //double raycast_cpt = 2 * ((x / screen->w) - 0.5); // -1 to +1
                double raycast_cpt = 2 * x / (float) screen->w - 1;
                double ray_x = direction_x + camera_x * raycast_cpt;
                double ray_y = direction_y + camera_y * raycast_cpt;

                int map_x = (int) player_x;
                int map_y = (int) player_y;

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
                    sideDistX = (player_x - map_x) * deltaDistX;
                } else {
                    stepX = 1;
                    sideDistX = (map_x + 1.0 - player_x) * deltaDistX;
                }
                if (ray_y < 0) {
                    stepY = -1;
                    sideDistY = (player_y - map_y) * deltaDistY;
                } else {
                    stepY = 1;
                    sideDistY = (map_y + 1.0 - player_y) * deltaDistY;
                }

                while (hit == 0) {
                    if (sideDistX < sideDistY) {
                        sideDistX += deltaDistX;
                        map_x += stepX;
                        side = 0;
                    } else {
                        sideDistY += deltaDistY;
                        map_y += stepY;
                        side = 1;
                    }
                    //printf("x = %d and map : %d - %d\n", x, map_x, map_y);
                    if (map[map_x][map_y] > 0) hit = 1;
                }
                if (side == 0) {
                    perpWallDist = (map_x - player_x + (1 - stepX) / 2) / ray_x;
                } else {
                    perpWallDist = (map_y - player_y + (1 - stepY) / 2) / ray_y;
                }

                int lineHeight = (int) (screen->h / perpWallDist);
                int drawStart = 0;
                switch(map_height[map_x][map_y]) {
                    case 1:
                        drawStart = -lineHeight / 2 + screen->h / 2;
                        break;
                    case 2:
                        drawStart = -lineHeight / 2 - lineHeight + screen->h / 2;
                        break;
                    case 3:
                        drawStart = -lineHeight / 2 - lineHeight * 2 + screen->h / 2;
                        break;
                    case 4:
                        drawStart = -lineHeight / 2 - lineHeight * 3 + screen->h / 2;
                        break;
                }
                int drawEnd = lineHeight / 2 + screen->h / 2;
                if (drawStart < 0) {
                    drawStart = 0;
                }
                if (drawEnd >= screen->h) {
                    drawEnd = screen->h - 1;
                }
                
                Uint32 color = RED; // for 1
                switch(map[map_x][map_y]) {
                    case 2:
                        color = YELLOW;
                        break;
                    case 3:
                        color = BLUE;
                        break;
                    case 4:
                        color = GREEN;
                        break;
                    default:
                        color = RED;
                }

                #ifndef TEXTURES
                // side change color ?
                vertical(x, drawStart, drawEnd, color);
                #else
                if (color == RED) {
                    double wallX;
                    if (side == 0) {
                        wallX = player_x + perpWallDist * ray_x;
                    } else {
                        wallX = player_x + perpWallDist * ray_x; // euh...
                    }
                    wallX -= floor(wallX);
                    int tex_x = (int) (wallX * TEX_WIDTH);
                    if (side == 0 && ray_x > 0) {
                        tex_x = TEX_WIDTH - tex_x - 1;
                    }
                    if (side == 1 && ray_y < 0) {
                        tex_x = TEX_WIDTH - tex_x - 1; // euh...
                    }
                    for (int y = drawStart; y < drawEnd; y++) {
                        pixel(x, y, YELLOW); //textures[0][0]);
                    }
                } else {
                    vertical(x, drawStart, drawEnd, color);
                }
                #endif
            }
            
            int FACTOR = 20;

            int minimap_player_x = player_x * FACTOR;
            int minimap_player_y = player_y * FACTOR;
            int minimap_posdirx = minimap_player_x + direction_x * ZOOM;
            int minimap_posdiry = minimap_player_y + direction_y * ZOOM;

            line(minimap_player_x, minimap_player_y, minimap_posdirx, minimap_posdiry, BLUE);
            line(minimap_posdirx, minimap_posdiry, minimap_posdirx + camera_x * ZOOM, minimap_posdiry + camera_y * ZOOM, YELLOW);
            line(minimap_posdirx, minimap_posdiry, minimap_posdirx - camera_x * ZOOM, minimap_posdiry - camera_y * ZOOM, YELLOW);
            line(minimap_player_x, minimap_player_y, minimap_posdirx + camera_x * ZOOM, minimap_posdiry + camera_y * ZOOM, YELLOW);
            line(minimap_player_x, minimap_player_y, minimap_posdirx - camera_x * ZOOM, minimap_posdiry - camera_y * ZOOM, YELLOW);
            pixel(minimap_player_x, minimap_player_y, GREEN);
            circle(minimap_player_x, minimap_player_y, ZOOM * 4, WHITE);

            for(int y = 0; y < MAP_HEIGHT; y++) {
                for(int x = 0; x < MAP_WIDTH; x++) {
                    if (map[x][y] > 0) {
                        //rectangle(x * 32, y * 32, x+32, y+32, WHITE);
                        vertical(x * FACTOR, y * FACTOR, (y + 1) * FACTOR, WHITE);
                        vertical((x + 1) * FACTOR, y * FACTOR, (y + 1) * FACTOR, WHITE);
                        horizontal(y * FACTOR, x * FACTOR, (x + 1) * FACTOR, WHITE);
                        horizontal((y + 1) * FACTOR, x * FACTOR, (x + 1) * FACTOR, WHITE);
                    }
                }
            }

        } else {
            int posdirx = player_x + direction_x * ZOOM;
            int posdiry = player_y + direction_y * ZOOM;

            SDL_BlitSurface(my_bitmap_conv, NULL, screen, &rect);
            SDL_BlitSurface(my_bitmap_key_conv, NULL, screen, &rect2);
            SDL_BlitSurface(my_png_conv, NULL, screen, &rect3);

            line(player_x, player_y, posdirx, posdiry, BLUE);
            line(posdirx, posdiry, posdirx + camera_x * ZOOM, posdiry + camera_y * ZOOM, YELLOW);
            line(posdirx, posdiry, posdirx - camera_x * ZOOM, posdiry - camera_y * ZOOM, YELLOW);
            line(player_x, player_y, posdirx + camera_x * ZOOM, posdiry + camera_y * ZOOM, YELLOW);
            line(player_x, player_y, posdirx - camera_x * ZOOM, posdiry - camera_y * ZOOM, YELLOW);
            pixel(player_x, player_y, GREEN);
            circle(player_x, player_y, ZOOM * 4, BLACK);

            disk(250, 250, ZOOM * 4, WHITE);
            circle(200, 100, ZOOM, WHITE);
            pixel(200, 100, YELLOW);
            get(200, 100);
            rectangle(500, 300, 600, 350, WHITE);
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
        //printf("%f.%f %f\n", player_x, player_y, frame_time); 
    }
    SDL_FreeSurface(my_bitmap_conv);
    SDL_FreeSurface(my_bitmap_key_conv);
    SDL_FreeWAV(audio_chunk);
    SDL_PauseAudio(1);
    SDL_CloseAudio();
    SDL_Quit();
    return EXIT_SUCCESS;
}
