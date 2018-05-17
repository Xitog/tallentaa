
#ifdef FLAT_NOGRID

//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <math.h>
#include <io.h>
#include "SDL.h"
#include "minisdl.h"

//-----------------------------------------------------------------------------
// Type definitions
//-----------------------------------------------------------------------------

typedef struct {
    double x;
    double y;
    double z;
} Vector;

typedef struct {
    Vector pos;
    Vector dir;
} Player;

typedef enum {
    VERTICAL = 0,
    HORIZONTAL = 1,
} WallType;

typedef struct {
    Vector pos1;
    Vector pos2;
    WallType type;
    int color;
} Wall;

typedef struct {
    Vector pos;
    Wall wall;
    double dist;
} Intersection;

typedef enum {
    WHITE_COLOR = 1,
    YELLOW_COLOR = 2,
    BLUE_COLOR = 3,
    RED_COLOR = 4,
    GREEN_COLOR = 5,
} Colors;

//-----------------------------------------------------------------------------
// Global constants
//-----------------------------------------------------------------------------

const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;

const Intersection NO_INTERSECTION = { 
    {-1, -1, -1}, // pos
    { {-1, -1, -1}, {-1, -1, -1}, 0, 0}, // wall
    -1 // dist
};

#define DEF_MAX_WALL 4

const int MAX_WALL = DEF_MAX_WALL;
const Wall map[DEF_MAX_WALL] = {
    {
        {1, 1, 0},      // pos 1
        {10, 1, 0},     // pos 2
        HORIZONTAL,     // sens
        WHITE_COLOR,    // color
    },
    {
        {1, 1, 0},
        {1, 10, 0},
        VERTICAL,
        BLUE_COLOR,
    },
    {
        {1, 10, 0},
        {10, 10, 0},
        HORIZONTAL,
        YELLOW_COLOR,
    },
    {
        {10, 1, 0},
        {10, 10, 0},
        VERTICAL,
        GREEN_COLOR,
    }
};

const double MOVE_SPEED = 0.008;
const double ROT_SPEED = 0.002;

const int MINIMAP_ZOOM = 20;

//-----------------------------------------------------------------------------
// Global variables
//-----------------------------------------------------------------------------

bool down;
bool up;
bool right;
bool left;
bool done = false;
bool show_map = true;
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
                    show_map = !show_map;
                    break;
                case SDLK_SPACE:
                    pause = !pause;
                    break;
            }
       } else if (event.type == SDL_QUIT ) {
            done = true;
       }
    }
}

Intersection intersection(Vector ray, Vector pos, Wall wall) {
    //printf("    Ray direction : %.2f, %.2f\n", ray.x, ray.y);
    //printf("    Origin position : %.2f, %.2f\n", pos.x, pos.y);
    //printf("    Wall : Pos1 = %.2f, %.2f, Pos2 = %.2f, %.2f and Type = %d and Color = %d\n", wall.pos1.x, wall.pos1.y, wall.pos2.x, wall.pos2.y, wall.type, wall.color);
    Vector ray_on_pos;
    ray_on_pos.x = ray.x + pos.x;
    ray_on_pos.y = ray.y + pos.y;
    //printf("    Intersection called with:\n");
    //printf("        ray X = %f Y = %f\n", ray.x, ray.y);
    //printf("        ray_on_pos X = %f Y = %f\n", ray_on_pos.x, ray_on_pos.y);
    if (wall.type == HORIZONTAL) {
        if (ray.y == 0) {
            //printf("    HORIZONTAL NO INTERSECTION PARALLEL\n");
            return NO_INTERSECTION;
        } else if (ray.y > 0 && wall.pos2.y < pos.y) {
            //printf("    HORIZONTAL NO INTERSECTION WALL NEVER ENCOUNTERED\n");
            return NO_INTERSECTION;
        } else if (ray.y < 0 && wall.pos1.y > pos.y) {
            //printf("    HORIZONTAL NO INTERSECTION WALL NEVER ENCOUNTERED\n");
            return NO_INTERSECTION;
        } else if (ray.x == 0) { // perpendicular to wall
            Intersection coll;
            coll.pos.x = ray_on_pos.x;
            coll.pos.y = wall.pos1.y;
            coll.pos.z = 0;
            coll.wall = wall;
            coll.dist = fabs(pos.y - wall.pos1.y);
            //printf("    HORIZONTAL PERPENDICULAR INTERSECTION AT %.2f, %.2f\n", coll.pos.x, coll.pos.y);
            return coll;
        } else {
            Intersection coll;
            // calc
            double A = ray.y / ray.x;
            double B = ray_on_pos.y - A * ray_on_pos.x;
            //printf("    HORIZONTAL WALL (%d) and RAY Y = %f * X + %f\n", wall.type, A, B);
            double coll_x = (wall.pos1.y - B) / A;
            //printf("    INTERSECT AT : %f %f\n", coll_x, wall.pos1.y);
            if (coll_x >= wall.pos1.x && coll_x <= wall.pos2.x) {
                coll.pos.x = coll_x;
                coll.pos.y = wall.pos1.y;
                coll.pos.z = 0;
                coll.wall = wall;
                coll.dist = sqrt(pow(coll.pos.x - pos.x, 2) + pow(coll.pos.y - pos.y, 2));
                return coll;
            } else {
                return NO_INTERSECTION;
            }
        }
    } else if (wall.type == VERTICAL) {
        if (ray.x == 0) {
            //printf("    VERTICAL NO INTERSECTION PARALLEL\n");
            return NO_INTERSECTION;
        } else if (ray.x > 0 && wall.pos2.x < pos.x) {
            //printf("    VERTICAL NO INTERSECTION WALL NEVER ENCOUNTERED\n");
            return NO_INTERSECTION;
        } else if (ray.x < 0 && wall.pos1.x > pos.x) {
            //printf("    VERTICAL NO INTERSECTION WALL NEVER ENCOUNTERED\n");
            return NO_INTERSECTION;
        } else if (ray.y == 0) { // perpendicular to wall
            Intersection coll;
            coll.pos.x = wall.pos1.x;
            coll.pos.y = ray_on_pos.y;
            coll.pos.z = 0;
            coll.wall = wall;
            //printf("        >>> %f %f = %f\n", pos.x, wall.pos1.x, fabs(pos.x - wall.pos1.x));
            coll.dist = fabs(pos.x - wall.pos1.x);
            //printf("        VERTICAL PERPENDICULAR INTERSECTION AT %.2f, %.2f\n", coll.pos.x, coll.pos.y);
            return coll;
        } else {
            Intersection coll;
            // calc
            double A = ray.y / ray.x;
            double B = ray_on_pos.y - A * ray_on_pos.x;
            //printf("        VERTICAL WALL (%d) and RAY Y = %f * X + %f\n", wall.type, A, B);
            double coll_y = A * wall.pos1.x + B;
            //printf("        INTERSECT AT : X = %f Y = %f. Y should be between %f %f\n", wall.pos1.x, coll_y, wall.pos1.y, wall.pos2.y);
            if (coll_y >= wall.pos1.y && coll_y <= wall.pos2.y) {
                coll.pos.x = wall.pos1.x;
                coll.pos.y = coll_y;
                coll.pos.z = 0;
                coll.wall = wall;
                coll.dist = sqrt(pow(coll.pos.x - pos.x, 2) + pow(coll.pos.y - pos.y, 2));
                return coll;
            } else {
                return NO_INTERSECTION;
            }
        }
    } else {
        return NO_INTERSECTION;
    }
}

int main(int argc, char * argv[]) {
    printf("Start\n");

    // Player
    Player player = {{5.5, 5.5, 0}, {-1, 0, 0}};
    Vector camera = {0, 0.66, 0};
    Vector next_pos = {0, 0, 0};

    // Time
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;

    // Moves
    double move_modifier = MOVE_SPEED;
    double rot_modifier = ROT_SPEED;

    // Init and screen
    int err = init("Woolfy 2.5 FLAT NO GRID", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
    if (err == EXIT_FAILURE) {
        return err;
    }

    // Colors
    Uint32 RED = SDL_MapRGB(screen->format, 255, 0, 0);
    Uint32 GREEN = SDL_MapRGB(screen->format, 0, 255, 0);
    Uint32 BLUE = SDL_MapRGB(screen->format, 0, 0, 255);
    Uint32 BLACK = SDL_MapRGB(screen->format, 0, 0, 0);
    Uint32 YELLOW = SDL_MapRGB(screen->format, 255, 255, 0);
    Uint32 WHITE = SDL_MapRGB(screen->format, 255, 255, 255);
    Uint32 PURPLE = SDL_MapRGB(screen->format, 128, 64, 128);
    
    // Check wall
    for (int i=0; i < MAX_WALL; i++) {
        if (map[i].pos1.x > map[i].pos2.x) {
            printf("ERROR: pos2.x > pos1.x\n");
        }
        if (map[i].pos1.y > map[i].pos2.y) {
            printf("ERROR: pos2.y > pos1.y\n");
        }
        if (map[i].pos1.x == map[i].pos2.x && map[i].type != VERTICAL) {
            printf("ERROR: Should be VERTICAL\n");
        }
        if (map[i].pos1.y == map[i].pos2.y && map[i].type != HORIZONTAL) {
            printf("ERROR: Should be HORIZONTAL\n");
        }
    }

    // Main loop
    while(!done) {

        Intersection intersections[SCREEN_WIDTH];
        
        // Rendering
        fill(BLACK);
        
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            intersections[x].dist = 1000;
            double raycast_cpt = 2 * x / (float) SCREEN_WIDTH - 1; // -1 to +1
            Vector ray;
            ray.x = player.dir.x + camera.x * raycast_cpt;
            ray.y = player.dir.y + camera.y * raycast_cpt;
            for (int i=0; i < MAX_WALL; i++) {
                Intersection inter = intersection(ray, player.pos, map[i]);
                if (inter.dist < intersections[x].dist && inter.dist > -1) {
                    intersections[x] = inter;
                }
            }
        }
        

        /*
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            intersections[x].dist = 1000;
        }
        
        Vector rays[3];
        rays[0] = player.dir;
        rays[1].x = player.dir.x + camera.x;
        rays[1].y = player.dir.y + camera.y;
        rays[2].x = player.dir.x - camera.x;
        rays[2].y = player.dir.y - camera.y;

        for (int r=0; r < 1; r++) {
            printf("== Ray %d ==\n", r);
            printf("    X = %.2f Y = %.2f\n", rays[r].x, rays[r].y);
            for (int i=0; i < MAX_WALL; i++) {
                printf("    == Wall num %d (color %d) ==\n", i, map[i].color);
                Intersection inter = intersection(rays[r], player.pos, map[i]);
                printf("        Inter.dist = %.2f vs %2.f\n", inter.dist, intersections[r].dist);
                if (inter.dist < intersections[r].dist && inter.dist > -1) {
                    intersections[r] = inter;
                }
            }
        }
        */

        if (show_map) {
            // Draw rays
            for (int x = 0; x < SCREEN_WIDTH; x++) {
                if (intersections[x].dist == -1 || intersections[x].dist == 1000) {
                    continue;
                }
                //printf("%d. INTERSECT : %.2f\n", x, intersections[x].dist);
                if (intersections[x].dist != -1) {
                    Uint32 color;
                    switch (intersections[x].wall.color) {
                        case WHITE_COLOR:
                            color = WHITE;
                            break;
                        case RED_COLOR:
                            color = RED;
                            break;
                        case BLUE_COLOR:
                            color = BLUE;
                            break;
                        case YELLOW_COLOR:
                            color = YELLOW;
                            break;
                        case GREEN_COLOR:
                            color = GREEN;
                            break;
                        default:
                            color = PURPLE;
                            break;
                    }
                    line(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, intersections[x].pos.x * MINIMAP_ZOOM, intersections[x].pos.y * MINIMAP_ZOOM, color);
                }
            }
            // Draw player and camera
            circle(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, 5, WHITE);
            double pos_dir_x = player.pos.x + player.dir.x;
            double pos_dir_y = player.pos.y + player.dir.y;
            // cam left and right
            line(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, (pos_dir_x + camera.x) * MINIMAP_ZOOM, (pos_dir_y + camera.y) * MINIMAP_ZOOM, GREEN);
            line(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, (pos_dir_x - camera.x) * MINIMAP_ZOOM, (pos_dir_y - camera.y) * MINIMAP_ZOOM, RED);
            line((pos_dir_x + camera.x) * MINIMAP_ZOOM, (pos_dir_y + camera.y) * MINIMAP_ZOOM, (pos_dir_x - camera.x) * MINIMAP_ZOOM, (pos_dir_y - camera.y) * MINIMAP_ZOOM, PURPLE);
            // dir
            line(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, pos_dir_x * MINIMAP_ZOOM, pos_dir_y * MINIMAP_ZOOM, PURPLE);
            // Draw walls
            for (int i=0; i < MAX_WALL; i++) {
                Uint32 color;
                switch (map[i].color) {
                    case WHITE_COLOR:
                        color = WHITE;
                        break;
                    case RED_COLOR:
                        color = RED;
                        break;
                    case BLUE_COLOR:
                        color = BLUE;
                        break;
                    case YELLOW_COLOR:
                        color = YELLOW;
                        break;
                    case GREEN_COLOR:
                        color = GREEN;
                        break;
                    default:
                        color = PURPLE;
                        break;
                }
                line(map[i].pos1.x * MINIMAP_ZOOM, map[i].pos1.y * MINIMAP_ZOOM, map[i].pos2.x * MINIMAP_ZOOM, map[i].pos2.y * MINIMAP_ZOOM, color);
            }
        }
        render();
        
        //done = true;

        // Time and input
        input();
        tick_previous = tick_current;
        tick_current = SDL_GetTicks();
        frame_time = (tick_current - tick_previous);
        
        // Update
        if (up || down) {
            if (up) {
                next_pos.x = player.pos.x + player.dir.x * move_modifier * frame_time;
                next_pos.y = player.pos.y + player.dir.y * move_modifier * frame_time;
            }
            if (down) {
                next_pos.x = player.pos.x - player.dir.x * move_modifier * frame_time;
                next_pos.y = player.pos.y - player.dir.y * move_modifier * frame_time;
            }
            player.pos.x = next_pos.x;
            player.pos.y = next_pos.y;
        }
        if (left) {
            double old_dir_x = player.dir.x;
            player.dir.x = player.dir.x * cos(rot_modifier * frame_time) - player.dir.y * sin(rot_modifier * frame_time);
            player.dir.y = old_dir_x * sin(rot_modifier * frame_time) + player.dir.y * cos(rot_modifier * frame_time);
            double old_cam_x = camera.x;
            camera.x = camera.x * cos(rot_modifier * frame_time) - camera.y * sin(rot_modifier * frame_time);
            camera.y = old_cam_x * sin(rot_modifier * frame_time) + camera.y * cos(rot_modifier * frame_time);
        }
        if (right) {
            double old_dir_x = player.dir.x;
            player.dir.x = player.dir.x * cos(-rot_modifier * frame_time) - player.dir.y * sin(-rot_modifier * frame_time);
            player.dir.y = old_dir_x * sin(-rot_modifier * frame_time) + player.dir.y * cos(-rot_modifier * frame_time);
            double old_cam_x = camera.x;
            camera.x = camera.x * cos(-rot_modifier * frame_time) - camera.y * sin(-rot_modifier * frame_time);
            camera.y = old_cam_x * sin(-rot_modifier * frame_time) + camera.y * cos(-rot_modifier * frame_time);
        }

        while (pause && !done) {
            wait_pause();
            tick_current = SDL_GetTicks();
        }
    }

    // Cleaning
    SDL_Quit();
    printf("End\n");
    return EXIT_SUCCESS;
}

#endif
