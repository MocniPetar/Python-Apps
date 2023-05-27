#define _CRT_SECURE_NO_WARNINGS

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define END (0)
#define ERROR (-1)
#define ERROR_1 (-2.0002) // The operation or value is not correct!
#define ERROR_2 (-3.0003) // There is more than one element left in stack!
#define ERROR_3 (-4.0004) // Undefined!
#define MAX_LINE (256)

struct Stog;
typedef struct Stog* Position;
struct Stog {
    float broj;
    Position next;
} *head = NULL; 

int Push(float);
float Pop();
float Calculate(char*);

const float PythonFunction(char *Postfix){

    float result = 0.0;
    result = Calculate(Postfix);
    if(result == -1){
        return -1;
    }
    free(head);
    return result;
}

float Calculate(char* buffer) {
     
    char mark[MAX_LINE] = { 0 };
    char* p = NULL;
    float num1 = 0.0, num2 = 0.0, value=0.0;
    int n = 0;

    p = buffer;

    while (strlen(p) > 0)
    {
        if (sscanf(p, "%f %n", &value, &n) <= 0){
            sscanf(p, "%s %n", mark, &n);

            if (strcmp(mark, "+") != 0 && strcmp(mark, "-") != 0 && strcmp(mark, "*") != 0 && strcmp(mark, "/") != 0)
                return ERROR_1;

            if (head == NULL || head->next == NULL)
                return ERROR_2;
    
            num1 = Pop();
            num2 = Pop();
            
            if (strcmp(mark, "+") == 0) 
                Push(num2 + num1);

            else if (strcmp(mark, "-") == 0)
                Push(num2 - num1);

            else if (strcmp(mark, "*") == 0)
                Push(num2 * num1);

            else{
                if (num1 == 0.0) {
                    Pop();
                    return ERROR_3;
                }
                else
                    Push(num2 / num1);
            } 
        }
        else 
            Push(value);
        p += n;
    }
        
    if (head != NULL && head->next == NULL) {
        return Pop();
    }

    return ERROR_2;
}

int Push(float x){

    Position temp =NULL;
    temp = (Position)malloc(sizeof(struct Stog));

    temp->broj = x;
    temp->next = NULL;

    temp->next = head;
    head = temp;

    return END;
}

float Pop(){

    Position temp;
    float result = 0.0;

    if(head == NULL)
        return ERROR;

    temp = head;
    result = temp->broj;

    head = head->next;
    free(temp);
    temp = NULL;

    return result;
}