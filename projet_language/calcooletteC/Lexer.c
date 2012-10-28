#include "Lexer.h"

Token Token_init(char * str, TokenType type)
{
    Token t;
    t.class = TOKEN;
    string_copy(&t.str, str);
    t.type = type;
    return t;
}

Token Token_init_guess(char * cmd, int start, int end, TokenType gentype)
{
	char * str = substr(start, end, cmd);
    Token t = Token_init(str, gentype);
    TokenType type = gentype;
    if (TokenType_eq(&gentype, &ID) || TokenType_eq(&gentype, &OP)) 
        type = TokenType_get(str);
    t.type = type;
    return t;
}

Token make_token(char * str, int start, int end, TokenType ptt)
{
    Token t = Token_init_guess(str, start, end, ptt);
    printf("Token operator from %d to %d (len = %d) (type = %s): [%s]\n", start, end, strlen(t.str), TokenType_to_s(&t.type), t.str);    
    return t;
}

List * lex(char * cmd)
{
	
    List * list_tokens = List_create();
    
    State mode = START;
    int mode_start = 0;
    int mode_end = 0;
    printf("Nb char = %d\n", strlen(cmd));
    for(int i=0; i < strlen(cmd)+1; i++)
    {
        int v = (int)cmd[i];
        printf("%2d : %c (%d)\n", i, cmd[i], v);
        if (mode == START)
        {
            if (isalpha(v)) //((v >= 65 && v <= 90) || (v >= 97 && v <= 122))
            {
                mode = SYMBOL;
                mode_start = i;
            }
            else if (isdigit(v))
            {
                mode = INTEGER;
                mode_start = i;
            }
            else if (ispunct(v) && v != '#' && v != '"' && v!= '\'') // !"#$%&'()*+,-./ :;<=>?@ [\]^_` {|}~
            {
                mode = OPERATOR;
                mode_start = i;
            }
            else if (v == '#')
            {
                mode = COMMENT;
            }
            else if (v == '"')
            {
                mode = STRING_QQ;
                mode_start = i;
            }
            else if (v == '\'')
            {
                mode = STRING_Q;
                mode_start = i;
            }
            else if (v == '\n')
            {
                mode_start = i;
                mode_end = i;
                Token t = make_token(cmd, mode_start, mode_end, NEWLINE);
                List_add(list_tokens, &t, sizeof(Token));
            }
        }
        else if (mode == SYMBOL)
        {
            if (isalpha(v)) //((v >= 65 && v <= 90) || (v >= 97 && v <= 122))
            {
                // Nothing
            }
            else
            {
                mode = START;
                mode_end = i-1;
                Token t = make_token(cmd, mode_start, mode_end, ID);
                i-=1;
                List_add(list_tokens, &t, sizeof(Token));
            }
        }
        else if (mode == INTEGER)
        {
            if (isdigit(v))
            {
                // Nothing
            }
            else
            {
                mode = START;
                mode_end = i-1;
                Token t = make_token(cmd, mode_start, mode_end, INT);
                i-=1;
                List_add(list_tokens, &t, sizeof(Token));
            }
        }
        else if (mode == OPERATOR)
        {
            bool finish = true;
            char vv = '\0'; // On va chercher un troisieme pour differencier <= et <=>
            if (i < strlen(cmd))
                vv = cmd[i+1];
            
            if (ispunct(v))
            {
                if (i - mode_start == 1) // We are now at the second token for operator
                {
                    if (
                        //(cmd[mode_start] == '*' && v == '*') || // ** 
                        (cmd[mode_start] == '>' && v == '=') || // >=
                        (cmd[mode_start] == '<' && v == '=' && vv != '>') || // <=
                        (cmd[mode_start] == '=' && v == '=') || // == =?
                        (cmd[mode_start] == '!' && v == '=') || // != !?
                        (cmd[mode_start] == '<' && v == '<') || // <<
                        (cmd[mode_start] == '>' && v == '>') || // >>
                        (cmd[mode_start] == '+' && v == '=') ||
                        (cmd[mode_start] == '*' && v == '=') ||
                        (cmd[mode_start] == '-' && v == '=') ||
                        (cmd[mode_start] == '/' && v == '=') ||
                        (cmd[mode_start] == '/' && v == '/' && vv != '=') ||
                        (cmd[mode_start] == '%' && v == '=') ||
                        (cmd[mode_start] == '*' && v == '*' && vv != '='))                    
                    {
                        mode_end = i;
                        Token t = make_token(cmd, mode_start, mode_end, OP);
                        List_add(list_tokens, &t, sizeof(Token));
                        finish = false;
                        mode = START;
                    }
                    else if ((cmd[mode_start] == '<' && v == '=' && vv == '>') || // <=>
                             (cmd[mode_start] == '*' && v == '*' && vv == '=') || // **=
                             (cmd[mode_start] == '/' && v == '/' && vv == '='))   // //=
                    {
                        printf("3op %2d : %c (%d)\n", i+1, cmd[i+1], vv);
                        mode_end = i+1;
                        Token t = make_token(cmd, mode_start, mode_end, OP);
                        List_add(list_tokens, &t, sizeof(Token));
                        finish = false;
                        mode = START;
                        i+=1; // !!
                    }
                }
            }
            
            if (finish)
            {
                mode = START;
                mode_end = i-1;
                i-=1; // We don't take it
                Token t = make_token(cmd, mode_start, mode_end, OP);
                List_add(list_tokens, &t, sizeof(Token));
            }
        }
        else if (mode == COMMENT)
        {
            if (v == '\n')
                mode = START;
        }
        else if (mode == STRING_QQ || mode == STRING_Q)
        {
            if ((v == '"' && mode == STRING_QQ) || (v == '\'' && mode == STRING_Q))
            {
                mode_end = i;
                Token t = make_token(cmd, mode_start, mode_end, STR);
                List_add(list_tokens, &t, sizeof(Token));
                mode = START;
            }
        }
    }
    printf("LEXING DONE\n");
	return list_tokens;
}
