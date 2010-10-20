/* 3.7. [3] Постройте модель регулируемого перекрестка, представив каждый из двух */
/*      светофоров отдельным процессом. */

/*      В нормальном состоянии светофор, разрешающий движение по Большому */
/*      проспекту, горит зеленым светом, а светофор, разрешающий движение по */
/*      Поперечной улице - красным. При нажатии ^C светофор Большого проспекта */
/*      меняет свет с зеленого на желтый. Через 5 секунд светофор Большого */
/*      проспекта переключается на красный свет, а светофор Поперечной улицы - с */
/*      красного на зеленый. Проходит 20 секунд. Светофор Поперечной улицы */
/*      переключается на желтый. Еще через 5 секунд светофор Поперечной улицы */
/*      загорается красным, а светофор Большого проспекта переключается с красного */
/*      на зеленый. Перед следующим переключением светофора на Большом проспекте */
/*      должно пройти не меньше 20 секунд. После нажатия ^C все последующие нажатия */
/*      этих клавиш в течение цикла переключения светофоров игнорируются. */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>

pid_t other_lights;
void big_to_red();

void big_catch_int(int sig_num)
{
   sigset_t mask, old_mask;
   sigemptyset(&mask);
   sigaddset(&mask, SIGINT);
   sigprocmask(SIG_BLOCK, &mask, NULL);
   big_to_red();
   sleep(20);
   sigprocmask(SIG_UNBLOCK, &mask, NULL);
}

void big_catch_usr1(int sig_num)
{
   puts("Big: Green");
}

void big_to_red()
{
   sleep(5);
   puts("Big: Red");
   kill(other_lights, SIGUSR1);
   signal(SIGUSR1, big_catch_usr1);
   pause();
}

int big_road_lights()
{
   puts("Big: Green");
   for (;;)
   {
      signal(SIGINT, big_catch_int);
      pause();
   }
}

void small_catch_usr1(int sig_num)
{
   puts("Small: Green");
   sleep(20);
   puts("Small: Yellow");
   sleep(5);
   puts("Small: Red");
   kill(other_lights, SIGUSR1);
}

int small_road_lights()
{
   sigset_t mask, old_mask;
   sigemptyset(&mask);
   sigaddset(&mask, SIGINT);
   sigprocmask(SIG_BLOCK, &mask, NULL);
   for (;;)
   {
      signal(SIGUSR1, small_catch_usr1);
      pause();
   }
   sigprocmask(SIG_UNBLOCK, &mask, NULL);
}

int main()
{
   pid_t small_pid = fork();
   if (small_pid == 0)
   {
      other_lights = getppid();
      small_road_lights();
      _exit(0);
   }
   else if (small_pid > 0)
   {
      other_lights = small_pid;
      big_road_lights();
      exit(0);
   }
   else
   {
      printf("Can't fork, error %d\n", errno);
      return EXIT_FAILURE;
   }
}




