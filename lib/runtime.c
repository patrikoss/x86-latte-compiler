#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define EXIT_FAIL_CODE 1

void printInt(int n){
    printf("%d\n", n);
}

void printString(char *s){
    printf("%s\n", s);
}

void _error(char* err){
    printf("%s\n", err);
    exit(EXIT_FAIL_CODE);
}

void error(){
    _error("Runtime error");
}

int readInt(){
    int n;
    if (scanf("%d\n", &n) == EOF) {
        _error("Runtime error: readInt failed");
    }
    return n;
}

char *readString(){
    char* line = NULL;
    size_t len = 0;
    ssize_t read = getline(&line, &len, stdin);
    if (read == -1){
        _error("Runtime error: readString failed.");
    }
    if (line[read-1]=='\n'){
        read--;
        line[read] = '\0';
    }
    return line;
}

char *concat(char *str1, char *str2){
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    char *newStr = malloc(len1+len2+1);
    if (newStr == NULL){
        _error("Runtime error: concat");
    }
    strcpy(newStr, str1);
    strcat(newStr, str2);
    return newStr;
}
