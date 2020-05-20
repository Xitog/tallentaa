#include <stdio.h>
#include <stdlib.h>

typedef unsigned short int octet;

int main(int argc, char * argv[]) {
    FILE * f = fopen("test.ash", "r");
    char * dest = calloc(200, sizeof(char));
    fread(dest, 100, 100, f);
    printf("%s\n", dest);
    fclose(f);

	printf("%d\n", sizeof(unsigned short)); // 2 octets = 16 bits

	printf("Reading file utf-16-be.txt\n");
	FILE * fb;
	fb = fopen("utf-16-be.txt", "rb");
	octet * buffer = (octet *) calloc(100, sizeof(octet));
	fread(buffer, sizeof(octet), 100, fb);
	octet index = 0;
	octet content = buffer[index];
	while (content != 0) {
		content = buffer[index];
		printf("%d %x\n", content, content);
		index += 1;
	}
	fclose(fb);

    return 0;
}
