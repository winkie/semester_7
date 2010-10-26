/* 2.5. [1] Напишите программу, которая печатает на стандартное устройство вывода */
/*      последние 10 строк файла и все строки, которые добавляются в конец файла */
/*      впоследствии (аналог tail -f). */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define NUM_LINES 10
#define BUF_SIZE 10

const char *program_name;

void print_help(const char *msg)
{
   if (msg)
      printf("%s\n", msg);
   printf("Usage: %s [-h, --help] [-f FILE]\n", program_name);
   exit(1);
}


void print_tail(FILE *f)
{
   char buffer[BUF_SIZE];
   int i, lines = 0;
   int read_bytes, file_size, slice = 1;
   int seek, size = BUF_SIZE;
   char flag = 1;
   int pos;
   
   fseek(f, 0, SEEK_END);
   file_size = ftell(f);
   
   while(flag)
   {
      seek = file_size - BUF_SIZE * slice;
      if (seek < 0)
      {
         seek = 0;
         flag = 0;
         size = (file_size - BUF_SIZE * (slice - 1));
      }

      int res = fseek(f, seek, SEEK_SET);
      read_bytes = fread(buffer, sizeof(char), size, f);
      
      for (i = read_bytes - 1; i >= 0; i--)
      {
         if (buffer[i] == '\n')
            lines++;
         
         if (lines == NUM_LINES + 1)
         {
            pos = seek + i + 1;
            flag = 0;
            break;
         }
      }
      slice++;
   }

   fseek(f, pos, SEEK_SET);

   while ((read_bytes = fread(buffer, sizeof(char), size, f)) > 0)
      fwrite(buffer, sizeof(char), read_bytes, stdout); 
}

void follow(FILE *f)
{
   int start_pos, end_pos;
   char buffer[BUF_SIZE];
   int size, i;
   
   struct timespec req;
   req.tv_sec = 0;
   req.tv_nsec = 300000000L; //300 milliseconds

   fseek(f, 0, SEEK_END);
   start_pos = ftell(f);
   
   while (1)
   {
      int res = nanosleep(&req, 0);
      int lines = 0;
      if (res == EINTR)
      {
         puts("Interrupted");
         exit(1);
      }

      fseek(f, 0, SEEK_END);
      end_pos = ftell(f);

      if (start_pos == end_pos)
         continue;

      size = end_pos - start_pos;

      fseek(f, start_pos, SEEK_SET);
      while (start_pos != end_pos)
      {
         int i, read = fread(buffer, sizeof(char), BUF_SIZE, f);
         start_pos += read;

         for (i = 0; i < read; i++)
            if (buffer[i] == '\n')
               lines++;
         fwrite(buffer, sizeof(char), read, stdout);
      }

      if (lines == 0)
      {
         puts("Retailing file!");
         print_tail(f);
         fseek(f, 0, SEEK_END);
         start_pos = ftell(f);
         continue;
      }
   }
}

int main(int argc, char **argv)
{
   const char *filename = 0;
   program_name = argv[0];

   if (argc == 2)
   {
      if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0)
         print_help(0);
      else
         print_help("Wrong command line");
   }
   else if (argc == 3)
   {
      if (strcmp(argv[1], "-f") != 0)
         print_help("Wrong command line");

      filename = argv[2];
   }
   else
   {
      print_help("Not enough or too much arguments");
   }
   
   FILE *f = fopen(filename, "r");
   
   print_tail(f);

   follow(f);
   
   return 0;
}
