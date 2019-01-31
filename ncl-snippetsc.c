#include "stdio.h"

int main()
{
    FILE *sublime_snippets=NULL;
    FILE *vscode_snippets=NULL;
    char soure[300], outNAME[300], *point=NULL;
    int flag=0, i=0, j=0;

    sublime_snippets = fopen("NCL.sublime-completions","r");
    vscode_snippets = fopen("snippets.json","w+");

    if (sublime_snippets==NULL) {
        printf("SOUCE FILE OPEN ERROR");
        return 1;
    }
    else if (vscode_snippets==NULL) {
        printf("TARGET FILE OPEN ERROR");
        return 1;
    }
    
    fprintf(vscode_snippets,"{\n");
    while(fgets(soure,300,sublime_snippets) != NULL){
        i=0;
        flag=0;
        point=NULL;
        j=1;
        outNAME[0]=0;
        while( soure[i] != '}' ){
            if ( soure[i] == '"' ) {
                flag++;
                if ( flag == 3 ) {
                    point=&soure[i];
                    sscanf(point,"%s",outNAME);
                    for(; outNAME[j] != '\0'; j++)
                    {
                        if( outNAME[j] == '"' ){
                            outNAME[j+1] = '\0';
                        }
                    }
                }
                else if ( flag == 7 ) {
                    point=&soure[i];
                    break;
                }
            }
            i++;
        }
        fprintf(vscode_snippets,"\t%s: {\n\t\t\"prefix\": %s,\n\t\t\"body\": %s",outNAME,outNAME,point);
    }
    fprintf(vscode_snippets,"}\n");

    fclose(sublime_snippets);
    fclose(vscode_snippets);

    return 0;
}
