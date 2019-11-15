#ifndef GAME_H
#define GAME_H

//-----------------------------------------------------------------------------
// Include
//-----------------------------------------------------------------------------

#include <stdio.h>
#include <math.h>
#include "sdl.h"
#include "draw.h"
#include "event.h"

//-----------------------------------------------------------------------------
// Type
//-----------------------------------------------------------------------------

typedef struct {
    float x;
    float y;
    float a;
    double cos_a;
    double sin_a;
    double fov;
} Player;

//-----------------------------------------------------------------------------
// Global variable
//-----------------------------------------------------------------------------

extern Player player;
extern const int MAP_WIDTH;
extern const int MAP_HEIGHT;
extern const Uint32 map[12][18];


//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

void game_draw(void);

void game_init(void);

void game_update(double frame_time);

void info(void);

#endif
