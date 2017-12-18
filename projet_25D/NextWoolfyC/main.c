#include "SDL.h"
#include <stdbool.h> // for bool
#include <stdio.h> // for printf
#include <stdlib.h> // for abs
#include <math.h> // for M_PI

typedef enum {
	NONE = 0,
	VERTICAL = 1,
	HORIZONTAL = 2,
} WallType;

typedef struct {
    Uint8 r;
    Uint8 g;
    Uint8 b;
    Uint8 a;
} Color;

typedef struct {
	bool used;
    int x1;
    int y1;
    int x2;
    int y2;
	int x;
	int y;
    WallType type;
    Color color;
} Wall;

#define MAX_WALL 100

Wall walls[MAX_WALL];

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
	/*
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
	*/
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

void wall_init(void) {
    for(int i = 0; i < 100; i++) {
        walls[i].used = false;
		walls[i].x1 = 0;
		walls[i].y1 = 0;
		walls[i].x2 = 0;
		walls[i].y2 = 0;
		walls[i].x = 0;
		walls[i].y = 0;
		walls[i].type = NONE;
        walls[i].color.r = 0;
        walls[i].color.g = 0;
        walls[i].color.b = 0;
        walls[i].color.a = 255;
    }
    int i = 0;
    walls[i].used = true;
    walls[i].x1 = 32;
    walls[i].y1 = 32;
    walls[i].x2 = 256;
    walls[i].y2 = 32;
	walls[i].y = 32;
    walls[i].type = HORIZONTAL;
    walls[i].color.r = 255;

    i = 1;
    walls[i].used = true;
    walls[i].x1 = 32;
    walls[i].y1 = 32;
    walls[i].x2 = 32;
    walls[i].y2 = 256;
	walls[i].x = 32;
    walls[i].type = VERTICAL;
    walls[i].color.r = 255;
    walls[i].color.g = 255;

    i = 2;
    walls[i].used = true;
    walls[i].x1 = 256;
    walls[i].y1 = 32;
    walls[i].x2 = 256;
    walls[i].y2 = 256;
	walls[i].x = 256;
    walls[i].type = VERTICAL;
    walls[i].color.b = 255;

    i = 3;
    walls[i].used = true;
    walls[i].x1 = 32;
    walls[i].y1 = 256;
    walls[i].x2 = 256;
    walls[i].y2 = 256;
	walls[i].y = 256;
    walls[i].type = HORIZONTAL;
    walls[i].color.g = 255;
}

typedef struct {
    int SCREEN_WIDTH;
    int SCREEN_HEIGHT;
    SDL_Window * window;
    SDL_Renderer * renderer;
    int SCREEN_START_OF_25D_RENDERING;
    int SCREEN_CENTER_25D_RENDERING;
    int SCREEN_HEIGHT_25D_RENDERING;
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
    bool turn_right;
    bool turn_left;
    bool step_right;
    bool step_left;
    bool up;
    bool down;
    // Dump for debug
    bool dump;
    // Loop
    bool done;
    Uint32 old;
} GameState;

void game_init(GameState * game) {
    game->x = 220;
    game->y = 150;
    game->cameraDirectionX = 0;
    game->cameraDirectionY = -1;
    game->screenPlaneX = 1;
    game->screenPlaneY = 0;
    game->screenSize = 640;

    game->speed = 30;

    game->turn_right = false;
    game->turn_left = false;
    game->step_right = false;
    game->step_left = false;
    game->up = false;
    game->down = false;
    game->dump = true;

    game->done = false;
    game->old = 0;
}

void game_start(GameState * game) {
    game->old = SDL_GetTicks();
}

int SQUARE_SIZE = 32;
int MAP_SIZE = 11;

int Map[11][11] = {
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};

void process_input(GameState * game) {
    int TURN_RIGHT = SDLK_d; // SDLK_RIGHT
    int TURN_LEFT = SDLK_q; // SDLK_LEFT
    int FORWARD = SDLK_z; // SDLK_UP
    int BACKWARD = SDLK_s; // SDLK_DOWN
    int STEP_RIGHT = SDLK_e;
    int STEP_LEFT = SDLK_a;
    SDL_Event event;
    while( SDL_PollEvent( &event ) != 0 ) {
        if( event.type == SDL_QUIT ) {
            game->done = true;
        } else if (event.type == SDL_KEYDOWN) {
            if (event.key.keysym.sym == TURN_RIGHT) {
                game->turn_right = true;
            } 
            if (event.key.keysym.sym == TURN_LEFT) {
                game->turn_left = true;
            }
            if (event.key.keysym.sym == FORWARD) {
                game->up = true;
            }
            if (event.key.keysym.sym == BACKWARD) {
                game->down = true;
            }
            if (event.key.keysym.sym == SDLK_ESCAPE) {
                game->done = true;
            }
            if (event.key.keysym.sym == SDLK_TAB) {
                game->dump = true;
            }
            if (event.key.keysym.sym == STEP_RIGHT) {
                game->step_right = true;
            } 
            if (event.key.keysym.sym == STEP_LEFT) {
                game->step_left = true;
            }
        } else if (event.type == SDL_KEYUP) {
            if (event.key.keysym.sym == TURN_RIGHT) {
                game->turn_right = false;
            }
            if (event.key.keysym.sym == TURN_LEFT) {
                game->turn_left = false;
            }
            if (event.key.keysym.sym == FORWARD) {
                game->up = false;
            }
            if (event.key.keysym.sym == BACKWARD) {
                game->down = false;
            }
            if (event.key.keysym.sym == SDLK_TAB) {
                game->dump = false;
            }
            if (event.key.keysym.sym == STEP_RIGHT) {
                game->step_right = false;
            } 
            if (event.key.keysym.sym == STEP_LEFT) {
                game->step_left = false;
            }
        }
    }
}

void update(GameState * game) {
    Uint32 elapsed = SDL_GetTicks() - game->old;
    float delta = elapsed / 1000.0;
    game->old = SDL_GetTicks();
    //double nx = game->x;
    //double ny = game->y;
    double change = game->speed * delta;
    double rotChange = 2.0 * delta;
    if (game->turn_left) {
        double oldDirX = game->cameraDirectionX;
        game->cameraDirectionX = oldDirX * cos(-rotChange) - game->cameraDirectionY * sin(-rotChange);
        game->cameraDirectionY = oldDirX * sin(-rotChange) + game->cameraDirectionY * cos(-rotChange);
        double oldPlaneX = game->screenPlaneX;
        game->screenPlaneX = oldPlaneX * cos(-rotChange) - game->screenPlaneY * sin(-rotChange);
        game->screenPlaneY = oldPlaneX * sin(-rotChange) + game->screenPlaneY * cos(-rotChange);
    }
    if (game->turn_right) {
        double oldDirX = game->cameraDirectionX;
        game->cameraDirectionX = oldDirX * cos(rotChange) - game->cameraDirectionY * sin(rotChange);
        game->cameraDirectionY = oldDirX * sin(rotChange) + game->cameraDirectionY * cos(rotChange);
        double oldPlaneX = game->screenPlaneX;
        game->screenPlaneX = oldPlaneX * cos(rotChange) - game->screenPlaneY * sin(rotChange);
        game->screenPlaneY = oldPlaneX * sin(rotChange) + game->screenPlaneY * cos(rotChange);
    }
    if (game->step_right) {
        //nx = game->x + change;
        game->x += change;
    }
    if (game->step_left) {
        game->x -= change;
        //nx = game->x - change;
    }
    if (game->up) {
        //game->y -= change;
        float nx = game->x + game->cameraDirectionX * change;
        float ny = game->y + game->cameraDirectionY * change;
        //if (area[(int) nx][(int) (posY)] == 0) { posX = nx; }
        //if (area[(int) (posX)][(int) ny] == 0) { posY = ny; }
        game->x = nx;
        game->y = ny;
    }
    if (game->down) {
        //game->y += change;
        float nx = game->x - game->cameraDirectionX * change;
        float ny = game->y - game->cameraDirectionY * change;
        game->x = nx;
        game->y = ny;
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
	//SDL_Rect fillRect = { 0, 0, app->SCREEN_WIDTH, app->SCREEN_HEIGHT}; &fillRect bellow is not needed: NULL 
    SDL_SetRenderDrawColor(app->renderer, 0, 0, 0, 255);
    SDL_RenderFillRect(app->renderer, NULL);
}

void draw_walls(GameState * game, Application * app) {
    SDL_SetRenderDrawColor(app->renderer, 255, 0, 0, 255);
    SDL_RenderDrawPoint(app->renderer, game->x, game->y);
    SDL_SetRenderDrawColor(app->renderer, 0, 255, 0, 255);
    for(int i = 0; i < 100; i++) {
        if (walls[i].used) {
            SDL_RenderDrawLine(app->renderer, walls[i].x1, walls[i].y1, walls[i].x2, walls[i].y2);
        }
    }
}

void draw_camera(GameState * game, Application * app) {
    // Camera point
    SDL_Rect fillRect = { game->x - 1, game->y -1, 3, 3};
    SDL_SetRenderDrawColor(app->renderer, 255, 0, 0, 255);
    SDL_RenderFillRect(app->renderer, &fillRect );
    //int midscreen = app->SCREEN_WIDTH / 2;
    // Rays
    int dist[game->screenSize];
    int wall[game->screenSize]; // id of wall
    double xcos[game->screenSize];
    const int STEP = 100;
    for (int i=0; i < game->screenSize; i+=STEP) {
        double rayDirYY = (game->cameraDirectionY  + ( ((double)i/game->screenSize) - 0.5) * game->screenPlaneY);
        double rayDirXX = (game->cameraDirectionX  + ( ((double)i/game->screenSize) - 0.5) * game->screenPlaneX);
        /*
        printf("===== %d ====\n", i);
        printf("Player : x = %f, y = %f\n", game->x, game->y);
        printf("Rayon X : %f\n", rayDirXX);
        printf("Rayon Y : %f\n", rayDirYY);
        */
        dist[i] = 0;
        wall[i] = NONE;
        for(int w=0; w < MAX_WALL; w++) {
            if (!walls[w].used) {
                break;
            }
		    if (walls[w].type == HORIZONTAL) { // y est FIXE, x varie entre 2 bornes. y = a * x + b donc x = (y-b) / a
                if ( (walls[w].y > game->y && rayDirYY < 0) || (walls[w].y < game->y && rayDirYY > 0)) {
                    continue;
                }
			    double diffBetweenY = walls[w].y - game->y;
                if (rayDirYY != 0) {
                    double factor = abs(diffBetweenY / rayDirYY);
                    if (factor > 0.0000000001) {
                        double xnew = game->x + rayDirXX * factor;
			            //printf("i/w = %f, diffy = %f, rayDirX = %f, rayDirY = %f, factor = %f, xnew = %f\n", ((double)i/game->screenSize), diffBetweenY, rayDirXX, rayDirYY, factor, xnew);
			            if (xnew > walls[w].x1 && xnew < walls[w].x2) {
                            //printf("Mur touche : %d %d-%d %d-%d @x=%f\n", w, walls[w].x1, walls[w].y1, walls[w].x2, walls[w].y2, xnew);
                            double produitScalaire = game->cameraDirectionX * abs(game->x - xnew) + game->cameraDirectionY * abs(game->y - walls[w].y);
                            //double normeCameraVector = sqrt(pow(game->cameraDirectionX, 2) + pow(game->cameraDirectionY, 2));
                            double normeDistance = sqrt(pow(game->x - xnew, 2)+pow(game->y - walls[w].y, 2));
                            //double cosVecteurs = produitScalaire / (normeCameraVector * normeDistance);
                            double cosVecteurs = produitScalaire / normeDistance;
                            //
                            double orthoDist = abs(normeDistance * cosVecteurs);
                            if (orthoDist > 0 && (dist[i] == 0 || dist[i] > orthoDist)) {
                                dist[i] = orthoDist;
                                wall[i] = w;
                                xcos[i] = cosVecteurs;
                                // Draw
                                SDL_SetRenderDrawColor(app->renderer, 255, 0, 0, 255);
				                SDL_RenderDrawLine(app->renderer, game->x, game->y, xnew, walls[w].y); // 2D
                            }
                        }
                    }
			    }
            } else if (walls[w].type == VERTICAL) {
                if ( (walls[w].x > game->x && rayDirXX < 0) || (walls[w].x < game->x && rayDirXX > 0)) {
                    continue;
                }
                double diffBetweenX = walls[w].x - game->x;
                if (rayDirXX != 0) {
                    double factor = abs(diffBetweenX / rayDirXX);
                    if (factor > 0.0000000001) {
                        double ynew = game->y + rayDirYY * factor;
                        if (ynew > walls[w].y1 && ynew < walls[w].y2) {
                            //printf("Mur touche : %d %d-%d %d-%d @ y=%f\n", w, walls[w].x1, walls[w].y1, walls[w].x2, walls[w].y2, ynew);
                            // COS
                            double produitScalaire = game->cameraDirectionX * abs(game->x - walls[w].x) + game->cameraDirectionY * abs(game->y - ynew);
                            //double normeCameraVector = sqrt(pow(game->cameraDirectionX, 2) + pow(game->cameraDirectionY, 2)); normeCameraVector=TOUJOURS 1!
                            double normeDistance = sqrt(pow(game->x - walls[w].x, 2)+pow(game->y - ynew, 2));
                            //double cosVecteurs = produitScalaire / (normeCameraVector * normeDistance); normeCameraVector=TOUJOURS 1!
                            double cosVecteurs = produitScalaire / normeDistance;
                            // PROJ ORTHO
                            double orthoDist = abs(normeDistance * cosVecteurs);
                            if (orthoDist > 0 && (dist[i] == 0 || dist[i] > orthoDist)) {
                                dist[i] = orthoDist;
                                wall[i] = w;
                                xcos[i] = cosVecteurs;
                                // Draw
                                SDL_SetRenderDrawColor(app->renderer, 255, 255, 0, 255);
				                SDL_RenderDrawLine(app->renderer, game->x, game->y, walls[w].x, ynew); // 2D
                            }
                        }
                    }
                }
            }
		}
    }
    for (int i=0; i < game->screenSize; i+=STEP) {
        if (dist[i] > 0) {
            SDL_SetRenderDrawColor(app->renderer, walls[wall[i]].color.r, walls[wall[i]].color.g, walls[wall[i]].color.b, 255);
            double divider = (double) dist[i] / 32; // 20h45 : il a suffit d'ajouter (double) pour que... ça marche !!! Yeepi ! 20h49 : cela ne dépasse plus de "l'écran" virtuel.
            if (divider == 0) {
                divider = 0.00000001;
            }
            int wallheight = app->SCREEN_HEIGHT_25D_RENDERING / divider;
            int drawStart = max(app->SCREEN_START_OF_25D_RENDERING, app->SCREEN_CENTER_25D_RENDERING - wallheight / 2);
            int drawEnd = min(app->SCREEN_START_OF_25D_RENDERING + app->SCREEN_HEIGHT_25D_RENDERING, app->SCREEN_CENTER_25D_RENDERING + wallheight / 2);
            SDL_RenderDrawLine(app->renderer, i, drawStart, i, drawEnd);
        }
    }
    SDL_SetRenderDrawColor(app->renderer, 255, 255, 255, 255);
    SDL_RenderDrawLine(app->renderer, 0, app->SCREEN_START_OF_25D_RENDERING, app->SCREEN_WIDTH, app->SCREEN_START_OF_25D_RENDERING);
    SDL_RenderDrawLine(app->renderer, 0, app->SCREEN_START_OF_25D_RENDERING + app->SCREEN_HEIGHT_25D_RENDERING, app->SCREEN_WIDTH, app->SCREEN_START_OF_25D_RENDERING + app->SCREEN_HEIGHT_25D_RENDERING);
    if (game->dump) {
        FILE * f = fopen("dump.txt", "w");
        for (int i=0; i < game->screenSize; i+=STEP) {
            if (dist[i] > 0) {
                fprintf(f, "%d. dist = %d 200 - dist = %d cos = %f\n", i, dist[i], 200 - dist[i], xcos[i]);
            } else {
                fprintf(f, "dist < 0\n");
            }
        }
        fclose(f);
        game->dump = false;
        //exit(EXIT_FAILURE);
    }
    // Screen
    SDL_SetRenderDrawColor(app->renderer, 0, 0, 255, 255);
    int start_of_screen_x = game->x + game->cameraDirectionX * 10 - 5 * game->screenPlaneX;
    int end_of_screen_x = game->x + game->cameraDirectionX * 10 + 5 * game->screenPlaneX;
    int start_of_screen_y = game->y + game->cameraDirectionY * 10 - 5 * game->screenPlaneY;
    int end_of_screen_y = game->y + game->cameraDirectionY * 10 + 5 * game->screenPlaneY;
    SDL_RenderDrawLine(app->renderer, start_of_screen_x, start_of_screen_y, end_of_screen_x, end_of_screen_y);
}

// global : walls_id, walls_data
void draw(GameState * game, Application * app) {
    clear(app);
    //draw_matrix(game, app);
	draw_walls(game, app);
    //draw_rays(game, app);
    draw_camera(game, app);
    SDL_RenderPresent(app->renderer);
    SDL_UpdateWindowSurface(app->window);
}

void application_start(Application * app, int w, int h, char * title) {
    app->window = NULL;
    app->SCREEN_WIDTH = w;
    app->SCREEN_HEIGHT = h;
    app->SCREEN_START_OF_25D_RENDERING = 250;
    app->SCREEN_HEIGHT_25D_RENDERING = 200;
    app->SCREEN_CENTER_25D_RENDERING = 350;
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
    game_init(&game);
    wall_init();
    application_start(&app, 640, 480, "WoolfyC-2");
    game_start(&game);
    while(!game.done) {
        process_input(&game);
        update(&game);
        draw(&game, &app);
    }
    application_quit(&app);
    return 0;
}

