//
// Symbolizer  string   -> [tokens]
// Parser      [tokens] -> abstract syntax tree (AST)
// Interpreter AST      -> result
//

//-----------------------------------------------------------------------
// Base
//-----------------------------------------------------------------------

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

// MISSING SYMBOL LIST

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

// From a string make a list of symbol
function Symbolizer() {
    this.symbols = [];
}
    
Symbolizer.prototype.parse = function(input) {
    this.symbols = [];
    i = 0;
    while (i < input.length) {
        if (digits.indexOf(input[i]) > -1) { 
            i = this.parse_num(input, i); 
        } else if (alphas.indexOf(input[i]) > -1) { 
            i = this.parse_id(input, i); 
        } else if (ops.indexOf(input[i]) > -1) { 
            i = this.parse_op(input, i); 
        } else if (white.indexOf(input[i]) > -1) { 
            i += 1; 
        } else if (separators.indexOf(input[i]) > -1) {
            this.symbols.push(new Symbol(Separator, input[i]));
            i +=1;
        } else {
            alert("Char incorrect " + input[i] + " at " + i);
        }
    }
    this.symbols.push(new Symbol(EOF, 'eof'));
    return this.symbols; // SymbolList(self.symbols)
}

// 23h32 : ok
Symbolizer.prototype.parse_num = function(input, i) {
    is_float = false;
    num = input[i];
    i +=1;
    cont = true;
    while (i < input.length && cont) {
        if (digits.indexOf(input[i]) > -1) {
            num += input[i];
            i +=1;
        } else if (input[i] == '.' && ! is_float && i+1 < input.length && digits.indexOf(input[i+1]) > -1) {
            is_float = true;
            num += input[i];
            i +=1;
        } else if (input[i] == '.' && ! is_float && i+1 < input.length && input[i+1] == '.') {
            is_float = true;
            num += input[i];
            i +=1;
            cont = false;
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
    console.log("num : " + num);
    console.log("i = " + i);
    return i;
}

// 23h48 : ok
Symbolizer.prototype.parse_id = function(input, i) {
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

Symbolizer.prototype.parse_op = function(input, i) {
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

Symbolizer.prototype.clear = function() {
    this.symbols = [];
}

// 00h15 : ça marche !
cmd = "2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3";
s = new Symbolizer();
tokens = s.parse(cmd);
console.log(tokens);
for (i = 0; i < tokens.length; i += 1) {
    console.log("" + i + ". " + tokens[i]);
}

//-----------------------------------------------------------------------
// Syntaxic analysis (Expression)
//-----------------------------------------------------------------------
