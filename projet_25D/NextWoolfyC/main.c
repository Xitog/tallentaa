#include "SDL.h"
#include <stdbool.h> // for bool
#include <stdio.h> // for printf
#include <stdlib.h> // for abs
#include <math.h> // for M_PI

const int NONE = -1;

const short VERTICAL = 1;
const short HORIZONTAL = 2;

typedef struct {
    int x1;
    int y1;
    int x2;
    int y2;
    short type;
} wall;

wall walls_data[100];
int walls_id[100];

int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
int min(int a, int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

bool collision_point(int x, int y) {
    bool res = false;
    for(int i = 0; i < 100; i++) {
        if (walls_id[i] != NONE) {
            if (walls_data[i].type == VERTICAL) {
                res = (x == walls_data[i].x1 && (y >= walls_data[i].y1 && y <= walls_data[i].y2));
                if (res) break;
            } else if (walls_data[i].type == HORIZONTAL) {
                res = (y == walls_data[i].y1 && (x >= walls_data[i].x1 && x <= walls_data[i].x2));
                if (res) break;
            }
        }
    }
    return res;
}

bool collision(int prevx, int prevy, int nextx, int nexty) {
    // Déplacement infra de 1 pixel ou pas de déplacement
    if (abs(prevx - nextx) <= 1 && abs(prevy - nexty) <= 1) {
        return collision_point(nextx, nexty);
    }
    return false;
    //int minx = min(prevx, nextx);
    //int miny = min(prevy, nexty);
    //int maxx = max(prevx, nextx);
    //int maxy = min(prevy, nexty);
    //for (int i = minx; i <= maxx; i++) {
    //    for (int j = miny; j <= maxy; j++) {
    //        if (collision_point(i, j)) {
    //            return true;
    //        }
    //    }
    //}
    //return false;
}

void init_wall(void) {
    for(int i = 0; i < 100; i++) {
        walls_id[i] = NONE;
    }
    int i = 0;
    walls_id[i] = 0;
    walls_data[i].x1 = 100;
    walls_data[i].y1 = 10;
    walls_data[i].x2 = 100;
    walls_data[i].y2 = 100;
    walls_data[i].type = VERTICAL;
    i = 1;
    walls_id[i] = 1;
    walls_data[i].x1 = 10;
    walls_data[i].y1 = 100;
    walls_data[i].x2 = 100;
    walls_data[i].y2 = 100;
    walls_data[i].type = HORIZONTAL;
}

typedef struct {
    int SCREEN_WIDTH;
    int SCREEN_HEIGHT;
    SDL_Window * window;
    SDL_Renderer * renderer;
} Application;

typedef struct {
    double x;
    double y;
    double cameraDirectionX;
    double cameraDirectionY;
    double screenPlaneX;
    double screenPlaneY;
    double screenSize;

    double speed;

    // Direction
    bool right;
    bool left;
    bool up;
    bool down;
    // Loop
    bool done;
    Uint32 old;
} GameState;

void init_game(GameState * game) {
    game->x = 150;
    game->y = 150;
    game->cameraDirectionX = 0;
    game->cameraDirectionY = -1;
    game->screenPlaneX = 1;
    game->screenPlaneY = 0;
    game->screenSize = 100;

    game->speed = 30;

    game->right = false;
    game->left = false;
    game->up = false;
    game->down = false;

    game->done = false;
    game->old = 0;
}

void start_game(GameState * game) {
    game->old = SDL_GetTicks();
}

int SQUARE_SIZE = 32;
int MAP_SIZE = 10;

int Map[10][10] = {
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};

void process_input(GameState * game) {
    SDL_Event event;
    while( SDL_PollEvent( &event ) != 0 ) {
        if( event.type == SDL_QUIT ) {
            game->done = true;
        } else if (event.type == SDL_KEYDOWN) {
            if (event.key.keysym.sym == SDLK_RIGHT) {
                game->right = true;
            } 
            if (event.key.keysym.sym == SDLK_LEFT) {
                game->left = true;
            }
            if (event.key.keysym.sym == SDLK_UP) {
                game->up = true;
            }
            if (event.key.keysym.sym == SDLK_DOWN) {
                game->down = true;
            }
            if (event.key.keysym.sym == SDLK_ESCAPE) {
                game->done = true;
            }
        } else if (event.type == SDL_KEYUP) {
            if (event.key.keysym.sym == SDLK_RIGHT) {
                game->right = false;
            }
            if (event.key.keysym.sym == SDLK_LEFT) {
                game->left = false;
            }
            if (event.key.keysym.sym == SDLK_UP) {
                game->up = false;
            }
            if (event.key.keysym.sym == SDLK_DOWN) {
                game->down = false;
            }
            //if (event.key.keysym.sym == SDLK_TAB) {
            //    game->show_map = !show_map;
            //}
        }
    }
}

void update(GameState * game) {
    //Uint32 elapsed = SDL_GetTicks() - game->old;
    //float delta = elapsed / 1000.0;
    game->old = SDL_GetTicks();
    //double nx = game->x;
    //double ny = game->y;
    //double change = game->speed * delta;
    if (game->right) {
        //game->screen_x += change; //nx = game->x + change;
        //game->x += change;
        //game->screen_i += change;
    }
    if (game->left) {
        //game->screen_x -= change; //nx = game->x - change;
        //game->x -= change;
        //game->screen_i -= change;
    }
    if (game->up) {
        //ny = game->y - change;
        //game->screen_y -= change;
        //game->y -= change;
    }
    if (game->down) {
        //ny = game->y + change;
        //game->screen_y += change;
        //game->y += change;
    }
    /*
    printf("down nx=%f x=%f ny=%f y=%f collision=%i\n", nx, game->x, ny, game->y, collision(game->x, game->y, nx, ny));
    if (!collision(game->x, game->y, nx, ny)) {
        game->x = nx;
        game->y = ny;
    }
    */
}

void draw_matrix(GameState * game, Application * app) {
    for(int line=0; line < MAP_SIZE; line++) {
        for(int column=0; column < MAP_SIZE; column++) {
            SDL_Rect rect = {column * SQUARE_SIZE, line * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE};
            if (Map[line][column] == 1) {
                SDL_SetRenderDrawColor(app->renderer, 0, 255, 0, 255);
                SDL_RenderFillRect(app->renderer, &rect );
            }
            SDL_SetRenderDrawColor(app->renderer, 255, 255, 255, 255);
            SDL_RenderDrawRect(app->renderer, &rect);
        }
    }
}

void clear(Application * app) {
    SDL_SetRenderDrawColor(app->renderer, 0, 0, 0, 255);
    SDL_RenderFillRect(app->renderer, NULL);
}

void draw_walls(GameState * game, Application * app) {
    SDL_Rect fillRect = { 0, 0, app->SCREEN_WIDTH, app->SCREEN_HEIGHT};
    SDL_SetRenderDrawColor(app->renderer, 0, 0, 0, 255);
    SDL_RenderFillRect(app->renderer, &fillRect );

    SDL_SetRenderDrawColor(app->renderer, 255, 0, 0, 255);
    SDL_RenderDrawPoint(app->renderer, game->x, game->y);
    SDL_SetRenderDrawColor(app->renderer, 0, 255, 0, 255);
    for(int i = 0; i < 100; i++) {
        if (walls_id[i] != NONE) {
            SDL_RenderDrawLine(app->renderer, walls_data[i].x1, walls_data[i].y1, walls_data[i].x2, walls_data[i].y2);
        }
    }
}

void draw_camera(GameState * game, Application * app) {
    // Camera point
    SDL_Rect fillRect = { game->x - 1, game->y -1, 3, 3};
    SDL_SetRenderDrawColor(app->renderer, 255, 0, 0, 255);
    SDL_RenderFillRect(app->renderer, &fillRect );
    // Rays
    SDL_SetRenderDrawColor(app->renderer, 255, 255, 0, 255);
    for (int i=0; i < game->screenSize; i++) {
        double rayDirX = game->x + game->cameraDirectionX * 50 - game->screenPlaneX * 50 + game->screenPlaneX * i;
        double rayDirY = game->y + game->cameraDirectionY * 50 - game->screenPlaneY * 50 + game->screenPlaneY * i;
        SDL_RenderDrawLine(app->renderer, game->x, game->y, rayDirX, rayDirY);
    }
    // Screen
    SDL_SetRenderDrawColor(app->renderer, 0, 0, 255, 255);
    int start_of_screen_x = game->x + game->cameraDirectionX * 50 - game->screenPlaneX * (game->screenSize / 2);
    int start_of_screen_y = game->y + game->cameraDirectionY * 50 - game->screenPlaneY * (game->screenSize / 2);
    SDL_RenderDrawLine(app->renderer, start_of_screen_x, start_of_screen_y, start_of_screen_x + game->screenSize, start_of_screen_y);
}

void draw_rays(GameState * game, Application * app) {
    /*
    int rays[100];
    SDL_SetRenderDrawColor(app->renderer, 255, 255, 0, 255);
    //for (int start_ray_x = game->screen_x; start_ray_x < game->screen_i; start_ray_x++) {
    for(int nb = 0; nb < game->screen_size; nb++) {
        int start_ray_x = ((int) game->screen_x) + nb;
        int start_ray_y = (int) game->screen_y;
        int i = start_ray_x;
        int j = start_ray_y;
        int x32 = i >> 5;
        int y32 = j >> 5;
        while (y32 > 0 && Map[y32][x32] == 0) {
            j -= 32;
            x32 = i >> 5;
            y32 = j >> 5;
        }
        // Which side is hit?
        int start_ray_x32 = start_ray_x >> 5;
        int start_ray_y32 = start_ray_y >> 5;
        int eol = 666;
        if (start_ray_x32 == x32) {
            if (start_ray_y32 > y32) { // straight hit by under
                eol = (y32+1) << 5;
            }
        }
        rays[nb] = (int) (((float) app->SCREEN_HEIGHT) / abs(eol-game->screen_y));
        SDL_RenderDrawLine(app->renderer, i, game->screen_y, i, eol);
    }
    // draw wall
    SDL_SetRenderDrawColor(app->renderer, 255, 0, 0, 255);
    SDL_RenderDrawLine(app->renderer, 0, app->SCREEN_HEIGHT >> 1, app->SCREEN_WIDTH, app->SCREEN_HEIGHT >> 1);
    for (int i = 0; i < 100; i++) {
        SDL_RenderDrawLine(app->renderer, 400+i, 240 - rays[i], 400+i, 240 + rays[i]);
    }
    */
}

// global : walls_id, walls_data
void draw(GameState * game, Application * app) {
    clear(app);
    draw_matrix(game, app);
    draw_rays(game, app);
    draw_camera(game, app);
    SDL_RenderPresent(app->renderer);
    SDL_UpdateWindowSurface(app->window);
}

void application_start(Application * app, int w, int h, char * title) {
    app->window = NULL;
    app->SCREEN_WIDTH = w;
    app->SCREEN_HEIGHT = h;
    if( SDL_Init( SDL_INIT_VIDEO ) < 0 ) {
        printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
        exit(EXIT_FAILURE);
    } else {
        //int flags = SDL_WINDOW_FULLSCREEN;
        int flags = 0;
        SDL_CreateWindowAndRenderer(app->SCREEN_WIDTH, app->SCREEN_HEIGHT, flags, &(app->window), &(app->renderer));
        if(app->window == NULL) {
            printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
            exit(EXIT_FAILURE);
        }
    }
    SDL_SetWindowTitle(app->window, title);
}

void application_quit(Application * app) {
    SDL_DestroyRenderer(app->renderer);
    SDL_DestroyWindow(app->window);
    SDL_Quit();
}

int main(int argc, char *argv[]) {
    printf("Hello\n");
    Application app;
    GameState game;
    init_game(&game);
    init_wall();
    application_start(&app, 640, 480, "WoolfyC-2");
    start_game(&game);
    while(!game.done) {
        process_input(&game);
        update(&game);
        draw(&game, &app);
    }
    application_quit(&app);
    return 0;
}

SDL_Event event;
