// Activate DEBUG to pass into calculation mode:
// Only one loop is performed and the results are saved into a dump file.
// Debug is working with FLAT_NOGRID_VECTOR and FLAT_NOGRID_ANGLE

// SHODAN changes where to find the textures.

// FLAT, ENABLE_FLOOR, TEXTURED and LODE are old switches for flat, textured and raycaster_textured.

//#define DEBUG
//#define FLAT
//#define ENABLE_FLOOR
//#define TEXTURED
//#define LODE
#define SHODAN
//#define FLAT_NOGRID_VECTOR
#define FLAT_NOGRID_ANGLE

//#include "flat.c"
//#include "textured.c"
//#include "raycaster_textured.c"
#include "flat_nogrid_vector.c"
#include "flat_nogrid_angle.c"
