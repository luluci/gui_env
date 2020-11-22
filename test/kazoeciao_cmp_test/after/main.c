#include <stdio.h>

int main(void) {
	int count;

	for (count=1; count<10; count++) {
		if	(count % 15 == 0)	printf("FizzBuzz");
		else if	(count % 3  == 0)	printf("Fizz");
		else if	(count % 5  == 0)	printf("Buzz");
		else				printf("%d", count);
		if	(count<10)		printf(", ", count);
	}
	printf("\r\n");

	return 0;
}
