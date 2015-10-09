#include <stdio.h>
#include <pthread.h>
#define NUM_THREADS 10 

void *countFiveMM(void *threadid)
{
    int count = 0;
    while ( count != 5000000)
    {
        count++;
    }
    printf("Thread finished with count of = %d \n", count);
    pthread_exit(NULL);
}
               
int main()
{
    pthread_t threads[NUM_THREADS];
    long t;    

    for(t=0; t<NUM_THREADS; t++){
      pthread_create(&threads[t], NULL, *countFiveMM, (void *)t);
   }
    
    printf("done!");
    pthread_exit(NULL);
}
