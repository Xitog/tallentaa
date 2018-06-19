//=============================================================================
// Demo program for minisdl.c
// Show examples of the function of minisdl library based on SDL 1.2.15
// Show examples of handling time in C (getting a string, difftime, timestamp)
// Show examples of handling Lua (registering C function, interpreting Lua)
// Show examples of loading a PNG image with SDL_image
// Needed DLL : SDL.dll, SDL_image.dll, zlib1.dll, lua53.dll, libpng15-15.dll
//-----------------------------------------------------------------------------
// Author           Damien Gouteux
// Created          2018
// Last modified    19 june 2018
//=============================================================================

//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

// Standard librairies
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <math.h>
#include <io.h>

// Internal librairies
#include "minisdl.h"

// SDL libraries
#include "SDL.h"

// Time examples
#include <time.h>

// Lua libraries
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

// SDL images
#include "SDL_image.h"

//-----------------------------------------------------------------------------
// Type definitions
//-----------------------------------------------------------------------------

typedef struct {
    int x;
    int y;
} Position;

//-----------------------------------------------------------------------------
// Global constants
//-----------------------------------------------------------------------------

const char * APPNAME = "ACTION";

const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int BITS_PER_PIXEL = 32;
const bool FULLSCREEN = false;

const char * SOUND_PATH = "..\\assets\\audio\\sounds\\blip.wav";
const char * TEXTURE_PATH = "..\\assets\\graphic\\walls\\door11_1.bmp";
const char * TEXTURE_COLOR_KEY_PATH = "..\\assets\\graphic\\walls\\mguard_s_1.bmp";
const char * TEXTURE_PNG_PATH = "..\\assets\\graphic\\walls\\tile110.png";

#define DEF_MAP_SIZE 32
const int MAP_SIZE = DEF_MAP_SIZE;
const int MAP[DEF_MAP_SIZE][DEF_MAP_SIZE] = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};

//-----------------------------------------------------------------------------
// Global variables
//-----------------------------------------------------------------------------

// Keys
bool down;
bool up;
bool right;
bool left;

// Global states
bool done = false;
bool pause = false;

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

void wait_pause(void) {
    if (SDL_PollEvent(&event)) {
        if (event.type == SDL_KEYUP) {
            switch (event.key.keysym.sym) {
                case SDLK_SPACE:
                    pause = !pause;
                    break;
            }
        } else if (event.type == SDL_QUIT ) {
            done = true;
        }
    }
}

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
                    // nothing
                    break;
                case SDLK_SPACE:
                    pause = !pause;
                    break;
                case SDLK_s:
                    // nothing
                    break;
            }
       } else if (event.type == SDL_QUIT ) {
            done = true;
       }
    }
}

//
// Random functions
//

void rand_init(void) {
    srand(time(NULL));
}

int rand_int(const int max) {
    // Getting a random number from 1 to MAX included
    const int BARRE = RAND_MAX / max;
    int nb = 1;
    int nb_barre = BARRE;
    int randomValue = rand();
    while (randomValue > nb_barre) {
        nb_barre += BARRE;
        nb += 1;
    }
    return nb;
}

//
// Time functions
//

void time_now_stamp(char time_stamp[], unsigned int size) {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    const struct tm * restrict tmp = &tm;
    strftime(time_stamp, size, "%Y-%m-%d_%H-%M-%S", tmp);
}

void time_now_string(char time_string[], unsigned int size) {
    // Getting time
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    const struct tm * restrict tmp = &tm;
    strftime(time_string, size, "%c", tmp);
}

//
// Lua function to register
//

static int twice(lua_State * lua) {
    double arg = lua_tonumber(lua, 1);  /* get argument */
    lua_pushnumber(lua, arg * 2);       /* push result */
    return 1;                           /* number of results */
}

// SDL image function
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

//
// Test function
//

void tests(void) {
    // Time
    char time_string[64];
    time_now_stamp(time_string, 64);
    printf("A time stamp: %s\n", time_string);

    // Random
    rand_init();
    for(int i=0; i < 10; i++) {
        printf("Dice : %d\n", rand_int(6));
    }
    
    // Lua
    lua_State * lua = luaL_newstate();
    luaL_openlibs(lua);

    lua_pushcfunction(lua, twice);
    lua_setglobal(lua, "twiceC");

    int res = luaL_dostring(lua, "print(\"Lua is here\")");
    printf("retour = %d\n", res);

    res = luaL_dostring(lua, "a = twiceC(2)");
    printf("retour = %d\n", res);

    res = luaL_dostring(lua, "print(a)");
    printf("retour = %d\n", res);

    lua_close(lua);
}

//-----------------------------------------------------------------------------
// Main function
//-----------------------------------------------------------------------------

int main(int argc, char * argv[]) {
    
    time_t start = time(NULL);
    
    char time_string[64];
    time_now_string(time_string, sizeof(time_string));
    
    // Init message
    printf("Start %s at %s\n", APPNAME, time_string);
    
    // Tests
    tests();

    // Init and screen
    int err = init((char *) APPNAME, SCREEN_WIDTH, SCREEN_HEIGHT, BITS_PER_PIXEL, FULLSCREEN);
    if (err == EXIT_FAILURE) {
        return err;
    }
    
    // Sound Test
    char name[32];
    printf("Using audio driver: %s\n", SDL_AudioDriverName(name, 32));
    init_audio(22050, AUDIO_U8, 1, 4096);
    load_wav(SOUND_PATH);
    play_wav();
    
    // Texture Test
    SDL_Surface * my_bitmap_conv = load_bmp(TEXTURE_PATH);
    
    // Texture Test with colorkey
    SDL_Surface * my_bitmap_key_conv = load_bmp(TEXTURE_COLOR_KEY_PATH);
    Uint32 key = SDL_MapRGB(screen->format, 152, 0, 136);
    SDL_SetColorKey(my_bitmap_key_conv, SDL_SRCCOLORKEY | SDL_RLEACCEL, key);
    
    // Texture from PNG
    // Another format
    SDL_Surface * my_png_conv = load_image((char *) TEXTURE_PNG_PATH);
    
    // Time
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;

    // Main loop
    while(!done) {
        // Prerendering computations
        // do something

        // Rendering
        fill(BLACK);
        // Examples
        vertical(100, 100, 200, PURPLE);
        horizontal(100, 100, 300, BLUE);
        line(100, 200, 300, 200, WHITE);
        circle(100, 100, 50, YELLOW);
        disk(300, 200, 20, GREEN);
        for(int i = 100; i <= 200; i++) {
            pixel(300, i, RED);
        }

        blit(500, 100, my_bitmap_conv);
        blit(500, 200, my_bitmap_key_conv);
        blit(500, 300, my_png_conv);

        // End of examples
        render();
        
        // Input
        input();

        // Time
        tick_previous = tick_current;
        tick_current = SDL_GetTicks();
        frame_time = (tick_current - tick_previous);

        // Update
        // do something

        // Pause
        while (pause && !done) {
            wait_pause();
            tick_current = SDL_GetTicks();
        }
    }

    // Cleaning
    SDL_Quit();
    time_t end = time(NULL);
    double elapsed = difftime(end, start);
    printf("End %s. Time elapsed: %02dh%02d\n", APPNAME, (int) elapsed / 60, (int) elapsed % 60);
    return EXIT_SUCCESS;

}
