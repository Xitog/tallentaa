// MACHINE VIRTUELLE ZEMBLA

#include "zembla.h"

#define LOAD_INT     0x00000001 // 1
#define LOAD_REF_INT 0x00000002 // 2
#define LOAD_ADDR	 0x00000003 // 3

#define STORE        0x00000010 // 16

#define GT           0x00000100 // 256

#define JMP_FALSE    0x00001000 // 4096
#define JUMP_NEG     0x00003000 // 12288

#define END	  	     0x00010000 // 65536

#define ADD_INT      0x00100000 // 1048576

#define PRINT_INT	 0x01000000

long a[32];
long vars[32];
long vars_ptr;
long stack[32];
long stack_ptr;

// ATTENTION AUX SAUTS !!!
void instruction_init(void) {
	a[0] = LOAD_INT;		// i = 0					1
	a[1] = 0x00000000;
	a[2] = LOAD_ADDR;		//							3
	a[3] = 0x00000000;
	a[4] = STORE;			//							16
	a[5] = LOAD_INT;		// while 5 > i do			1
	a[6] = 0x00000005;
	a[7] = LOAD_REF_INT;	//							2
	a[8] = 0x00000000;
	a[9] = GT;				//							256
	a[10]= JMP_FALSE;		//							4096
	a[11]= 0x0000000E;
	a[12]= PRINT_INT;		// print i
	a[13]= 0x00000000;
	a[14]= LOAD_INT;		// i += 1					1
	a[15]= 0x00000001;
	a[16]= LOAD_REF_INT;	//							2
	a[17]= 0x00000000;
	a[18]= ADD_INT;			//							1048576
	a[19]= LOAD_ADDR;		//							3
	a[20]= 0x00000000;
	a[21]= STORE;			//							16
	a[22]= JUMP_NEG;		// end						12288
	a[23]= 0x00000011;
	a[24]= END;				//							65536
}

void go(void) {
	printf("size long = %d\n\n", sizeof(long));

	instruction_init();
	long cpt = 0;
	long val = a[cpt];

	printf("instructions :\n");
	while (val != END) {
		printf("%d.\t0x%08.8X\n", cpt, val);
		cpt += 1;
		val = a[cpt];
	}
	printf("%d.\t0x%08.8X\n\n", cpt, val);

	vars[0] = -1;
	stack_ptr = 0;
	cpt = 0;
	while (1) {
		//printf("order=%d, cpt=%d, stack_ptr=%d\n", a[cpt], cpt, stack_ptr);

		val = a[cpt];
		if (val == LOAD_INT) {
			//printf("\tje charge %d dans la pile !\n", a[cpt+1]);
			stack[stack_ptr] = a[cpt+1];
			stack_ptr+=1;
			cpt+=2;
		} else if (val == LOAD_ADDR) {
			//printf("\tje charge une addr\n");
			stack[stack_ptr] = a[cpt+1];
			stack_ptr+=1;
			cpt+=2;
		} else if (val == STORE) {
			//printf("\tje store\n");
			long addr = stack[stack_ptr-1];
			long value = stack[stack_ptr-2];
			vars[addr] = value;
			stack_ptr-=2;
			cpt+=1;
		} else if (val == LOAD_REF_INT) {
			stack[stack_ptr] = vars[a[cpt+1]];
			stack_ptr+=1;
			cpt+=2;
		} else if (val == GT) {
			long op1 = stack[stack_ptr-2];
			long op2 = stack[stack_ptr-1];
			stack_ptr-=2;
			stack[stack_ptr] = op1 > op2;
			stack_ptr+=1;
			cpt+=1;
		} else if (val == JMP_FALSE) {
			if (!stack[stack_ptr-1]) {
				//printf("\tje jump a %d !\n", cpt+a[cpt+1]);
				cpt+=a[cpt+1];
			} else {
				cpt+=2;
			}
			stack_ptr-=1; // pop
		} else if (val == ADD_INT) {
			long op1 = stack[stack_ptr-1];
			long op2 = stack[stack_ptr-2];
			stack_ptr-=2;
			stack[stack_ptr] = op1 + op2;
			stack_ptr+=1;
			cpt+=1;
		} else if (val == JUMP_NEG) {
			cpt -= a[cpt+1];
		} else if (val == PRINT_INT) {
			printf("%d\n", vars[a[cpt+1]]);
			cpt+=2;
		} else if (val == END) {
			break;
		}
	
		/*
		long x = stack_ptr;
		printf("\t(%d)[", stack_ptr);
		while (x > 0) {
			printf("%d, ", stack[x-1]);
			x-=1;
		}
		printf("]\n");
		printf("\ti=%d\n", vars[0]);
		*/

		//system("pause");
	}
}
