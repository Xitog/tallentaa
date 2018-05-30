
#ifdef FLAT_NOGRID_VECTOR

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
    int texture;
    int sector;
} Wall;

typedef struct {
    int nb_wall;
    int walls[7];
    double height;
} Sector;

typedef struct {
    Vector ray;
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
    {-1, -1, -1}, // ray
    {-1, -1, -1}, // pos
    { {-1, -1, -1}, {-1, -1, -1}, 0, 0}, // wall
    -1, // dist
};

#define DEF_MAX_WALL 7
const int MAX_WALL = DEF_MAX_WALL;
const Wall map[DEF_MAX_WALL] = {
    { // 0
        {1, 1, 0},      // pos 1
        {10, 1, 0},     // pos 2
        HORIZONTAL,     // sens
        WHITE_COLOR,    // color
        1,              // texture
        0,              // sector
    },
    { // 1
        {1, 1, 0},
        {1, 10, 0},
        VERTICAL,
        BLUE_COLOR,
        0,              // texture
        0,              // sector
    },
    {// 2
        {1, 10, 0},
        {10, 10, 0},
        HORIZONTAL,
        YELLOW_COLOR,
        0,              // texture
        0,              // sector
    },
    {// 3
        {10, 1, 0},
        {10, 5, 0},     //{10, 10, 0},
        VERTICAL,
        GREEN_COLOR,
        0,              // texture
        0,              // sector
    },
    /*
    {
        {10, 5, 0},
        {10, 10, 0},
        VERTICAL,
        WHITE_COLOR,
        1,
    }
    */
    {// 4
        {10, 5, 0},
        {15, 5, 0},
        HORIZONTAL,
        WHITE_COLOR,
        1,
        0,              // sector
    },
    {// 5
        {15, 5, 0},
        {15, 10, 0},
        VERTICAL,
        YELLOW_COLOR,
        2,
        0,              // sector
    },
    {// 6
        {10, 10, 0},
        {15, 10, 0},
        HORIZONTAL,
        BLUE_COLOR,
        1,
        0,              // sector
    },
};

#define DEF_MAX_SECTOR 1
const int MAX_SECTOR = DEF_MAX_SECTOR;
const Sector sectors[DEF_MAX_SECTOR] = {
    {
        7, // nb of walls
        {0, 1, 2, 3, 4, 5, 6}, // walls ref
        1, // 3
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
            if (pos.x >= wall.pos1.x && pos.x <= wall.pos2.x) {
                Intersection coll;
                coll.ray.x = ray.x;
                coll.ray.y = ray.y;
                coll.pos.x = pos.x;
                coll.pos.y = wall.pos1.y;
                coll.pos.z = 0;
                coll.wall = wall;
                coll.dist = fabs(pos.y - wall.pos1.y);
                //printf("    HORIZONTAL PERPENDICULAR INTERSECTION AT %.2f, %.2f\n", coll.pos.x, coll.pos.y);
                return coll;
            } else {
                return NO_INTERSECTION;
            }
        } else {
            // calc
            double A = ray.y / ray.x;
            double B = ray_on_pos.y - A * ray_on_pos.x;
            //printf("    HORIZONTAL WALL (%d) and RAY Y = %f * X + %f\n", wall.type, A, B);
            double coll_x = (wall.pos1.y - B) / A;
            //printf("    INTERSECT AT : %f %f\n", coll_x, wall.pos1.y);
            if (coll_x >= wall.pos1.x && coll_x <= wall.pos2.x) {
                Intersection coll;
                coll.ray.x = ray.x;
                coll.ray.y = ray.y;
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
            if (pos.y >= wall.pos1.y && pos.y <= wall.pos2.y) {
                Intersection coll;
                coll.ray.x = ray.x;
                coll.ray.y = ray.y;
                coll.pos.x = wall.pos1.x;
                coll.pos.y = pos.y;
                coll.pos.z = 0;
                coll.wall = wall;
                //printf("        >>> %f %f = %f\n", pos.x, wall.pos1.x, fabs(pos.x - wall.pos1.x));
                coll.dist = fabs(pos.x - wall.pos1.x);
                //printf("        VERTICAL PERPENDICULAR INTERSECTION AT %.2f, %.2f\n", coll.pos.x, coll.pos.y);
                return coll;
            } else {
                return NO_INTERSECTION;
            }
        } else {
            // calc
            double A = ray.y / ray.x;
            double B = ray_on_pos.y - A * ray_on_pos.x;
            //printf("        VERTICAL WALL (%d) and RAY Y = %f * X + %f\n", wall.type, A, B);
            double coll_y = A * wall.pos1.x + B;
            //printf("        INTERSECT AT : X = %f Y = %f. Y should be between %f %f\n", wall.pos1.x, coll_y, wall.pos1.y, wall.pos2.y);
            if (coll_y >= wall.pos1.y && coll_y <= wall.pos2.y) {
                Intersection coll;
                coll.ray.x = ray.x;
                coll.ray.y = ray.y;
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

void draw_sector(int sid, int x, Player player, Vector ray, Intersection * intersections) {
    for (int i=0; i < sectors[sid].nb_wall; i++) {
        Intersection inter = intersection(ray, player.pos, map[sectors[sid].walls[i]]);
        if (inter.dist < intersections[x].dist && inter.dist > -1) {
            intersections[x] = inter;
        }
    }
}

int main(int argc, char * argv[]) {
    printf("Start nogrid vector\n");

    // Player
    Player player = {{12, 5.5, 0}, {-1, 0, 0}}; // pos dir {5.5, 5.5, 0}
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
    int err = init("Woolfy 2.5 FLAT NO GRID VECTOR", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
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

    // Texture loading
    #define TEX_WIDTH 128 //64
    #define TEX_HEIGHT 128 //64
    #define TEXTURES 3
    char * texture_names[] = { ".\\assets\\brick.bmp", ".\\assets\\concrete.bmp", ".\\assets\\door9_1.bmp" };
    Uint32 texture[TEXTURES][TEX_WIDTH][TEX_HEIGHT];
    for (int tni = 0; tni < TEXTURES; tni++) {
        SDL_Surface * surface = load_bmp(texture_names[tni]);
        for (int x = 0; x < surface->w; x++) {
            for (int y = 0; y < surface->h; y++) {
                texture[tni][x][y] = *((Uint32 *)((Uint8 *)surface->pixels + y * surface->pitch + x * surface->format->BytesPerPixel));
            }
        }
    }

    // Main loop
    while(!done) {

        Intersection intersections[SCREEN_WIDTH];
        
        // Computing raycasting
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            intersections[x].dist = 1000;
            double raycast_cpt = 2 * x / (float) SCREEN_WIDTH - 1; // -1 to +1
            Vector ray;
            ray.x = player.dir.x - camera.x * raycast_cpt;
            ray.y = player.dir.y - camera.y * raycast_cpt;
            //printf("%.2f %.2f\n", ray.x, ray.y);
            draw_sector(0, x, player, ray, intersections);
        }
        
        #ifdef DEBUG
        FILE * traces = fopen("debug_1_12_55L.txt", "w");
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            //double raycast_cpt = 2 * x / (float) SCREEN_WIDTH - 1; // -1 to +1
            double perpDist = 1;
            if (intersections[x].wall.type == HORIZONTAL) {
                perpDist = fabs((intersections[x].pos.y - player.pos.y) / intersections[x].ray.y);
            } else if (intersections[x].wall.type == VERTICAL) {
                perpDist = fabs((intersections[x].pos.x - player.pos.x) / intersections[x].ray.x);
            }
            int lineHeight = sectors[intersections[x].wall.sector].height * (SCREEN_HEIGHT / perpDist);
            /*
            fprintf(traces, "x= %3d  ipx= %.4lf  ipy= %.4lf  irx= %.4lf  iry= %.4lf  idist= %lf  line= %5d\n", //  raya= %lf\n", // play= %lf  raya= %lf  diff= %lf  cos= %lf\n", 
                             x, 
                             intersections[x].pos.x,
                             intersections[x].pos.y, 
                             intersections[x].ray.x,
                             intersections[x].ray.y,
                             perpDist, lineHeight); //, 3.141593 - atan(intersections[x].ray.y)); // raycast_cpt, diff, cosdiff);
            */
            fprintf(traces, "%3d, %5d\n", x, lineHeight);
        }
        fclose(traces);
        done = true;
        #endif

        // Rendering
        fill(BLACK);
        
        int mid = SCREEN_HEIGHT / 2;
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            if (intersections[x].dist == -1 || intersections[x].dist == 1000 || intersections[x].dist == 0) {
                continue;
            }
            double perpDist = 1;
            if (intersections[x].wall.type == HORIZONTAL) {
                perpDist = fabs((intersections[x].pos.y - player.pos.y) / intersections[x].ray.y);
            } else if (intersections[x].wall.type == VERTICAL) {
                perpDist = fabs((intersections[x].pos.x - player.pos.x) / intersections[x].ray.x);
            }
            int lineHeight = sectors[intersections[x].wall.sector].height * (SCREEN_HEIGHT / perpDist);
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
            // Flat
            //line(x, mid - lineHeight, x, mid + lineHeight, color);
            // Textured
            double tex_x;
            if (intersections[x].wall.type == VERTICAL) {
                tex_x = intersections[x].pos.y; // 14h07 : il fallait inverser : premiere vraie texture mais tutti frutti !
            } else {
                tex_x = intersections[x].pos.x;
            }
            tex_x -= floor(tex_x);
            tex_x *= (double) TEX_WIDTH;
            int draw_start = mid - lineHeight / 2;
            int draw_end = mid + lineHeight / 2;
            for(int yy = draw_start ; yy <= draw_end ; yy++) {
                int tex_y = (int) (yy - draw_start) * ((double) TEX_HEIGHT / lineHeight); //14h04 (double) + inverser div : premier texture mais répété
                while (tex_y >= TEX_HEIGHT) {
                    tex_y -= TEX_HEIGHT; // 14h12 c'est bon :-) plus rapide que %
                }
                if (tex_x < 0 || tex_x >= TEX_WIDTH || tex_y < 0 || tex_y >= TEX_HEIGHT) {
                    printf("%d %d\n", (int) tex_x, tex_y);
                }
                pixel(x, yy, texture[intersections[x].wall.texture][(int) tex_x][(int) tex_y]);
            }
        }

        if (show_map) {
            // Draw rays
            for (int x = 0; x < SCREEN_WIDTH; x++) {
                if (intersections[x].dist == -1 || intersections[x].dist == 1000) {
                    continue;
                }
                //printf("%d. INTERSECT : %.2f\n", x, intersections[x].dist);
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
        if (right) {
            double old_dir_x = player.dir.x;
            player.dir.x = player.dir.x * cos(rot_modifier * frame_time) - player.dir.y * sin(rot_modifier * frame_time);
            player.dir.y = old_dir_x * sin(rot_modifier * frame_time) + player.dir.y * cos(rot_modifier * frame_time);
            double old_cam_x = camera.x;
            camera.x = camera.x * cos(rot_modifier * frame_time) - camera.y * sin(rot_modifier * frame_time);
            camera.y = old_cam_x * sin(rot_modifier * frame_time) + camera.y * cos(rot_modifier * frame_time);
        }
        if (left) {
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
