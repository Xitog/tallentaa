
#ifdef FLAT_NOGRID_ANGLE

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
    double angle;
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
        1,
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
    Vector ray_on_pos;
    ray_on_pos.x = ray.x + pos.x;
    ray_on_pos.y = ray.y + pos.y;
    if (wall.type == HORIZONTAL) {
        if (ray.y == 0) {
            return NO_INTERSECTION;
        } else if (ray.y > 0 && wall.pos2.y < pos.y) {
            return NO_INTERSECTION;
        } else if (ray.y < 0 && wall.pos1.y > pos.y) {
            return NO_INTERSECTION;
        } else if (ray.x == 0) { // perpendicular to wall
            Intersection coll;
            coll.ray.x = ray.x;
            coll.ray.y = ray.y;
            coll.pos.x = ray_on_pos.x;
            coll.pos.y = wall.pos1.y;
            coll.pos.z = 0;
            coll.wall = wall;
            coll.dist = sqrt(pow(coll.pos.x - pos.x, 2) + pow(coll.pos.y - pos.y, 2));
            return coll;
        } else {
            double A = ray.y / ray.x;
            double B = ray_on_pos.y - A * ray_on_pos.x;
            double coll_x = (wall.pos1.y - B) / A;
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
            return NO_INTERSECTION;
        } else if (ray.x > 0 && wall.pos2.x < pos.x) {
            return NO_INTERSECTION;
        } else if (ray.x < 0 && wall.pos1.x > pos.x) {
            return NO_INTERSECTION;
        } else if (ray.y == 0) { // perpendicular to wall
            Intersection coll;
            coll.ray.x = ray.x;
            coll.ray.y = ray.y;
            coll.pos.x = wall.pos1.x;
            coll.pos.y = ray_on_pos.y;
            coll.pos.z = 0;
            coll.wall = wall;
            coll.dist = sqrt(pow(coll.pos.x - pos.x, 2) + pow(coll.pos.y - pos.y, 2));
            return coll;
        } else {
            double A = ray.y / ray.x;
            double B = ray_on_pos.y - A * ray_on_pos.x;
            double coll_y = A * wall.pos1.x + B;
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

/*
 x_diff = playerx - xs;
 y_diff = playery - ys;
 if (abs(x_diff) > abs(y_diff)) {
   distance = x_diff / cos(angle); else
   distance = y_diff / sin(angle); 
 }
 */

void draw_sector(int sid, int x, Player player, Vector ray, Intersection * intersections) {
    for (int i=0; i < sectors[sid].nb_wall; i++) {
        Intersection inter = intersection(ray, player.pos, map[sectors[sid].walls[i]]);
        if (inter.dist < intersections[x].dist && inter.dist > -1) {
            intersections[x] = inter;
        }
    }
}

int main(int argc, char * argv[]) {
    printf("Start nogrid angle\n");

    // Player
    Player player = {{12, 5.5, 0}, {-1, 0, 0}, 180.0 * 0.017453292519943295}; // pos dir angle {5.5, 5.5, 0}
    Vector next_pos = {0, 0, 0};

    // Time
    double tick_current = 0.0;
    double tick_previous = 0.0;
    double frame_time = 0.0;

    // Moves
    double move_modifier = MOVE_SPEED;
    double rot_modifier = ROT_SPEED;

    // Init and screen
    int err = init("Woolfy 2.5 FLAT NO GRID ANGLE", SCREEN_WIDTH, SCREEN_HEIGHT, 32, false);
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
    #ifdef SHODAN
    char * texture_names[] = { 
        "..\\..\\assets\\graphic\\textures\\woolfy_wall\\freedoom\\brick.bmp", 
        "..\\..\\assets\\graphic\\textures\\woolfy_wall\\freedoom\\concrete.bmp", 
        "..\\..\\assets\\graphic\\textures\\woolfy_wall\\freedoom\\door9_1.bmp" 
    };
    #endif
    #ifndef SHODAN
    char * texture_names[] = { ".\\assets\\brick.bmp", ".\\assets\\concrete.bmp", ".\\assets\\door9_1.bmp" };
    #endif
    Uint32 texture[TEXTURES][TEX_WIDTH][TEX_HEIGHT];
    for (int tni = 0; tni < TEXTURES; tni++) {
        SDL_Surface * surface = load_bmp(texture_names[tni]);
        for (int x = 0; x < surface->w; x++) {
            for (int y = 0; y < surface->h; y++) {
                texture[tni][x][y] = *((Uint32 *)((Uint8 *)surface->pixels + y * surface->pitch + x * surface->format->BytesPerPixel));
            }
        }
    }
    
    double player_fov = 66.84962236520761 * 0.017453292519943295; // 45 66 90 120
    double player_fov_mid = player_fov / (double) 2;
    double player_fov_inc = player_fov / (double) SCREEN_WIDTH;

    // Main loop
    while(!done) {

        Intersection intersections[SCREEN_WIDTH];
        
        double camera_x = cos(player.angle + 90 * 0.017453292519943295) * 0.66;
        double camera_y = sin(player.angle + 90 * 0.017453292519943295) * 0.66;

        // Computing raycasting
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            intersections[x].dist = 1000;
            
            double raycast_cpt = 2 * x / (float) SCREEN_WIDTH - 1; // -1 to +1
            Vector ray;
            ray.x = cos(player.angle) + camera_x * raycast_cpt;
            ray.y = sin(player.angle) + camera_y * raycast_cpt;
            double ray_angle = 3.141593 - atan(ray.y);

            /*
            double ray_angle = player_fov_inc * x + player.angle - player_fov_mid;
            Vector ray;
            ray.x = cos(ray_angle);
            ray.y = sin(ray_angle);
            */

            draw_sector(0, x, player, ray, intersections);

            // Calcul distance
            if (intersections[x].dist != -1 && intersections[x].dist != 1000) {
                //double dist = intersections[x].dist;
                double ray_angle = player_fov_inc * x + player.angle - player_fov_mid;
                double diff = player.angle - ray_angle;
                intersections[x].dist *= fabs(cos(diff));
                /*
                double perpDist = 1;
                char c = 'u';
                if (intersections[x].wall.type == HORIZONTAL) {
                    perpDist = fabs((intersections[x].pos.y - player.pos.y) / intersections[x].ray.y);
                    c = 'h';
                } else if (intersections[x].wall.type == VERTICAL) {
                    perpDist = fabs((intersections[x].pos.x - player.pos.x) / intersections[x].ray.x);
                    c = 'v';
                }
                intersections[x].dist = perpDist;
                */
                /*
                if (fabs(perpDist - intersections[x].dist) > 0.1) {
                    printf("x: %d diff_angle: %f wall: %c\n", x, diff, c);
                    printf("   cos : %f sin  : %f\n", cos(diff), sin(diff));
                    printf("   rayx: %f rayy : %f\n", ray.x, ray.y);
                    printf("   inter_raw: %.2f inter_correct: %.2f perp: %.2f diff: %.2f\n", dist, intersections[x].dist, perpDist, perpDist - intersections[x].dist);
                }*/
                //intersections[x].dist = perpDist;
            }
        }
        
        #ifdef DEBUG
        FILE * traces = fopen("debug_2_12_55L.txt", "w");
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            double ray_angle = player_fov_inc * x + player.angle - player_fov_mid;
            int lineHeight = sectors[intersections[x].wall.sector].height * (SCREEN_HEIGHT / intersections[x].dist);
            //double diff = player.angle - ray_angle;
            //double cosdiff = cos(diff);
            /*
            fprintf(traces, "x= %3d  ipx= %.4lf  ipy= %.4lf  irx= %.4lf  iry= %.4lf  idist= %lf  line= %5d\n", //  raya= %lf\n", // play= %lf  diff= %lf  cos= %lf\n", 
                             x, 
                             intersections[x].pos.x,
                             intersections[x].pos.y, 
                             intersections[x].ray.x,
                             intersections[x].ray.y,
                             intersections[x].dist, lineHeight); //, ray_angle); //, player.angle, diff, cosdiff);
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
            int lineHeight = sectors[intersections[x].wall.sector].height * (SCREEN_HEIGHT / intersections[x].dist);
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
                tex_x = intersections[x].pos.y;
            } else {
                tex_x = intersections[x].pos.x;
            }
            tex_x -= floor(tex_x);
            tex_x *= (double) TEX_WIDTH;
            int draw_start = mid - lineHeight / 2;
            int draw_end = mid + lineHeight / 2;
            for(int yy = draw_start ; yy <= draw_end ; yy++) {
                int tex_y = (int) (yy - draw_start) * ((double) TEX_HEIGHT / lineHeight);
                while (tex_y >= TEX_HEIGHT) {
                    tex_y -= TEX_HEIGHT; // plus rapide que %
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
            double pos_dir_x = player.pos.x + cos(player.angle);
            double pos_dir_y = player.pos.y + sin(player.angle);
            // cam left and right
            line(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, (pos_dir_x + camera_x) * MINIMAP_ZOOM, (pos_dir_y + camera_y) * MINIMAP_ZOOM, GREEN);
            line(player.pos.x * MINIMAP_ZOOM, player.pos.y * MINIMAP_ZOOM, (pos_dir_x - camera_x) * MINIMAP_ZOOM, (pos_dir_y - camera_y) * MINIMAP_ZOOM, RED);
            //line((pos_dir_x + camera.x) * MINIMAP_ZOOM, (pos_dir_y + camera.y) * MINIMAP_ZOOM, (pos_dir_x - camera.x) * MINIMAP_ZOOM, (pos_dir_y - camera.y) * MINIMAP_ZOOM, PURPLE);
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

        // Time and input
        input();
        tick_previous = tick_current;
        tick_current = SDL_GetTicks();
        frame_time = (tick_current - tick_previous);
        
        // Update
        if (up || down) {
            if (up) {
                next_pos.x = player.pos.x + cos(player.angle) * move_modifier * frame_time;
                next_pos.y = player.pos.y + sin(player.angle) * move_modifier * frame_time;
            }
            if (down) {
                next_pos.x = player.pos.x - cos(player.angle) * move_modifier * frame_time;
                next_pos.y = player.pos.y - sin(player.angle) * move_modifier * frame_time;
            }
            bool dist_ok = true;
            int size = 10;
            int min_dist = 1;
            for (int x = SCREEN_WIDTH / 2 - size; x < SCREEN_WIDTH / 2 + size; x++) {
                if (intersections[x].dist <= min_dist) {
                    dist_ok = false;
                    break;
                }
            }
            if (dist_ok || down) {
            player.pos.x = next_pos.x;
            player.pos.y = next_pos.y;
        }
        }
        if (left) {
            player.angle -= rot_modifier * frame_time;
        }
        if (right) {
            player.angle += rot_modifier * frame_time;
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
