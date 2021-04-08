#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <inttypes.h>

int main (void)
{
    FILE * fp;
    unsigned char *buffer;
    long filelen;
    fp = fopen("./input/utf8_lf.txt","rb");
    if (fp == NULL)
    {
        perror("ERROR");
        return 1;
    }
    fseek(fp, 0, SEEK_END);          // Jump to the end of the file
    filelen = ftell(fp);             // Get the current byte offset in the file
    rewind(fp);                      // Jump back to the beginning of the file
    buffer = (unsigned char *) malloc(filelen * sizeof(unsigned char)); // Enough memory for the file
    fread(buffer, filelen, 1, fp); // Read in the entire file
    //fprintf (fp, "Hello, there.\n"); // if you want something in the file.
    fclose(fp);
    for (int i=0; i < filelen; i++)
    {
        unsigned char bit_1     = buffer[i] & 0x80; // 0b10000000
        unsigned char bits_1to3 = buffer[i] & 0xE0; // 0b11100000
        if (bit_1 == 0)
        {
            printf("One bit:  ");
            if (buffer[i] == '\n')
            {
                printf("<NL>\n");
            }
            else if (buffer[i] == ' ')
            {
                printf("<SP>\n");
            }
            else
            {
                printf("%c\n", buffer[i]);
            }
        }
        else if (bits_1to3 == 0xC0)
        {
            unsigned char first = buffer[i];
            unsigned char second = buffer[i+1];
            i += 1;
            uint16_t combined = first * 256 + second;
            switch (combined)
            {
                case 0xC3A0:
                    printf("Two bits: à\n");
                    break;
                case 0xC3A7:
                    printf("Two bits: ç\n");
                    break;
                case 0xC3A8:
                    printf("Two bits: è\n");
                    break;
                case 0xC3A9:
                    printf("Two bits: é\n");
                    break;
                case 0xC3AA:
                    printf("Two bits: ê\n");
                    break;
                
                default:
                    printf("Two bits: <?>  = %u * 256 %u = %u\n", first, second, combined);
            }
        }
        else
        {
            printf("%c\n", buffer[i]);
        }
    }
    printf("File opened\n");
    return 0;
}

