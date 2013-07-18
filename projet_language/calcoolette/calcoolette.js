//
// Lexer         string  -> [tokens]
// Parser       [tokens] -> abstract syntax tree (AST)
// Interpreter    AST    -> result
//

DEBUG = true;

//-----------------------------------------------------------------------------
// Base
//-----------------------------------------------------------------------------

var SymbolType = {
    Integer : 'Integer',
    Float : 'Float',
    Id : 'Id',
    Operator : 'Operator',
    Separator : 'Separator',
    Keyword : 'Keyword',
    Boolean : 'Boolean',
    String : 'String',
    //Discard : 'Discard',
    //Error : 'Error',
    Structure : 'Structure',
};

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
id_booleans = ['true', 'True', 'TRUE', 'false', 'False', 'FALSE'];
id_operators = ['and', 'xor', 'or'];
id_keywords = ['class', 'fun', 'return', 'next', 'break', 'unless', 'until', 'do', 'while', 'end', 'elsif', 'else', 'then', 'if', 'module'];
spe = ['$', '?'];
comment = ['#'];
delimiters = ['"', "'"];

all_digits = digits.concat(['A', 'a', 'B', 'c', 'D', 'd', 'E', 'e', 'F', 'f']);
all_separators = white.concat(ops).concat(separators).concat(comment);

// Constructor
function Lexer() {
    this.symbols = [];
}

// Main function. From a stream of characters produces a list of terminal symbols (tokens).
Lexer.prototype.tokenize = function(input) {
    this.symbols = [];
    var i = 0;
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
            this.symbols.push(new Symbol(SymbolType.Separator, input[i]));
            i += 1;
        } else if (comment.indexOf(input[i]) > -1) {
            while (i < input.length && input[i] != '\n' && input[i] != ';') {
                i += 1;
            }
        } else if (delimiters.indexOf(input[i]) > -1) {
            i = this.read_string(input, i);
        } else {
            alert("Char incorrect " + input[i] + " at " + i);
        }
    }
    //this.symbols.push(new Symbol(EOF, 'eof'));
    return this.symbols; // SymbolList(self.symbols)
}

// Read a number
Lexer.prototype.read_num = function(input, i) {
    var is_float = false;
    var num = input[i];
    i +=1;
    var mode = 'standard';
    while (i < input.length) {
        if (all_digits.indexOf(input[i]) > -1) {
            if (mode == 'binary' && ['0', '1'].indexOf(input[i]) == -1) {
                throw new Error("Incorrect Binary number '" + input[i] + "'");
            } else if (mode == 'standard' && digits.indexOf(input[i]) == -1) {
                throw new Error("Incorrect Decimal number '" + input[i] + "'");
            } else if (mode == 'octal' && (['8', '9'].indexOf(input[i]) > -1 || digits.indexOf(input[i]) == -1)) {
                throw new Error("Incorrect Octal number '" + input[i] + "'");
            }
            num += input[i];
            i +=1;
        } else if (input[i] == '.') {
            if (! is_float && i+1 < input.length && digits.indexOf(input[i+1]) > -1) {
                is_float = true;
                num += input[i];
                i += 1;
            } else if (! is_float && i+1 < input.length && input[i+1] == '.') {
                is_float = true;
                num += input[i];
                i += 1;
                break;
            } else if (! is_float && i+1 == input.length) {
                is_float = true;
                num += input[i];
                i += 1;
                break;
            } else {
                break;
            }
        } else if (alphas.indexOf(input[i]) > -1) {
            if (num.length == 1 && ['b', 'B'].indexOf(input[i]) > -1) {    
                mode = 'binary';
                num += input[i];
                i += 1;
            } else if (num.length == 1 && ['t', 'T'].indexOf(input[i]) > -1) {
                mode = 'octal';
                num += input[i];
                i += 1;
            } else if (num.length == 1 && ['x', 'X'].indexOf(input[i]) > -1) {
                mode = 'hexa';
                num += input[i];
                i += 1;
            } else {
                alert("Incorrect Id starting with numbers");
            }
        } else if (all_separators.indexOf(input[i]) > -1) {
            break;
        } else {
            console.log("problem at " + this.symbols.length);
            for (ii=0; ii < this.symbols.length; i++) {
                console.log(this.symbols[ii]);
            }
            throw new Error("Lexing number at character [" + input[i] + "]");
        }
    }
    if (! is_float) {
        this.symbols.push(new Symbol(SymbolType.Integer, num));
    } else {
        this.symbols.push(new Symbol(SymbolType.Float, num));
    }
    return i;
}

// Read an id
Lexer.prototype.read_id = function(input, i) {
    var id = input[i];
    i +=1;
    var cont = true;
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
        this.symbols.push(new Symbol(SymbolType.Boolean, id));
    } else if (id_operators.indexOf(id) > -1) {
        // operator boolean as function
        if (this.symbols.length > 1 && i > 0 && this.symbols[this.symbols.length-1].val == '.') {
            this.symbols.push(new Symbol(SymbolType.Id, id));
        } else {
            this.symbols.push(new Symbol(SymbolType.Operator, id));
        }
    } else if (id_keywords.indexOf(id) > -1) {
        // keyword as function
        if (this.symbols.length > 1 && i > 0 && this.symbols[this.symbols.length-1].val == '.') {
            this.symbols.push(new Symbol(SymbolType.Id, id));
        } else {
            this.symbols.push(new Symbol(SymbolType.Keyword, id));
        }
    } else {
        this.symbols.push(new Symbol(SymbolType.Id, id));
    }
    return i;
}

// Read an operator
Lexer.prototype.read_op = function(input, i) {
    var op = input[i];
    i +=1;
    while (op != '-' && i < input.length) {             // 2 +- 3 should not be seen as an "+-" operator but as "+" and "-" operators
        if (ops.indexOf(input[i]) > -1 && input[i] != '-') {
            op += input[i];
            i += 1;
        } else {
            break;
        }
    }
    if (operators.indexOf(op) == -1) {
        alert("Not known operator : " + op)
    }
    this.symbols.push(new Symbol(SymbolType.Operator, op))
    return i
}

// Read a string
Lexer.prototype.read_string = function(input, i) {
    var str = '';
    var begin_by = input[i];
    i += 1;
    while (i < input.length && input[i] != begin_by) {
        str += input[i];
        i += 1;
    }
    if (input[i] != begin_by) {
        alert("Unfinished string");
    } else {
        i += 1;
    }
    this.symbols.push(new Symbol(SymbolType.String, str));
    return i;
}

// Clear the symbol list
Lexer.prototype.clear = function() {
    this.symbols = [];
}

// Tests
Lexer.prototype.test = function(input, result) {
    this.clear();
    this.tokenize(input);
    var r = true;
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
        if (!r) {
            alert("ERROR : " + input);
        }
    }
    return r;
}

test_lexer = new Lexer();
test_lexer.test("4", [[4, SymbolType.Integer]]) ? console.log("=> 4 OK") : console.log("ERROR : 4");
test_lexer.test("4.0", [["4.0", SymbolType.Float]]) ? console.log("=> 4.0 OK") : console.log("ERROR : 4.0");
test_lexer.test("4.", [["4.", SymbolType.Float]]) ? console.log("=> 4. OK") : console.log("ERROR : 4.");
test_lexer.test("4..", [["4.", SymbolType.Float], [".", SymbolType.Operator]]) ? console.log("=> 4.. OK") : console.log("ERROR : 4..");
test_lexer.test("4..to_f", [["4.", SymbolType.Float], [".", SymbolType.Operator], ["to_f", SymbolType.Id]]) ? console.log("=> 4..to_f OK") : console.log("ERROR : 4..to_f");
test_lexer.test("4.to_f", [[4, SymbolType.Integer], [".", SymbolType.Operator], ["to_f", SymbolType.Id]]) ? console.log("=> 4.to_f OK") : console.log("ERROR : 4.to_f");
test_lexer.test("true", [[true, SymbolType.Boolean]]) ? console.log("=> true OK") : console.log("ERROR : true");
test_lexer.test("true or false", [[true, SymbolType.Boolean], ["or", SymbolType.Operator], [false, SymbolType.Boolean]]) ? console.log("=> true or false OK") : console.log("ERROR : true or false");

cmd = "2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3";
result = [[2, SymbolType.Integer], ["+", SymbolType.Operator], [3, SymbolType.Integer], ["-", SymbolType.Operator], [4, SymbolType.Integer], [".", SymbolType.Operator], ["to_f", SymbolType.Id], ["+", SymbolType.Operator], ["(", SymbolType.Separator], ["true", SymbolType.Boolean], [")", SymbolType.Separator], ["or", SymbolType.Operator], ["False", SymbolType.Boolean], ["xor", SymbolType.Operator], ["True", SymbolType.Boolean], ["**", SymbolType.Operator], [2.3, SymbolType.Float], ["+", SymbolType.Operator], ["0.3", SymbolType.Float], [".", SymbolType.Operator], ["to_i", SymbolType.Id], ["/", SymbolType.Operator], [0, SymbolType.Integer], [".", SymbolType.Operator], ["to_f", SymbolType.Id], ["/", SymbolType.Operator], ["0.", SymbolType.Float], [".", SymbolType.Operator], ["to_f", SymbolType.Id], ["+", SymbolType.Operator], ["-", SymbolType.Operator], [3, SymbolType.Integer]];
test_lexer.test(cmd, result) ? console.log("=> 2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3 OK") : console.log("ERROR : 2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3");

test_lexer.test("'abc'", [["abc", SymbolType.String]]) ? console.log("=> 'abc' OK") : console.log("ERROR : 'abc'");
test_lexer.test('"abc"', [["abc", SymbolType.String]]) ? console.log('=> "abc" OK') : console.log('ERROR : "abc"');
test_lexer.test("if", [["if", SymbolType.Keyword]]) ? console.log('=> if OK') : console.log('ERROR : if');

//-----------------------------------------------------------------------
// Syntaxic analysis (Expression)
//-----------------------------------------------------------------------

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
        if (symb.terminal() && (symb.kind == SymbolType.Operator || symb.kind == SymbolType.Separator)) {
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

// From a token list make a tree!
Parser.prototype.parse_expression = function(symbols) {
    this.prepare(symbols);
    while (symbols.length > 1) {    
        var target = this.first_op(symbols);
        if (DEBUG) {
            console.log('>>> target=' + target + ' symb=' + symbols[target]);
        }
        if (!symbols[target].terminal()) {
            if (symbols[target].val == 'call(') {
                var id = symbols[target-1];
                if (id.terminal() && id.kind == SymbolType.Id) {
                    var n = new Symbol(SymbolType.Structure, 'unprefixed_call', id, symbols[target]); // kind val left right
                    symbols.splice(target, 1);
                    symbols[target-1] = n;
                } else {
                    alert("Call not understood");
                }
            } else {
                alert("Error on target node");
            }
        } else if (symbols[target].terminal()) {
            if (symbols[target].val == 'unary-') {
                var n = new Symbol(SymbolType.Operator, 'unary-', null, symbols[target+1]); // kind val left right
                symbols.splice(target+1, 1);
                symbols[target] = n;
            } else if (symbols[target].val == 'expr(') {
                var fin = this.fetch_closing('(', symbols, target);
                var sub = symbols.slice(target+1, fin);
                this.make_tree(sub);
                var jj = fin;
                while (jj > target) {
                    this.symbols.splice(jj, 1);
                    jj -= 1;
                }
                symbols[target] = sub[0];
            } else if (symbols[target].val == 'call(') {
                var fin = this.fetch_closing('(', symbols, target);
                var sub = symbols.slice(target+1, fin);
                this.make_tree(sub);
                jj = fin;
                while (jj > target) {
                    this.symbols.splice(jj, 1);
                    jj -= 1;
                }
                symbols[target] = new Symbol(SymbolType.Structure, 'call(', null, sub[0]); // kind val left right
            } else if (symbols[target].val == ',') {
                var n = new Symbol(SymbolType.Structure, 'suite', symbols[target-1], symbols[target+1]); // kind val left right
                symbols.splice(target+1, 1);
                symbols.splice(target, 1);
                symbols[target-1] = n;
            } else if (target > 0) {
                if (symbols[target].val != '.' || (symbols[target].val == '.' && this.not_exist_or_dif(symbols, target+2, False, "call"))) {
                    var n = new Symbol(symbols[target].val, symbols[target].kind, symbols[target-1], symbols[target+1]); // kind val left right
                    symbols.splice(target+1, 1);
                    symbols.splice(target, 1);
                    symbols[target-1] = n;
                } else {
                    alert("WTF?");
                }
                //} else { No converted Python
                //    alert("AAAAAAAAAAAAAAAAA");
                //    // nx -> fun, call (avec par)
                //    nx = symbols[target+2]
                //    nx.left = symbols[target+1]
                //    // n -> id, nx
                //    n = Symbol(left=symbols[target-1], right=nx, val="prefixed_call", kind=Structure)
                //    del symbols[target+2]
                //    del symbols[target+1]
                //    del symbols[target]
                //    symbols[target-1] = n
                //}
            } else if (target == -1 && symbols.length > 0) {
                var n = symbols[0];
            } else {
                alert("YOUPI!");
            }
        } else {
            alert("Expression not understood : " + symbols[target]);
        }
        if (DEBUG) {
            for(ii = 0; ii < symbols.length; ii++) {
                console.log('' + ii + '. ' + symbols[ii]);
                ii +=1 ;
            }
            console.log("length=" + symbols.length);
        }
    }
    this.tree = symbols[0];
}

//-----------------------------------------------------------------------------
// Syntaxic analysis (Instruction)
//-----------------------------------------------------------------------------

Parser.prototype.parse = function(symbols) {
    this.parse_expression(symbols);
    return this.tree;
}

//-----------------------------------------------------------------------------
// Interpreter
//-----------------------------------------------------------------------------

var TypeSystem = {
    Object : 'Object',
    String : 'String',
    Float : 'Float',
    Integer : 'Integer',
}

function Value(value, kind) {
    this.value = value;
    this.kind = kind;
}

Value.prototype.toString = function() {
    return '' + this.value + " : " + this.kind;
}

Value.prototype.equal = function(v) {
    return (v.value === this.value && v.kind === this.kind);
}

function Interpreter() {
}

Interpreter.prototype.exec_node = function(symbol, scope) {
    if (typeof symbol == "undefined") { 
        return null; //alert("undefined !") 
    }
    if (symbol.terminal()) {
        return this.exec_terminal(symbol, scope);
    } else {
        console.log(typeof symbol);
        console.log(symbol);
        alert("Node not known");
    }
}

Interpreter.prototype.exec_terminal = function(symbol, scope) {
    if (symbol.kind == SymbolType.Integer) {
        if (symbol.val.length > 1 && (symbol.val[1] == 'x' || symbol.val[1] == 'X')) {
            return new Value(parseInt(symbol.val), TypeSystem.Integer);
        } else if (symbol.val.length > 1 && (symbol.val[1] == 'b' || symbol.val[1] == 'B')) {
            return new Value(parseInt(symbol.val.slice(2, symbol.val.length), 2), TypeSystem.Integer);
        } else if (symbol.val.length > 1 && (symbol.val[1] == 't' || symbol.val[1] == 'T')) {
            return new Value(parseInt("0" + symbol.val.slice(2, symbol.val.length), 8), TypeSystem.Integer);
        } else {
            return new Value(parseInt(symbol.val), TypeSystem.Integer);
        }
    } else if (symbol.kind == SymbolType.Float) {
        return new Value(parseFloat(symbol.val), TypeSystem.Float);
    } else if (symbol.kind == SymbolType.Id) {
        if (!scope.hasOwnProperty(symbol.val)) {
            alert('unreferenced variable ' + symbol.val);
        } else {
            return scope[symbol.val]
        }
    } else if (symbol.kind == SymbolType.String) {
        return new Value(symbol.val, TypeSystem.String);
    } else if (symbol.kind == SymbolType.Boolean) {
        if (symbol.val == 'true' || symbol.val == 'True' || symbol.val == 'TRUE') {
            return new Value(true, TypeSystem.Boolean);
        } else {
            return new Value(false, TypeSystem.Boolean);
        }
    }
    // CASE OF ERRORS
    else if (symbol.kind == SymbolType.Operator) {
        alert("Operators need one or more operands");
    } else if (symbol.kind == Separator) {
        alert("Separators alone are meaningless");
    } else {
        alert("TokenType not understood : " + symbol);
    }
}

Interpreter.prototype.do_string = function(cmd, scope) {
    l = new Lexer();
    p = new Parser();
    tokens = l.tokenize(cmd);
    tree   = p.parse(tokens);
    result = this.exec_node(tree);
    return result;
}

Interpreter.prototype.test = function(cmd, scope, waiting_for) {
    l = new Lexer();
    p = new Parser();
    tokens = l.tokenize(cmd);
    tree   = p.parse(tokens);
    result = this.exec_node(tree);
    if (!result.equal(waiting_for)) {
        console.warn("ERROR : waiting for " + waiting_for + " and the result was " + result);
        console.warn("Parsed tokens :");
        for (i=0; i < tokens.length; i++) {
            console.warn(tokens[i]);
        }
        console.warn("Head of the tree :");
        console.warn("    " + tree);
    } else {
        console.log("OK : " + cmd + " => " + result);
    }
    return result;
}


root_scope = {
    'Pi' : Value(Math.PI, TypeSystem.Float),
    'PI' : Value(Math.PI, TypeSystem.Float),
    '_'  : Value(null, TypeSystem.Object),
}

// Tests

console.log("----------------------------------------------------------------");
console.log("Interpreter");
console.log("----------------------------------------------------------------");

r = test_lexer.tokenize("2+3");
 
test_parser = new Parser();
console.log(test_parser.first_op(r));
test_parser.parse_expression(r);
console.log(test_parser.tree);

test_interpreter = new Interpreter();

test_interpreter.test("2", root_scope, new Value(2, TypeSystem.Integer));
test_interpreter.test("0b10", root_scope, new Value(2, TypeSystem.Integer));
test_interpreter.test("0xA", root_scope, new Value(10, TypeSystem.Integer));
test_interpreter.test("0t10", root_scope, new Value(8, TypeSystem.Integer));
