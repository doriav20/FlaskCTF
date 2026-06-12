#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void validate_arguments(int argc, char* argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: is_admin <username>\n");
        exit(0);
    }
}

void validate_username(const char* username)
{
    if (username == NULL || username[0] == '\0')
    {
        fprintf(stderr, "Invalid username provided.\n");
        exit(0);
    }
}

FILE* open_file_for_reading(const char* file_path)
{
    return fopen(file_path, "r");
}

void close_file(FILE* file)
{
    if (file != NULL)
    {
        fclose(file);
    }
}

char* read_next_line(FILE* file, char* buffer, int buffer_size)
{
    if (fgets(buffer, buffer_size, file) == NULL)
    {
        return NULL;
    }

    buffer[strcspn(buffer, "\n")] = '\0';
    return buffer;
}

int string_equals(const char* str1, const char* str2)
{
    return str1 && str2 && strcmp(str1, str2) == 0;
}

int is_admin(const char* username)
{
    const char* admins_file_path = "/tmp/admins.txt";

    FILE* file = open_file_for_reading(admins_file_path);
    if (file == NULL)
    {
        return 0;
    }

    char line_buffer[256];
    while (read_next_line(file, line_buffer, sizeof(line_buffer) / sizeof(char)))
    {
        const char* admin_username = line_buffer;

        validate_username(line_buffer);

        if (string_equals(admin_username, username))
        {
            close_file(file);
            return 1;
        }
    }

    close_file(file);
    return 0;
}

int main(int argc, char* argv[])
{
    validate_arguments(argc, argv);

    char* input_username = argv[1];

    validate_username(input_username);

    if (is_admin(input_username))
    {
        printf("You are an admin!\n");
        return 1;
    }
    else
    {
        printf("You are not an admin.\n");
        return 0;
    }
}
