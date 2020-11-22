#include <stdio.h>

int main(void) {
	int count;

	for (count=1; count<10; count++) {
		if	(count % 15 == 0)	printf("FizzBuzz\r\n");
		else if	(count % 3  == 0)	printf("Fizz\r\n");
		else if	(count % 3  == 0)	printf("Buzz\r\n");
		else				printf("%d\r\n", count);
	}

	return 0;
}
