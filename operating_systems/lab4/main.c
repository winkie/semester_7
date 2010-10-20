#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <signal.h>
#include <stdlib.h>

#define N 5
#define LEFT(i) (i - 1 + N) % N
#define RIGHT(i) (i + 1) % N
enum STATE_TYPES
{
   THINKING,
   HUNGRY,
   EATING
};

pthread_mutex_t state_lock;
enum STATE_TYPES state[N];
sem_t philosopher_lock[N];

void catch_int(int sig_num)
{
   int i;
   pthread_mutex_destroy(&state_lock);
   for (i = 0; i < N; i++)
      sem_destroy(&philosopher_lock[i]);
   
   exit(0);
}

void test(int i)
{
   if (state[i] == HUNGRY && state[LEFT(i)] != EATING && state[RIGHT(i)] != EATING)
   {
      state[i] = EATING;
      sem_post(&philosopher_lock[i]);
   }
}

void take_forks(int i)
{
   pthread_mutex_lock(&state_lock);
   state[i] = HUNGRY;
   test(i);
   pthread_mutex_unlock(&state_lock);
   sem_wait(&philosopher_lock[i]);
}

void put_forks(int i)
{
   pthread_mutex_lock(&state_lock);
   state[i] = THINKING;
   test(LEFT(i));
   test(RIGHT(i));
   pthread_mutex_unlock(&state_lock);
}

void *philosopher(void *data)
{
   int id = (int)data;

   while (1)
   {
      printf("Philosopher %d is thinking\n", id);
      sleep(1);
      take_forks(id);
      printf("Philosopher %d is eating\n", id);
      sleep(3);
      put_forks(id);
   }
}

int main()
{
   int i;
   
   pthread_mutex_init(&state_lock, 0);
   for (i = 0; i < N; i++)
   {
      sem_init(&philosopher_lock[i], 0, 0);
      state[i] = THINKING;
   }
   
   signal(SIGINT, catch_int);

   for (i = 0; i< N; i++)
   {
      pthread_t thrd;
      pthread_create(&thrd, 0, philosopher, (void*)i);
   }

   pause();
   
   return 0;
}
