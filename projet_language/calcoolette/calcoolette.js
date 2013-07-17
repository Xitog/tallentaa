//
// Lexer         string  -> [tokens]
// Parser       [tokens] -> abstract syntax tree (AST)
// Interpreter    AST    -> result
//

DEBUG = true;

//-----------------------------------------------------------------------------
// Base
//-----------------------------------------------------------------------------

function SymbolType (name) {
    this.name = name;
}
 
SymbolType.prototype.toString = function() {
    return this.name;
};

// Types of Symbol

Integer     = new SymbolType('Integer');
Float       = new SymbolType('Float');
Id          = new SymbolType('Id');
Operator    = new SymbolType('Operator');
Separator   = new SymbolType('Separator');
Keyword     = new SymbolType('Keyword');
EOF         = new SymbolType('EOF');
Boolean     = new SymbolType('Boolean');
String      = new SymbolType('String');
Discard     = new SymbolType('Discard');
Error       = new SymbolType('Error');
Structure   = new SymbolType('Structure');

function Symbol(kind, val, left, right) {
    this.kind = kind;
    this.val = val;
    this.left = typeof left !== 'undefined' ? left : null;
    this.right = typeof right !== 'undefined' ? right : null;
}

Symbol.prototype.toString = function() {
    if (this.left == null && this.right == null) {
        return "" + this.val + ":" + this.kind;
    } else if (this.right == null && this.left != null) {
        return "" + this.left + "--" + this.val + ":" + this.kind;
    } else if (this.left == null && this.right != null) {
        return "" + this.val + ":" + this.kind + "--" + this.right;
    } else {
        return "" + this.left + "--" + this.val + ":" + this.kind + "--" + this.right;
    }
}

Symbol.prototype.terminal = function() {
        return this.left == null && this.right == null;
}

//-----------------------------------------------------------------------------
// Lexical analyzer
//
// Stream of characters => List of terminal symbols (tokens)
//
// class Lexer
//      attr symbols[]
//      op tokenize
//      op read_num
//      op read_id
//      op read_operator
//      op clear
//      op test
//-----------------------------------------------------------------------------

// Authorized characters
digits = ['0','1','2','3','4','5','6','7','8','9'];
alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_'];
ops = ['+', '-', '*', '/', '**', '%', '.', '<', '>', '!', '=', ':'];
white = [' ', '\n', '\t'];
operators = ['+', '-', '*', '/', '**', '%', '.', '<', '<<', '<=', '>', '>>', '>=', '!=', '==', '<=>', '=', '//', ':'];
separators = ['(', ')', ';', ','];
id_booleans = ['true', 'True', 'False', 'false'];
id_operators = ['and', 'xor', 'or'];
id_keywords = ['class', 'fun', 'return', 'next', 'break', 'unless', 'until', 'do', 'while', 'end', 'elsif', 'else', 'then', 'if', 'module'];
spe = ['$', '?'];
comment = ['#'];

// Constructor
function Lexer() {
    this.symbols = [];
}

// Main function. From a stream of characters produces a list of terminal symbols (tokens).
Lexer.prototype.tokenize = function(input) {
    this.symbols = [];
    i = 0;
    while (i < input.length) {
        if (digits.indexOf(input[i]) > -1) { 
            i = this.read_num(input, i); 
        } else if (alphas.indexOf(input[i]) > -1) { 
            i = this.read_id(input, i); 
        } else if (ops.indexOf(input[i]) > -1) { 
            i = this.read_op(input, i); 
        } else if (white.indexOf(input[i]) > -1) { 
            i += 1; 
        } else if (separators.indexOf(input[i]) > -1) {
            this.symbols.push(new Symbol(Separator, input[i]));
            i += 1;
        } else if (comment.indexOf(input[i]) > -1) {
            while (i < input.length && input[i] != '\n' && input[i] != ';') {
                i += 1;
            }
        } else {
            alert("Char incorrect " + input[i] + " at " + i);
        }
    }
    //this.symbols.push(new Symbol(EOF, 'eof'));
    return this.symbols; // SymbolList(self.symbols)
}

// Read a number
Lexer.prototype.read_num = function(input, i) {
    is_float = false;
    num = input[i];
    i +=1;
    cont = true;
    while (i < input.length && cont) {
        if (digits.indexOf(input[i]) > -1) {
            num += input[i];
            i +=1;
        } else if (input[i] == '.') {
            if (! is_float && i+1 < input.length && digits.indexOf(input[i+1]) > -1) {
                is_float = true;
                num += input[i];
                i +=1;
            } else if (! is_float && i+1 < input.length && input[i+1] == '.') {
                is_float = true;
                num += input[i];
                i +=1;
                cont = false;
            } else if (! is_float && i+1 == input.length) {
                is_float = true;
                num += input[i];
                i +=1;
                cont = false;
            } else {
                cont = false;
            }
        } else if (alphas.indexOf(input[i]) > -1) {
            alert("Incorrect Id starting with numbers");
        } else {
            cont = false;
        }
    }
    if (! is_float) {
        this.symbols.push(new Symbol(Integer, num));
    } else {
        this.symbols.push(new Symbol(Float, num));
    }
    //console.log("num : " + num);
    //console.log("i = " + i);
    return i;
}

// Read an id
Lexer.prototype.read_id = function(input, i) {
    id = input[i];
    i +=1;
    cont = true;
    while (i < input.length && cont) {
        if (alphas.indexOf(input[i]) > -1 || digits.indexOf(input[i]) > -1) {
            id +=input[i];
            i +=1;
        }
        // si i == $ ou ? et que c le dernier ou que i+1 != digits et i+1 != alphas alors
        else if (spe.indexOf(input[i]) > -1 && (i == input.length-1 || (digits.indexOf(input[i+1]) == -1 && alphas.indexOf(input[i+1]) == -1))) {
            id +=input[i];
            i +=1;
        } else {
            cont = false;
        }
    }
    if (id_booleans.indexOf(id) > -1) {
        this.symbols.push(new Symbol(Boolean, id));
    } else if (id_operators.indexOf(id) > -1) {
        // operator boolean as function
        if (this.symbols.length > 1 && i > 0 && this.symbols[this.symbols.length-1].val == '.') {
            this.symbols.push(new Symbol(Id, id));
        } else {
            this.symbols.push(new Symbol(Operator, id));
        }
    } else if (id_keywords.indexOf(id) > -1) {
        // keyword as function
        if (this.symbols.length > 1 && i > 0 && this.symbols[this.symbols.length-1].val == '.') {
            this.symbols.push(new Symbol(Id, id));
        } else {
            this.symbols.push(new Symbol(Keyword, id));
        }
    } else {
        this.symbols.push(new Symbol(Id, id));
    }
    return i;
}

// Read an operator
Lexer.prototype.read_op = function(input, i) {
    op = input[i];
    i +=1;
    cont = true;
    while (op != '-' && i < input.length && cont) {
        if (ops.indexOf(input[i]) > -1 && input[i] != '-') {
            op += input[i];
            i +=1;
        } else {
            cont = false;
        }
    }
    if (operators.indexOf(op) == -1) {
        alert("Not known operator : " + op)
    }
    this.symbols.push(new Symbol(Operator, op))
    return i
}

Lexer.prototype.clear = function() {
    this.symbols = [];
}

// Tests
Lexer.prototype.test = function(input, result) {
    this.clear();
    this.tokenize(input);
    r = true;
    if (this.symbols.length != result.length) {
        console.log("length!");
        r = false;
    } else {
        for (i = 0; i < result.length; i++) {
            //console.log(this.symbols[i].val);
            //console.log(result[i][0].toString());
            if (this.symbols[i].val != result[i][0].toString() || this.symbols[i].kind != result[i][1]) {
                r = false;
                break;
            }
        }
    }
    if (DEBUG) {
        for (i = 0; i < this.symbols.length; i += 1) {
            console.log("" + i + ". " + this.symbols[i]);
        }
    }
    return r;
}

test_lexer = new Lexer();
test_lexer.test("4", [[4, Integer]]) ? console.log("=> 4 OK") : console.log("ERROR : 4");
test_lexer.test("4.0", [["4.0", Float]]) ? console.log("=> 4.0 OK") : console.log("ERROR : 4.0");
test_lexer.test("4.", [["4.", Float]]) ? console.log("=> 4. OK") : console.log("ERROR : 4.");
test_lexer.test("4..", [["4.", Float], [".", Operator]]) ? console.log("=> 4.. OK") : console.log("ERROR : 4..");
test_lexer.test("4..to_f", [["4.", Float], [".", Operator], ["to_f", Id]]) ? console.log("=> 4..to_f OK") : console.log("ERROR : 4..to_f");
test_lexer.test("4.to_f", [[4, Integer], [".", Operator], ["to_f", Id]]) ? console.log("=> 4.to_f OK") : console.log("ERROR : 4.to_f");
test_lexer.test("true", [[true, Boolean]]) ? console.log("=> true OK") : console.log("ERROR : true");
test_lexer.test("true or false", [[true, Boolean], ["or", Operator], [false, Boolean]]) ? console.log("=> true or false OK") : console.log("ERROR : true or false");

cmd = "2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3";
result = [[2, Integer], ["+", Operator], [3, Integer], ["-", Operator], [4, Integer], [".", Operator], ["to_f", Id], ["+", Operator], ["(", Separator], ["true", Boolean], [")", Separator], ["or", Operator], ["False", Boolean], ["xor", Operator], ["True", Boolean], ["**", Operator], [2.3, Float], ["+", Operator], ["0.3", Float], [".", Operator], ["to_i", Id], ["/", Operator], [0, Integer], [".", Operator], ["to_f", Id], ["/", Operator], ["0.", Float], [".", Operator], ["to_f", Id], ["+", Operator], ["-", Operator], [3, Integer]];
test_lexer.test(cmd, result) ? console.log("=> 2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3 OK") : console.log("ERROR : 2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3");

//-----------------------------------------------------------------------
// Syntaxic analysis (Expression)
//-----------------------------------------------------------------------
/*
function Parser() {
    this.tree = null;
}

// Fetch the operator with the highest priority to execute
Parser.prototype.first_op = function(symbols) {
    i = 0;
    best = -1;
    best_prio = -1;
    prio = { ')' : 0, ',' : 1, 'and' : 5, 'or' : 5, 'xor' : 5, 
             '>' : 8, '<' : 8, '>=' : 8, '<=' : 8, '==' : 8, '!=' : 8, '<=>' : 8, 
             '<<': 9, '>>' : 9, '+' : 10, '-' : 10, 
             '*' : 20, '/' : 20, '//' : 20, '**' : 30, '%' : 30, 'call' : 35, '.' : 40, 
             'unary-' : 50, 'call(' : 51, 'expr(' : 60 };
    lvl = 1;
    while (i < symbols.length) {
        symb = symbols[i];
        if (symb.terminal() && (symb.kind == Operator || symb.kind == Separator)) {
            if (best == -1) {
                best = i
                best_prio = prio[symb.val]*lvl
            } else {
                if (prio[symb.val]*lvl > best_prio) {
                    best = i
                    best_prio = prio[symb.val]*lvl
                }
            }
            // () for others
            if (symb.val == 'call(' || symb.val == 'expr(') {
                lvl*=10
            } else if (symb.val == ')') {
                lvl/=10
            }
        } else if (symb.val == 'call(') { // not terminal
            if (prio[symb.val]*lvl > best_prio) {
                best = i
                best_prio = prio[symb.val]*lvl
            } else {
                alert("Incorrect expression call");
            }
        }
        i +=1;
    }
    if (best == -1) {
        alert("Incorrect expression");
    }
    return best;
}

Parser.prototype.fetch_closing = function(sep, symbols, i) {
    lvl = 0;
    pos = 0;
    pos = i;
    while (pos < symbols.length) {
        symb = symbols[pos];
        if (sep == '(' && (symb.val == 'call(' || symb.val == 'expr(')) {
            lvl += 1;
        } else if (sep == '(' && symb.val == ')') {
            lvl -= 1;
        }
        if (lvl == 0) {
            break;
        }
        pos += 1;
    }
    if (lvl != 0) {
        alert("Incorrect expression ()");
    }
    return pos;
}

Parser.prototype.not_exist_or_dif = function(symbols, index, terminal, value) {
    if (symbols.length <= index) {
        return true;
    }
    if (symbols[index].terminal() != terminal) {
        return true;
    }
    if (symbols[index].val != value) {
        return true;
    }
    return false;
}

// highlighting differences between :
//     - (unary) et - (binary)
//     () (call) et () (expr)
Parser.prototype.prepare = function(symbols) {
    i = 0;
    while (i < symbols.length) {
        symb = symbols[i];
        if (symb.terminal()) {
            if (symb.val == '-' && (i == 0 || symbols[i-1].kind == Operator)) {
                symb.val = 'unary-';
            }
            // () -> x
            if (symb.val == '(' && i < symbols.length-1 && symbols[i+1].val == ')') {
                symbols.splice(i+1 , 1);
                symbols.splire(i, 1);
                i-=1;
            }
            //
            if (symb.val == '(' && i > 0 && symbols[i-1].kind != Operator) {
                symb.val = 'call(';
            } else if (symb.val == '(') {
                symb.val = 'expr(';
            }
        i+=1;
        }
    }
}

p = new Parser();
console.log(p.first_op(tokens));
*/