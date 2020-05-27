#include <stdio.h>
#include <stdlib.h>

typedef unsigned short int duoctet;
typedef char octet;

int main(int argc, char * argv[]) {

	// Size of type
	printf("Taille unsigned short int = %d\n", sizeof(unsigned short)); // 2 octets = 16 bits
	printf("Taille duoctet            = %d\n", sizeof(duoctet));        // 2 octets = 16 bits
	printf("Taille char               = %d\n", sizeof(char));           // 1 octet  =  8 bits
	printf("Taille octet              = %d\n", sizeof(octet));          // 1 octet  =  8 bits
	printf("\n");

	// Char in C
	char D = 'A';
	printf("Caractere de controle 'A' char = %c, hexa = 0x%02x, int = %02d\n", D, D, D);
	printf("\n");

	// Getting the endian
	duoctet full = 0x4100;
	duoctet big  = full >> 8;
	char car = (char) big;
	printf("full = %04x, big = %04x, car = %c\n", full, big, car);
	printf("\n");

	//-------------------------------------------------------------------------
	// Reading files
	//-------------------------------------------------------------------------

	printf("Reading ANSI\n");
	FILE * fb = fopen("enc_ansi.txt", "rb");
	char * ansi = (char *) calloc(42, sizeof(char));
	fread(ansi, sizeof(char), 42, fb);
	fclose(fb);

	printf("Reading ISO-8859-1\n");
	fb = fopen("enc_iso-8859-1.txt", "rb");
	char * iso1 = (char *) calloc(42, sizeof(char));
	fread(iso1, sizeof(char), 42, fb);
	fclose(fb);

	printf("Reading UTF-8\n");
	fb = fopen("enc_utf-8.txt", "rb");
	char * utf8 = (char *) calloc(84, sizeof(char));
	fread(utf8, sizeof(char), 84, fb);

	printf("Reading UTF-16-BE\n");
	fb = fopen("enc_utf-16-be.txt", "rb");
	unsigned short * utf16be = (unsigned short *) calloc(84, sizeof(unsigned short));
	fread(utf16be, sizeof(unsigned short), 84, fb);

	printf("Reading UTF-8-small\n");
	fb = fopen("enc_utf-8-small.txt", "rb");
    int start = ftell(fb);
	printf("Start = %d\n", start);
    fseek(fb, 0L, SEEK_END);
    int size = ftell(fb);
	printf("Size = %d\n", size);
    fseek(fb, start, SEEK_SET); //go back to where we were
	unsigned char * u = (unsigned char *) calloc(size, sizeof(unsigned char));
	fread(u, sizeof(unsigned char), size, fb);

	for (int i = 0; i < size; i++) {
		if (u[i] < 124) {
			printf("%04u %02x ---- -- %c\n", u[i], u[i], u[i]);
		} else if (u[i] < 224 && i + 1 < size) {
			unsigned short s = u[i] + u[i + 1];
			printf("%04u %02x %04u %02x ", u[i], u[i], u[i + 1], u[i + 1]);
			if (s == 355) {
				printf("%c (a accent grave )\n", 133);
			} else {
				printf("%u\n", s);
			}
		}
	}

	char txt[11] = "a : int = 5";
	for (int i = 0; i < 11; i++) {
		printf("%c\n", txt[i]);
	}

	return 0;

	//-------------------------------------------------------------------------
	// Displaying characters
	//-------------------------------------------------------------------------

	for (int i = 0 ; i < 26; i++) { // 42
		printf("ansi = %c %04u %04x | iso1 = %c %04u %04x\n", 
			ansi[i], ansi[i], ansi[i], 
			iso1[i], iso1[i], iso1[i]);
	}

    return 0;
}
