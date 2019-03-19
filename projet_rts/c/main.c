#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

//#include "minisdl.h"
#include "SDL.h"
#include "SDL_image.h"
#include "SDL_ttf.h"

SDL_Surface * screen;
SDL_Event event;

#define not !

// uint32_t

typedef struct {
	int width;
	int height;
	int ** lines;
} Map;

Map * create_map(int width, int height, int def) {
	Map * map = (Map *) malloc(sizeof(Map));
	map->width = width;
	map->height = height;
	map->lines = (int **) malloc(sizeof(int *) * height);
    for (int row = 0; row < height; row++) {
        map->lines[row] = (int *) malloc(sizeof(int) * width);
		for (int col = 0; col < width; col++) {
			map->lines[row][col] = def;
		} 
    }
	return map;
}

void display_map(Map * map) {
    for (int row = 0; row < map->height; row++) {
        for (int col = 0; col < map->width; col++) {
            printf("%d ", map->lines[row][col]);
        }
        printf("\n");
    }
}

// SDL image function
SDL_Surface * load_image(char * filename ) {
    SDL_Surface * loadedImage = NULL;
    SDL_Surface * optimizedImage = NULL;
    loadedImage = IMG_Load(filename);
    if( loadedImage != NULL ) {
        optimizedImage = SDL_DisplayFormat( loadedImage );
        SDL_FreeSurface( loadedImage ); 
    }
    return optimizedImage;
}

TTF_Font *font = NULL;

SDL_Color CWHITE = { 255, 255, 255 };
//SDL_Color BLACK = {   0,   0,   0 };

bool done = false;
bool down = false;
bool up = false;
bool left = false;
bool right = false;

Uint32 x = 0;
Uint32 y = 0;

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
                    // nothing
                    break;
                case SDLK_SPACE:
                    //pause = !pause;
                    break;
                case SDLK_s:
                    // nothing
                    break;
            }
       } else if (event.type == SDL_QUIT ) {
            done = true;
       }
    }
}

void blit2(int x, int y, SDL_Surface * surf) {
    SDL_Rect rect;
    rect.x = x;
    rect.y = y;
    //rect.w = surf->w;
    //rect.h = surf->h;
    SDL_BlitSurface(surf, NULL, screen, &rect);
}

SDL_Surface * load2(const char * path) {
    SDL_Surface * temp = SDL_LoadBMP(path);
    SDL_Surface * optimized = NULL;
    if(temp != NULL) {
        optimized = SDL_DisplayFormat(temp);
        SDL_FreeSurface(temp);
    }
    return optimized;
}

int main (int argc, char * argv[]) {
    
    int size = 0;
    char name[256];

    FILE * file = fopen("map.txt", "r");
    fscanf(file, "%s", name);
    for (int i = 0; i < 256; i++) {
        if (name[i] == '_') {
            name[i] = ' ';
        }
    }

    printf("Name = %s\n", name);

    fscanf(file, "%d", &size);
    printf("Size = %d\n", size);

    Map * map1 = create_map(size, size, 0);

    for (int row = 0; row < size; row++) {
        for (int col = 0; col < size; col++) {
            fscanf(file, "%d", &map1->lines[row][col]);
        }
    }
    
    fclose(file);

	display_map(map1);

	// Matrix tests

	Map * one_row = create_map(20, 1, 0);
	display_map(one_row);
	
	Map * one_col = create_map(1, 10, 2);
	display_map(one_col);
    
    // Lecture de map

    FILE * map_file = fopen("The_quiet_river.map", "rb");
    int version = 0;
    fread(&version, sizeof(int), 1, map_file);
    printf("Version = %d\n", version);
    int width = 0;
    fread(&width, sizeof(int), 1, map_file);
    printf("Width   = %d\n", width);
    int height = 0;
    fread(&height, sizeof(int), 1, map_file);
    printf("Height  = %d\n", height);
    int namelen = 0;
    fread(&namelen, sizeof(int), 1, map_file);
    printf("Length  = %d\n", namelen);

    char * map_name = (char *) malloc((namelen + 1) * sizeof(char));
    memset(map_name, '\0', namelen + 1);
    size_t len = fread(map_name, sizeof(char), namelen, map_file);
    printf("Len = %d\n", len);
    printf("Name  = %s\n", map_name);
    fclose(map_file);

	// Transition
	
    // Init and screen

	const char * APPNAME = "RTS C";
	const int SCREEN_WIDTH = 640;
	const int SCREEN_HEIGHT = 480;
	const int BITS_PER_PIXEL = 32;
	//const bool FULLSCREEN = false;

    if (SDL_Init(SDL_INIT_EVERYTHING) < 0) {
        perror("Error when initializing SDL");
        return EXIT_FAILURE;
    }
    screen = SDL_SetVideoMode(SCREEN_WIDTH, SCREEN_HEIGHT, BITS_PER_PIXEL, SDL_SWSURFACE | SDL_HWPALETTE);
    if (screen == NULL) {
        printf("Error when setting video mode : %s\n", SDL_GetError());
        SDL_Quit();
        return EXIT_FAILURE;
    }
    SDL_WM_SetCaption(APPNAME, NULL);
    SDL_EnableUNICODE(true);

    //int err = init((char *) APPNAME, SCREEN_WIDTH, SCREEN_HEIGHT, BITS_PER_PIXEL, FULLSCREEN);
    //if (err == EXIT_FAILURE) {
    //    return err;
    //}
    //Initialize SDL_ttf
    if (TTF_Init() == -1)
    {
        return false;    
    }
	
	font = TTF_OpenFont("ProzaLibre-Regular.ttf", 28);
	if (font == NULL)
    {
        return false;
    }
	SDL_Surface * message = TTF_RenderText_Solid(font, "The quick brown fox jumps over the lazy dog", CWHITE);
	
    printf("Loading textures\n");
	SDL_Surface * textures[10];
	textures[0] = load2("graphics\\0000000000.bmp"); //"..\\javascript\\graphics\\textures\\0000000000.bmp"); SDL_LoadBMP
	textures[1] = load2("graphics\\1000000000.bmp"); //"..\\javascript\\graphics\\textures\\1000000000.bmp"); SDL_LoadBMP
	// use SDL_image, load_bmp use only minisdl	
	//SDL_Surface * tex1 = load_image((char *) "..\\javascript\\graphics\\textures\\0000000000.bmp");
    //if (tex1 == NULL) {
    //    printf("Failed to load texture\n");
    //    return -1;
    //}

    printf("Starting main loop\n");

    Uint32 cap_fps_start = 0;
	const Uint32 FRAMES_PER_SECOND = 30;
	const Uint32 TIME_PER_FRAME = 1000 / FRAMES_PER_SECOND; // 33
    
    // Free FPS + Measure
    Uint32 frame_count_start = SDL_GetTicks();
    Uint32 frame_count = 0;
    char output[50];
    float fps;

    int current;
    float diff_with_last;

	while(not done) {
        current = SDL_GetTicks();
        diff_with_last = (current - cap_fps_start) / 1000.f;
        cap_fps_start = current;
        
		input();

		// Provoque le rafraîchissement de l'écran
		if (down) y += 500 * diff_with_last;
		if (up) y -= 500 * diff_with_last;
		if (left) x -= 500 * diff_with_last;
		if (right) x += 500 * diff_with_last;
		
		SDL_FillRect(screen, NULL, 0); // Clear
	    // Bliting textures
		for (int row = 0; row < 10; row++) {
			for (int col = 0; col < 10; col++) {
	            //printf("%d %d %d\n", row, col, (int) tex1);
				blit2(col * 32, row * 32, textures[0]);
			}
		}
		blit2(x, y, textures[1]);
		blit2(200, 50, message);

		SDL_Flip(screen);
        
        // FPS Free + Measure
        frame_count += 1;
        int elapsed = SDL_GetTicks() - frame_count_start;
        if(elapsed >= 1000) { // 1 second passed
            fps = frame_count / ( elapsed / 1000.f );
            frame_count = 0;
            snprintf(output, 50, "%f", fps);
            SDL_WM_SetCaption(output, NULL);
            frame_count_start = SDL_GetTicks();
        }
        
        // FPS capped
		//printf("Timer: %d\n", (SDL_GetTicks() - start)/1000);
        if ((SDL_GetTicks() - cap_fps_start) < TIME_PER_FRAME)
        {
            //Sleep the remaining frame time
            Uint32 time_to_wait = TIME_PER_FRAME - (SDL_GetTicks() - cap_fps_start);
            printf("sleep for %d\n", time_to_wait);
            if (time_to_wait > 0 && time_to_wait < TIME_PER_FRAME)
                SDL_Delay(time_to_wait);
        }
	}
	
	//int SDL_SaveBMP(SDL_Surface *surface, const char *file);
	SDL_SaveBMP(screen, "out.bmp");

    SDL_FreeSurface( message );
    TTF_CloseFont( font );
    TTF_Quit();

    return 0;

	// TODO : display actual FPS

}
