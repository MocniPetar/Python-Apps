#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define END (0)
#define ERROR (-1)
#define MAX_NUM_OF_CHAR (256)

struct stog;
struct postfix;
typedef struct stog *pos;
typedef struct postfix *Pos;

typedef struct stog{
    char sign[MAX_NUM_OF_CHAR];
    pos next;
}S;

typedef struct postfix{
    char PostFix[MAX_NUM_OF_CHAR];
    Pos next;
}P;

Pos readFromFile(char*);
Pos oprStog(pos, pos, Pos, char*);
Pos addToPost(pos, Pos, char*);
int convertToString(Pos);
int Push(Pos, char*);
int push(pos, char*);
int pop(pos);
void freeMemory(Pos);

static int count = 0;
char postfix[MAX_NUM_OF_CHAR] = {0};

const char* PythonFunction(char *Infix){

    Pos izrazi = NULL;
    izrazi = readFromFile(Infix);
    if(izrazi == NULL)
        return "ERROR";
    convertToString(izrazi);
    freeMemory(izrazi);
    return postfix;
}

Pos readFromFile(char *FileName){

    char buffer[MAX_NUM_OF_CHAR], opr[MAX_NUM_OF_CHAR] = {0};
    char *p = NULL;
    int check = 0, n = 0, i = 0, one_expression = 1;
    Pos izraz = NULL, post_temp = NULL, q_p = NULL;
    pos stog_temp = NULL, start = NULL, prev_ = NULL;

    izraz = (Pos)malloc(sizeof(P));
    strcpy(buffer,FileName);

    P Post = { .PostFix = {0}, .next = NULL };
    S Stog = { .sign = {0}, .next = NULL };
    post_temp = &Post;
    stog_temp = &Stog;
    p = buffer;
    while(strlen(p) > 0){
        q_p = (Pos)malloc(sizeof(P));
        if(sscanf(p,"%d %n", &check, &n) <= 0){
            sscanf(p,"%s %n", opr, &n);
            post_temp = oprStog(&Stog, stog_temp, post_temp, opr);
            stog_temp = stog_temp->next;
            if(stog_temp == NULL){
                stog_temp = &Stog;
                stog_temp = stog_temp->next;
            }
        }
        else {
            sscanf(p,"%s %n", opr, &n);
            Push(post_temp,opr);
            post_temp = post_temp->next;
        }
        p+=n;
    }
        
    stog_temp = start = prev_ = &Stog;
    while(start->next != NULL){
        while(stog_temp->next != NULL){
            prev_ = stog_temp;
            stog_temp = stog_temp->next;
        }
        Push(post_temp,stog_temp->sign);
        post_temp = post_temp->next;
        pop(prev_);
        stog_temp = start;
    }
    izraz = &Post;
    return izraz;
}

Pos addToPost(pos oper, Pos p, char *opr){

    pos start = NULL, temp = NULL, tmp = NULL;
    temp = start = tmp = oper;

    while(start->next != NULL){
        while(temp->next != NULL){
            tmp = temp;
            temp = temp->next;
        }
        Push(p,temp->sign);
        p = p->next;
        tmp->next = NULL;
        free(temp);
        temp = start;
    }
    push(start,opr);

    return p;
}

Pos oprStog(pos s_head, pos s_curr , Pos p, char *opr){

    if(s_head == NULL)
        return NULL;

    if(strcmp(s_curr->sign,opr) != 0 && (strcmp(s_curr->sign,"*") == 0 || strcmp(s_curr->sign,"/") == 0)){
        if(strcmp(opr,"+") == 0 || strcmp(opr,"-") == 0)
            p = addToPost(s_head,p,opr);
        else
            push(s_curr,opr);
    }
    else
        push(s_curr,opr);

    return p;
}

int Push(Pos s, char *post){

    if(s == NULL)
        return ERROR;
    Pos q = NULL;
    q = (Pos)malloc(sizeof(P));
    strcpy(q->PostFix,post);
    q->next = s->next;
    s->next = q;

    return END;
}

int push(pos s, char *opr){

    if(s == NULL)
        return ERROR;
    pos q = NULL;
    q = (pos)malloc(sizeof(S));
    strcpy(q->sign,opr);
    q->next = s->next;
    s->next = q;

    return END;
}

int pop(pos s){

    if(s == NULL)
        return ERROR;
    pos temp = NULL;
    temp = s->next;
    s->next = s->next->next;
    free(temp);

    return END;
}
int convertToString(Pos p){

    if(p == NULL)
        return ERROR;       
    while(p->next != NULL){
        strcat(postfix,p->next->PostFix);
        strcat(postfix," ");
        p = p->next;
    }
    return END;
}

void freeMemory(Pos p){
    Pos temp = NULL;
    while(p->next != NULL){
        temp = p->next;
        p->next = temp->next;
        free(temp);
    }
}