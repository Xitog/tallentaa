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
const float M_PI = 3.14159265358979323846;

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

// retro calc 1/3
double dirX = -1, dirY = 0;
double planeX = 0, planeY = 0.66;

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

void game_init(void) {
    printf("Game started\n");
    player.x = 2.2;
    player.y = 1.2;
    player.a = 180;
    player.cos_a = cos(player.a * D2R);
    player.sin_a = sin(player.a * D2R);
    player.fov = 66;
    info();
}

void game_raycast(void) {
    for(int x = 0; x < screen->w; x+=100) {
        // rayX et rayY
        float vectorRayX = player.cos_a;
        float vectorRayY = player.sin_a;
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
    
            /*
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
            */

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
        /*
        printf("---------\n");
        printf("VectorRayX  = %f\n", vectorRayX);
        printf("VectorRayY  = %f\n", vectorRayY);
        printf("AppliedRayX = %f\n", appliedRayX);
        printf("AppliedRayY = %f\n", appliedRayY);
        */


        /*if (dirRayX > 0) {
            xx -= 1;
        }
        
        if (dirRayY > 0) {
            yy -= 1;
        }*/
        
        //printf("%d %d\n", xx, yy);
        // dirX
        
        // 
        int xx = mapRayX;
        int yy = mapRayY;
        line((int) (player.x * FACTOR), (int) (player.y * FACTOR), xx * FACTOR + FACTOR / 2, yy * FACTOR + FACTOR / 2, RED);    
        
    }

    
    line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) ((player.x + player.cos_a) * FACTOR), (int) ((player.y + player.sin_a) * FACTOR), WHITE);
    
    line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) ((player.x + player.cos_a - player.sin_a * 0.66) * FACTOR), (int) ((player.y + player.sin_a + player.cos_a * 0.66) * FACTOR), YELLOW);
    line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) ((player.x + player.cos_a + player.sin_a * 0.66) * FACTOR), (int) ((player.y + player.sin_a - player.cos_a * 0.66) * FACTOR), YELLOW);

    // projected

    // Calc
    
    //float player_angle_deg = 180;
    //float player_angle_rad = player_angle_deg / 180 * M_PI;
    //float player_fov_deg = 66;
    //float player_fov_rad = player_fov_deg / 180 * M_PI;

    //float vectorProjX = player.sin_a;
    //float vectorProjY = player.cos_a;
    //float appliedRayX = player.x + player.cos_a;
    //float appliedRayY = player.y + player.sin_a;
    //float appliedProjX = player.x +  player.x + cos(player.a) + vectorProjX;
    //float appliedProjY = player.y +  player.y - sin(player.a) + vectorProjY;

    //line(appliedRayX * FACTOR, appliedRayY * FACTOR, (appliedRayX + vectorProjY) * FACTOR, (appliedRayY - vectorProjX) * FACTOR, YELLOW);
    //line(appliedRayX * FACTOR, appliedRayY * FACTOR, (appliedRayX - vectorProjY) * FACTOR, (appliedRayY + vectorProjX) * FACTOR, YELLOW);
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

void info(void) {
    printf("MATH.PI     = %f\n", M_PI);
    printf("angle (deg) = %f\n", player.a);
    printf("angle (rad) = %f\n", player.a / 180 * M_PI);
    printf("dirX        = %f   retroDirX = %f\n", player.cos_a, dirX);
    printf("dirY        = %f   retroDirY = %f\n", player.sin_a, dirY);
    printf("fovX         = %f  retroPlaneX = %f\n", player.sin_a * 0.66, planeX);
    printf("fovY         = %f  retroPlaneY = %f\n", player.cos_a * 0.66, planeY);
}

void game_update(double frame_time) {
    float old_x = player.x;
    float old_y = player.y;
    bool print = false;

    if (action_state[A_USE]) {

    }
    if (action_state[A_MOVE_FORWARD]) {
        player.x += player.cos_a * move_modifier * frame_time;
        player.y += player.sin_a * move_modifier * frame_time;
    }
    if (action_state[A_MOVE_BACKWARD]) {
        player.x -= player.cos_a * move_modifier * frame_time;
        player.y -= player.sin_a * move_modifier * frame_time;
    }
    if (action_state[A_STRAFE_LEFT]) {
        player.x += player.sin_a * move_modifier * frame_time;
        player.y -= player.cos_a * move_modifier * frame_time;
    }
    if (action_state[A_STRAFE_RIGHT]) {
        player.x -= player.sin_a * move_modifier * frame_time;
        player.y += player.cos_a * move_modifier * frame_time;
    }
    if (action_state[A_TURN_LEFT]) {
        player.a += turn_modifier * 180 / M_PI * frame_time;
        if (player.a < 0) {
            player.a += 360;
        } else if (player.a > 360) {
            player.a -= 360;
        }
        player.cos_a = cos(player.a * D2R);
        player.sin_a = sin(player.a * D2R);
        // retro calc 2
        double oldDirX = dirX;
        dirX = dirX * cos(turn_modifier * frame_time) - dirY * sin(turn_modifier * frame_time);
        dirY = oldDirX * sin(turn_modifier * frame_time) + dirY * cos(turn_modifier * frame_time);
        double oldPlaneX = planeX;
        planeX = planeX * cos(turn_modifier * frame_time) - planeY * sin(turn_modifier * frame_time);
        planeY = oldPlaneX * sin(turn_modifier * frame_time) + planeY * cos(turn_modifier * frame_time);
        print = true;
    }
    if (action_state[A_TURN_RIGHT]) {
        player.a -= turn_modifier * 180 / M_PI * frame_time;
        if (player.a < 0) {
            player.a += 360;
        } else if (player.a > 360) {
            player.a -= 360;
        }
        player.cos_a = cos(player.a * D2R);
        player.sin_a = sin(player.a * D2R);
        // retro calc 3
        double oldDirX = dirX;
        dirX = dirX * cos(-turn_modifier * frame_time) - dirY * sin(-turn_modifier * frame_time);
        dirY = oldDirX * sin(-turn_modifier * frame_time) + dirY * cos(-turn_modifier * frame_time);
        double oldPlaneX = planeX;
        planeX = planeX * cos(-turn_modifier * frame_time) - planeY * sin(-turn_modifier * frame_time);
        planeY = oldPlaneX * sin(-turn_modifier * frame_time) + planeY * cos(-turn_modifier * frame_time);
        print = true;
    }
    
    if (print) {
        info();
    }

    if (map[(int)player.y][(int)player.x] == 1) {
        player.x = old_x;
        player.y = old_y;
    }

    if (player.x < 0) player.x = 0;
    if (player.y < 0) player.y = 0;
}
