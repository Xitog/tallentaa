//-----------------------------------------------------------------------------
// Include
//-----------------------------------------------------------------------------

#include <stdio.h>
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

int main(int argc, char * argv[]) {
    
    int err = init("Woolfy 2.5 FLAT", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }
    
    printf("%d\n", sizeof(*screen)); // 60
    printf("%d\n", sizeof(*(screen->format))); // 40
    printf("PixelFormat.BytesPexPixel = %d\n", screen->format->BytesPerPixel); // 4
    printf("Surface.Pitch = %d\n", screen->pitch); // 2560

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
