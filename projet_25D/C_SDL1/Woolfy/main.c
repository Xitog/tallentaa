//-----------------------------------------------------------------------------
// Include
//-----------------------------------------------------------------------------

#include <stdio.h>
#include <math.h>
#include "sdl.h"
#include "draw.h"
#include "event.h"
#include "game.h"

//-----------------------------------------------------------------------------
// Global constants
//-----------------------------------------------------------------------------

const Uint32 SCREEN_WIDTH  = 640;
const Uint32 SCREEN_HEIGHT = 480;

//-----------------------------------------------------------------------------
// Function
//-----------------------------------------------------------------------------

void infosurf(SDL_Surface * surf) {
    printf("%d\n", sizeof(*surf)); // 60
    printf("%d\n", sizeof(*(surf->format))); // 40
    printf("PixelFormat.BytesPexPixel = %d\n", surf->format->BytesPerPixel); // 4
    printf("Surface.Pitch = %d\n", surf->pitch); // 2560
}

void load_textures() {
    // Textures
    TEXTURES[0] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\0-placeholder.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[1] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\1-grey_stone_wall.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[2] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\2-grey_stone_wall_stone.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[3] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\3-light_stone_wall.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[4] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\4-light_stone_wall_stone.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[5] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\5-light_stone_wall_grass.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[6] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\6-light_wood_wall.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[7] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\7-light_wood_wall_window.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[8] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\8-dark_wood_wall.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[9] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\9-red_brick_wall.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[10] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\10-red_brick_wall_light.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[11] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\11-red_brick_wall_pillar.bmp"), screen->format, SDL_SWSURFACE);
    TEXTURES[12] = SDL_ConvertSurface(SDL_LoadBMP(".\\data\\tex\\12-red_brick_wall_bars.bmp"), screen->format, SDL_SWSURFACE);
    infosurf(TEXTURES[0]);
}

int main(int argc, char * argv[]) {
    
    FILE * fp = fopen("D:\\Tools\\Perso\\Projets\\map_editor\\New map.bin", "rb");
    short s1;
    fread(&s1, 2, 1, fp);
    int l1;
    fread(&l1, 4, 1, fp);
    float f1;
    fread(&f1, 4, 1, fp);
    printf("%hd %d %f\n", s1, l1, f1);

    int err = init("Woolfy 2.5 FLAT", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }
    
    load_textures();

    // Time
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;
    
    event_init();
    game_init();
    
    while (!action_state[A_ESCAPE]) {
        // Draw
        game_draw();
        render();
 
        // Input
        event_input();

        // Time
        tick_previous = tick_current;
        tick_current = SDL_GetTicks();
        frame_time = (tick_current - tick_previous);

        // Update
        game_update(frame_time);
    }
    SDL_Quit();
    return EXIT_SUCCESS;
}
