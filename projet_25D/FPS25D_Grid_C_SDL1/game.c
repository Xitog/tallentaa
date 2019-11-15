//-----------------------------------------------------------------------------
// Include
//-----------------------------------------------------------------------------

#include "game.h"

//-----------------------------------------------------------------------------
// Global variable
//-----------------------------------------------------------------------------

Player player;

Uint32 x = 0;
Uint32 drawStart = 0;
Uint32 drawEnd = 0;
Uint32 color = RED;

double move_modifier = 0.004;
double turn_modifier = 0.002;
double col = 0.0;
double height = 0.0;

const float D2R = 0.01745329252;
const int FACTOR = 32;

const int MAP_WIDTH = 18;
const int MAP_HEIGHT = 12;
const Uint32 map[12][18] = {
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
};

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

void game_init(void) {
    printf("Game started\n");
    player.x = 2.2;
    player.y = 1.2;
    player.a = 0;
}

void game_raycast(void) {
    for(int x = 0; x < screen->w; x+=100) {
        // rayX et rayY
        float vectorRayX = cos(player.a);
        float vectorRayY = - sin(player.a);
        float appliedRayX = player.x + vectorRayX;
        float appliedRayY = player.y + vectorRayY;
        int mapRayX = (int) appliedRayX;
        int mapRayY = (int) appliedRayY;
    
        // Hypo X et Y
        float hypoRayX = 0.0;
        if (vectorRayX != 0) {
            hypoRayX = fabs(1 / vectorRayX);
        }
        float hypoRayY = 0.0;
        if (vectorRayY != 0) {
            hypoRayY = fabs(1 / vectorRayY);
        }
        
        // Sens de rayX et rayY
        int dirRayX = 0;
        int dirRayY = 0;
    
        if (vectorRayX > 0) {
            dirRayX = 1;
        } else if (vectorRayX < 0) {
            dirRayX = -1;
        }
        if (vectorRayY > 0) {
            dirRayY = 1;
        } else if (vectorRayY < 0) {
            dirRayY = -1;
        }
        
        // Distance next
        float dist2nextX = 0;
        float dist2nextY = 0;
    
        if (dirRayX > 0) {
            dist2nextX = (1 + ((int) appliedRayX) - appliedRayX) * hypoRayX;
        } else {
            dist2nextX = (appliedRayX - ((int) appliedRayX)) * hypoRayX;
        }
        if (dirRayY > 0) {
            dist2nextY = (1 + ((int) appliedRayY) - appliedRayY) * hypoRayY;
        } else {
            dist2nextY = (appliedRayY - ((int) appliedRayY)) * hypoRayY;
        }
        
        // Next case
        bool hit = false;
        while (!hit) {
    
            printf("---------\n");
    
            printf("Dir and adding to map coordinates\n");
            printf("dirRayX     = %d\n", dirRayX);
            printf("dirRayY     = %d\n", dirRayY);
    
            printf("dist2nextX  = %f\n", dist2nextX);
            printf("dist2nextY  = %f\n", dist2nextY);
    
            printf("Adding to dist2next\n");
            printf("HypoRayX    = %f\n", hypoRayX);
            printf("HypoRayY    = %f\n", hypoRayY);
    
            printf("mapRayX     = %d\n", mapRayX);
            printf("mapRayY     = %d\n", mapRayY);
    
            if (dirRayX == 0 && dirRayY == 0) {
                printf("[ERROR] Ray without direction.");
                break;
            }
            if (dist2nextX < dist2nextY || dirRayY == 0) {
                mapRayX += dirRayX;
                dist2nextX += hypoRayX;
            } else {
                mapRayY += dirRayY;
                dist2nextY += hypoRayY;
            }
            if (map[mapRayY][mapRayX] > 0) {
                hit = true;
            }
        }

        // Print

        printf("---------\n");
        printf("VectorRayX  = %f\n", vectorRayX);
        printf("VectorRayY  = %f\n", vectorRayY);
        printf("AppliedRayX = %f\n", appliedRayX);
        printf("AppliedRayY = %f\n", appliedRayY);
        
        int xx = mapRayX;
        if (dirRayX < 0) {
            xx += 1;
        }
        int yy = mapRayY;
        if (dirRayY < 0) {
            yy += 1;
        }
        
        printf("%d %d\n", xx, yy);
        line((int) (player.x * FACTOR), (int) (player.y * FACTOR), xx * FACTOR, yy * FACTOR, RED);
    }
    // projected
    float vectorProjX = sin(player.a);
    float vectorProjY = cos(player.a);
    float appliedRayX = player.x + cos(player.a);
    float appliedRayY = player.y - sin(player.a);
    //float appliedProjX = player.x +  player.x + cos(player.a) + vectorProjX;
    //float appliedProjY = player.y +  player.y - sin(player.a) + vectorProjY;
    line(appliedRayX * FACTOR, appliedRayY * FACTOR, (appliedRayX + vectorProjX) * FACTOR, (appliedRayY + vectorProjY) * FACTOR, YELLOW);
    line(appliedRayX * FACTOR, appliedRayY * FACTOR, (appliedRayX - vectorProjX) * FACTOR, (appliedRayY - vectorProjY) * FACTOR, YELLOW);
}

void game_draw(void) {

    fill(BLACK);

    // Grid
    for (int row = 0; row < MAP_HEIGHT; row++) {
        for (int col = 0; col < MAP_WIDTH; col++) {
             if (map[row][col] == 1) {
                SDL_Rect r;
                r.x = col * FACTOR;
                r.y = row * FACTOR;
                r.w = FACTOR;
                r.h = FACTOR;
                SDL_FillRect(screen, &r, BLUE);
            }
            rect(col * FACTOR, row * FACTOR, FACTOR, FACTOR, WHITE);
        }
    }

    // Player
    rect((player.x * FACTOR) - 2, (player.y * FACTOR) - 2, 5, 5, WHITE);

    game_raycast();

    /*for (Uint32 i = 0; i <= x; i++) {
        vertical(i, drawStart, drawEnd, color);
    }*/

}

void game_update(double frame_time) {
    float old_x = player.x;
    float old_y = player.y;

    if (action_state[A_MOVE_FORWARD]) {
        player.x += cos(player.a) * move_modifier * frame_time;
        player.y -= sin(player.a) * move_modifier * frame_time;
    }
    if (action_state[A_MOVE_BACKWARD]) {
        player.x -= cos(player.a) * move_modifier * frame_time;
        player.y += sin(player.a) * move_modifier * frame_time;
    }
    if (action_state[A_STRAFE_LEFT]) {
        player.x += sin(player.a) * move_modifier * frame_time;
        player.y -= cos(player.a) * move_modifier * frame_time;
    }
    if (action_state[A_STRAFE_RIGHT]) {
        player.x -= sin(player.a) * move_modifier * frame_time;
        player.y += cos(player.a) * move_modifier * frame_time;
    }
    if (action_state[A_TURN_LEFT]) {
        player.a += turn_modifier * frame_time;
    }
    if (action_state[A_TURN_RIGHT]) {
        player.a -= turn_modifier * frame_time;
    }
    
    if (map[(int)player.y][(int)player.x] == 1) {
        player.x = old_x;
        player.y = old_y;
    }

    if (player.x < 0) player.x = 0;
    if (player.y < 0) player.y = 0;
}
