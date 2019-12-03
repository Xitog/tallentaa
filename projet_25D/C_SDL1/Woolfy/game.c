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
    {1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
};

const int TEXTURE_WIDTH = 32;
const int TEXTURE_HEIGHT = 32;
SDL_Surface * TEXTURES[10];

// retro calc 1/3
double dirX = -1, dirY = 0;
double planeX = 0, planeY = 0.66;
double column_width = 0;

//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------

void game_init(void) {
    printf("Game started\n");
    player.x = 2.2;
    player.y = 4.2; //1.2;
    player.a = 180;
    player.cos_a = cos(player.a * D2R);
    player.sin_a = -sin(player.a * D2R);
    player.fov = 66;
    column_width = 1 / screen->w;
    info();
}

// X = rouge
// Y = jaune

double final_distances[640];

int START_SCREEN = 380; // 0; //380;
int FPS_SCREEN_HEIGHT = 100; //screen->h; //100;
bool debug = true;

void game_raycast(void) {
    for(int x = 0; x < screen->w; x++) {
        double factor = ((float) x / screen->w) * 2 - 1;
        
        double camVectorX = - player.sin_a * 0.66 * factor;
        double camVectorY = player.cos_a * 0.66 * factor;

        double vectorRayX = player.cos_a - player.sin_a * 0.66 * factor;
        double vectorRayY = player.sin_a + player.cos_a * 0.66 * factor;
        if (vectorRayX > 0 && vectorRayX < 0.00000001) vectorRayX = 0;
        if (vectorRayY > 0 && vectorRayY < 0.00000001) vectorRayY = 0;
        if (vectorRayX < 0 && vectorRayX > -0.00000001) vectorRayX = 0;
        if (vectorRayY < 0 && vectorRayY > -0.00000001) vectorRayY = 0;
        
        double x2 = player.x + vectorRayX;
        double y2 = player.y + vectorRayY;
        int mapX2 = (int) x2;
        int mapY2 = (int) y2;
        int player_xi = (int) player.x;
        int player_yi = (int) player.y;
        
        int dirX = 1;
        int dirY = 1;
        if (vectorRayX < 0) dirX = -1; 
        if (vectorRayY < 0) dirY = -1;
        
        double final_x = 0;
        double final_y = 0;
        double final_d = 0;
        double final_w = 0; // where we hit the wall
        int tex = 0;

        if (vectorRayX != 0 && vectorRayY != 0) {
            // y = a * x + b
            double a = (y2 - player.y) / (x2 - player.x);
            double b = player.y - a * player.x;

            // crossColumn
            double crossColumn_x = dirX > 0 ? player_xi + dirX : player_xi;
            double crossColumn_y = crossColumn_x * a + b;
            int crossColumn_xi = player_xi + dirX;
            int crossColumn_yi = (int) crossColumn_y;
            double crossColumn_d = sqrt(pow(crossColumn_x - player.x, 2) + pow(crossColumn_y - player.y, 2));

            // crossLine
            double crossLine_y = dirY > 0 ? player_yi + dirY : player_yi;
            double crossLine_x = (crossLine_y - b) / a;
            int crossLine_xi = (int) crossLine_x;
            int crossLine_yi = player_yi + dirY;
            double crossLine_d = sqrt(pow(crossLine_x - player.x, 2) + pow(crossLine_y - player.y, 2));
            
            // applied vector ray (try)
            double vectorCameraPlaneNorme_x = player.sin_a;
            double vectorCameraPlaneNorme_y = - player.cos_a;
            double crossCameraPlane_x = player.x + vectorRayX;
            double crossCameraPlane_y = player.y + vectorRayY;
            double lenOnCameraPlane = fabs(0.66*factor);
            double diffAngleRayPlayer = atan(lenOnCameraPlane);

            bool hit = false;
            while (!hit) {
                if (crossLine_d < crossColumn_d) {
                    while (crossLine_d < crossColumn_d) {
                        if (map[crossLine_yi][crossLine_xi] > 0) {
                            tex = map[crossLine_yi][crossLine_xi];
                            hit = 1;
                            final_x = crossLine_x;
                            final_y = crossLine_y;
                            final_d = fabs(cos(diffAngleRayPlayer) * crossLine_d);
                            final_w = final_x;
                            break;
                        } else {
                            crossLine_y += dirY;
                            crossLine_x = (crossLine_y - b) / a;
                            crossLine_xi = (int) crossLine_x;
                            crossLine_yi += dirY;
                            crossLine_d = sqrt(pow(crossLine_x - player.x, 2) + pow(crossLine_y - player.y, 2));
                        }
                    }
                    //line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) (crossColumn_x * FACTOR), (int) (crossColumn_y * FACTOR), RED); 
                    //line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) (crossLine_x * FACTOR), (int) (crossLine_y * FACTOR), YELLOW); 
                } else {
                    while (crossLine_d >= crossColumn_d) {
                        if (map[crossColumn_yi][crossColumn_xi] > 0) {
                            tex = map[crossColumn_yi][crossColumn_xi];
                            hit = 1;
                            final_x = crossColumn_x;
                            final_y = crossColumn_y;
                            final_d = fabs(cos(diffAngleRayPlayer) * crossColumn_d);
                            final_w = final_y;
                            break;
                        } else {
                            crossColumn_x += dirX;
                            crossColumn_y = crossColumn_x * a + b;
                            crossColumn_xi += dirX;
                            crossColumn_yi = (int) crossColumn_y;
                            crossColumn_d = sqrt(pow(crossColumn_x - player.x, 2) + pow(crossColumn_y - player.y, 2));
                        }
                    }
                    //line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) (crossLine_x * FACTOR), (int) (crossLine_y * FACTOR), YELLOW); 
                    //line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) (crossColumn_x * FACTOR), (int) (crossColumn_y * FACTOR), RED);
                }
            }
            // debug
            if (final_d == 0) {
                printf("OUPS\n");
                printf("%d\n", x);
                printf("%f\n", vectorRayX);
                printf("%f\n", vectorRayY);
                printf("%f\n", crossLine_d);
                printf("%f\n", crossColumn_d);
                printf("%f\n", (crossLine_xi - player_xi) / vectorRayY);
                printf("%f\n", (crossColumn_xi - player_xi) / vectorRayX);
                //system("pause");
            }
        } else if (vectorRayY == 0) {
            bool hit = false;
            int crossColumn_xi = player_xi;
            while (!hit) {
                crossColumn_xi += dirX;
                if (map[player_yi][crossColumn_xi] > 0) {
                    tex = map[player_yi][crossColumn_xi];
                    hit = true;
                }
            }
            final_x = dirX > 0 ? crossColumn_xi : crossColumn_xi + 1;
            final_y = player.y;
            final_d = sqrt(pow(final_x - player.x, 2) + pow(final_y - player.y, 2));
            final_w = final_y;
        } else if (vectorRayX == 0) {
            bool hit = false;
            int crossLine_yi = player_yi;
            while (!hit) {
                crossLine_yi += dirY;
                if (map[crossLine_yi][player_xi] > 0) {
                    tex = map[crossLine_yi][player_xi];
                    hit = true;
                }
            }
            final_x = dirY > 0 ? crossLine_yi : crossLine_yi + 1;
            final_y = player.x;
            final_d = sqrt(pow(final_x - player.x, 2) + pow(final_y - player.y, 2));
            final_w = final_x;
        }

        Uint32 color;
        switch (tex) {
            case 1:
                color = BLUE;
                break;
            case 2:
                color = RED;
                break;
            case 3:
                color = YELLOW;
                break;
        }

        if (debug) {
            line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) (final_x * FACTOR), (int) (final_y * FACTOR), color);
        }

        // 2.5D
        final_distances[x] = final_d;
        int column_height = (int) (FPS_SCREEN_HEIGHT / final_d);
        //if (d > FPS_SCREEN_HEIGHT) d = FPS_SCREEN_HEIGHT;
        //if (d < 0) d = 0;
        int column_start = START_SCREEN + FPS_SCREEN_HEIGHT / 2 - (int) (column_height / 2);
        int column_end = START_SCREEN + FPS_SCREEN_HEIGHT / 2 + (int) (column_height / 2);
        for (int s = column_start ; s <= column_end ; s++) {
            if (s >= START_SCREEN && s < screen->h) {
                int col_tex = (final_w - (int) final_w) * (TEXTURE_WIDTH - 1);
                int lin_tex = ((s - column_start) / (float) column_height) * (TEXTURE_HEIGHT - 1);
                //printf("%d\n", col_tex);
                Uint32 c = get_pixel(TEXTURES[0], col_tex, lin_tex);
                set_pixel(x, s, c);
            }
        }
        //line(x, START_SCREEN + FPS_SCREEN_HEIGHT / 2 - (int) (d / 2), x, START_SCREEN + FPS_SCREEN_HEIGHT / 2 + (int) (d / 2), color);

        for(int yy = 0; yy < TEXTURE_HEIGHT; yy++) {
            for (int xx = 0; xx < TEXTURE_WIDTH; xx++) {
                Uint32 c = get_pixel(TEXTURES[0], xx, yy);
                set_pixel(xx, yy, c);
            }
        }
    }
}

void game_raycast2(void) {
    for(int x = 0; x < screen->w; x++) {

        //float factor = ((float) x / screen->w) * 2 - 1;
        float factor = 1;
        float vectorRayX = player.cos_a + player.sin_a * 0.66 * factor;
        float vectorRayY = player.sin_a + player.cos_a * 0.66 * factor;
        int mapJustInFrontX = (int) (player.cos_a * 0.1 + player.sin_a * 0.66 * factor);
        int mapJustInFrontY = (int) (player.sin_a * 0.1 + player.cos_a * 0.66 * factor);

        // rayX et rayY
        //float vectorRayX = player.cos_a;
        //float vectorRayY = player.sin_a;
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
        if (map[mapRayY][mapRayX] > 0 || map[mapJustInFrontY][mapJustInFrontX] > 0) {
            hit = true;
        }
        float dist = 0;
        while (!hit) {
            if (dirRayX == 0 && dirRayY == 0) {
                printf("[ERROR] Ray without direction.");
                break;
            }
            if (dist2nextX < dist2nextY || dirRayY == 0) {
                mapRayX += dirRayX;
                dist2nextX += hypoRayX;
                dist += hypoRayX;
            } else {
                mapRayY += dirRayY;
                dist2nextY += hypoRayY;
                dist += hypoRayY;
            }
            if (map[mapRayY][mapRayX] > 0) {
                hit = true;
            }
        }
        
        int xx = mapRayX;
        int yy = mapRayY;
        line((int) (player.x * FACTOR), (int) (player.y * FACTOR), xx * FACTOR + FACTOR / 2, yy * FACTOR + FACTOR / 2, RED);       
    }

    line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) ((player.x + player.cos_a) * FACTOR), (int) ((player.y + player.sin_a) * FACTOR), WHITE);
    
    line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) ((player.x + player.cos_a - player.sin_a * 0.66) * FACTOR), (int) ((player.y + player.sin_a + player.cos_a * 0.66) * FACTOR), YELLOW);
    line((int) (player.x * FACTOR), (int) (player.y * FACTOR), (int) ((player.x + player.cos_a + player.sin_a * 0.66) * FACTOR), (int) ((player.y + player.sin_a - player.cos_a * 0.66) * FACTOR), YELLOW);
}

void game_draw(void) {
    
    fill(BLACK);

    rect(0, START_SCREEN, screen->w, FPS_SCREEN_HEIGHT / 2, CEILGREY, true);
    rect(0, START_SCREEN + FPS_SCREEN_HEIGHT / 2, screen->w, FPS_SCREEN_HEIGHT / 2, FLOORGREY, true);

    if (debug) {
        // Grid
        for (int row = 0; row < MAP_HEIGHT; row++) {
            for (int col = 0; col < MAP_WIDTH; col++) {
                if (map[row][col] > 0) {
                    Uint32 color;
                    switch (map[row][col]) {
                        case 1:
                            color = BLUE;
                            break;
                        case 2:
                            color = RED;
                            break;
                        case 3:
                            color = YELLOW;
                            break;
                    }
                    rect(col * FACTOR, row * FACTOR, FACTOR, FACTOR, color, true);
                }
                rect(col * FACTOR, row * FACTOR, FACTOR, FACTOR, WHITE, false);
            }
        }
        // Player
        rect((player.x * FACTOR) - 2, (player.y * FACTOR) - 2, 5, 5, WHITE, false);
        // Div
        line(0, START_SCREEN, screen->w-1, START_SCREEN, RED);
    }

    game_raycast();
}

void info(void) {
    printf("-------------------------\n");
    printf("MATH.PI     = %f\n", M_PI);
    printf("angle (deg) = %f\n", player.a);
    printf("angle (rad) = %f\n", player.a / 180 * M_PI);
    printf("dirX        = %f   retroDirX = %f\n", player.cos_a, dirX);
    printf("dirY        = %f   retroDirY = %f\n", player.sin_a, dirY);
    printf("fovX        = %f  retroPlaneX = %f\n", player.sin_a * 0.66, planeX);
    printf("fovY        = %f  retroPlaneY = %f\n", player.cos_a * 0.66, planeY);
    printf("mapX        = %d\n", (int) player.x);
    printf("mapY        = %d\n", (int) player.y);
    float vectorRayX = player.cos_a + player.sin_a * 0.66;
    float vectorRayY = player.sin_a + player.cos_a * 0.66;
    printf("vectorRayX  = %f\n", vectorRayX);
    printf("vectorRayY  = %f\n", vectorRayY);
    printf("mapRayX     = %d\n", (int) (vectorRayX + player.x));
    printf("mapRayY     = %d\n", (int) (vectorRayY + player.y));
}

bool load_use = false;
bool load_jump = false;
bool load_fire = false;

void game_update(double frame_time) {
    float old_x = player.x;
    float old_y = player.y;
    bool print = false;

    if (action_state[A_FIRE]) {
        load_fire = true;
    } else if (load_fire) {
        load_fire = false;
        if (!debug) {
            debug = true;
            START_SCREEN = 380;
            FPS_SCREEN_HEIGHT = 100;
        } else {
            debug = false;
            START_SCREEN = 0;
            FPS_SCREEN_HEIGHT = screen->h;
        }
    }

    if (action_state[A_JUMP]) {
        load_jump = true;
    } else if (load_jump) {
        load_jump = false;
        FILE * f = fopen("dump.txt", "w");
        fprintf(f, "player.x     = %f\n", player.x);
        fprintf(f, "player.y     = %f\n", player.y);
        fprintf(f, "player.a     = %f\n", player.a);
        fprintf(f, "player.cos_a = %f\n", player.cos_a);
        fprintf(f, "player.sin_a = %f\n", player.sin_a);
        fprintf(f, "Col Dist    Height\n");
        for (int i=0; i < screen->w; i++) {
            int d = (int) (100 / final_distances[i]);
            fprintf(f, "%.3d. %f %d\n", i, final_distances[i], d);
        }
        fclose(f);
    }

    if (action_state[A_USE]) {
        load_use = true;
    } else if (load_use) {
        load_use = false;
        if (player.a == 90 || player.a == 180 || player.a == 270 || player.a == 0) {
            player.a += 90;
            if (player.a >= 360) {
                player.a -= 360;
            }
        } else {
            player.a = 180;
        }
        player.cos_a = cos(player.a * D2R);
        player.sin_a = -sin(player.a * D2R);
        printf("use\n");
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
        } else if (player.a >= 360) {
            player.a -= 360;
        }
        player.cos_a = cos(player.a * D2R);
        player.sin_a = -sin(player.a * D2R);
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
        player.sin_a = -sin(player.a * D2R);
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

    if (map[(int)player.y][(int)player.x] > 0) {
        player.x = old_x;
        player.y = old_y;
    }

    if (player.x < 0) player.x = 0;
    if (player.y < 0) player.y = 0;
}
