//
// Lexer         string  -> [tokens]
// Parser       [tokens] -> abstract syntax tree (AST)
// Interpreter    AST    -> result
//

DEBUG = false;

//-----------------------------------------------------------------------------
// Base
//-----------------------------------------------------------------------------

var SymbolType = {
    Integer : 'Integer Symbol',
    Float : 'Float Symbol',
    Id : 'Id Symbol',
    Operator : 'Operator Symbol',
    Separator : 'Separator Symbol',
    Keyword : 'Keyword Symbol',
    Boolean : 'Boolean Symbol',
    String : 'String Symbol',
    //Discard : 'Discard',
    //Error : 'Error',
};

function Symbol(type, value, line) {
    this.type = type;
    this.value = value;
    this.line = line;
}

Symbol.prototype.terminal = function() {
    return true;
}

Symbol.prototype.getValue = function() {
    return this.value;
}

Symbol.prototype.setValue = function(v) {
    this.value = v;
}

Symbol.prototype.getType = function() {
    return this.type;
}

Symbol.prototype.getLine = function() {
    return this.line;
}

Symbol.prototype.getLength = function() {
    return 1;
}

Symbol.prototype.toString = function() {
    return this.getValue() + " : " + this.type; // + " @" + this.line;
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

// highlighting differences between :
//     - (unary) et - (binary)
//     () (call) et () (expr)
Lexer.prototype.prepare = function() {
    var i = 0;
    while (i < this.symbols.length) {
        symb = this.symbols[i];
        if (symb.terminal()) {
            if (symb.getValue() == '-' && (i == 0 || this.symbols[i-1].getType() == SymbolType.Operator)) {
                symb.setValue('unary-');
            }
            // () -> x
            if (symb.getValue() == '(' && i < this.symbols.length-1 && this.symbols[i+1].getValue() == ')') {
                this.symbols.splice(i+1 , 1);
                this.symbols.splice(i, 1);
                i-=1;
            }
            //
            if (symb.getValue() == '(' && i > 0 && this.symbols[i-1].getType() != SymbolType.Operator) {
                symb.setValue('call(');
            } else if (symb.getValue() == '(') {
                symb.setValue('expr(');
            }
        i+=1;
        }
    }
}

// Main function. From a stream of characters produces a list of terminal symbols (tokens).
Lexer.prototype.tokenize = function(input) {
    this.symbols = [];
    var i = 0;
    var nb_line = 1;
    while (i < input.length) {
        if (digits.indexOf(input[i]) > -1) { 
            i = this.read_num(input, i, nb_line); 
        } else if (alphas.indexOf(input[i]) > -1) { 
            i = this.read_id(input, i, nb_line); 
        } else if (ops.indexOf(input[i]) > -1) { 
            i = this.read_op(input, i, nb_line); 
        } else if (white.indexOf(input[i]) > -1) { 
            if (input[i] == "\n") { nb_line += 1; }
            i += 1; 
        } else if (separators.indexOf(input[i]) > -1) {
            this.symbols.push(new Symbol(SymbolType.Separator, input[i], nb_line));
            i += 1;
        } else if (comment.indexOf(input[i]) > -1) {
            while (i < input.length && input[i] != '\n' && input[i] != ';') {
                i += 1;
            }
        } else if (delimiters.indexOf(input[i]) > -1) {
            i = this.read_string(input, i, nb_line);
        } else {
            throw new Error("Char incorrect " + input[i] + " at " + i);
        }
    }
    this.prepare();
    return this.symbols;
}

// Read a number
Lexer.prototype.read_num = function(input, i, nb_line) {
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
                throw new Error("Incorrect Id starting with numbers");
            }
        } else if (all_separators.indexOf(input[i]) > -1) {
            break;
        } else {
            console.log("problem at " + this.symbols.length);
            for (var ii=0; ii < this.symbols.length; i++) {
                console.log(this.symbols[ii]);
            }
            throw new Error("Lexing number at character [" + input[i] + "]");
        }
    }
    if (! is_float) {
        this.symbols.push(new Symbol(SymbolType.Integer, num, nb_line));
    } else {
        this.symbols.push(new Symbol(SymbolType.Float, num, nb_line));
    }
    return i;
}

// Read an id
Lexer.prototype.read_id = function(input, i, nb_line) {
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
        this.symbols.push(new Symbol(SymbolType.Boolean, id, nb_line));
    } else if (id_operators.indexOf(id) > -1) {
        // operator boolean as function
        if (this.symbols.length > 1 && i > 0 && this.symbols[this.symbols.length-1].getValue() == '.') {
            this.symbols.push(new Symbol(SymbolType.Id, id, nb_line));
        } else {
            this.symbols.push(new Symbol(SymbolType.Operator, id, nb_line));
        }
    } else if (id_keywords.indexOf(id) > -1) {
        // keyword as function
        if (this.symbols.length > 1 && i > 0 && this.symbols[this.symbols.length-1].getValue() == '.') {
            this.symbols.push(new Symbol(SymbolType.Id, id, nb_line));
        } else {
            this.symbols.push(new Symbol(SymbolType.Keyword, id, nb_line));
        }
    } else {
        this.symbols.push(new Symbol(SymbolType.Id, id, nb_line));
    }
    return i;
}

// Read an operator
Lexer.prototype.read_op = function(input, i, nb_line) {
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
        throw new Error("Not known operator : " + op)
    }
    this.symbols.push(new Symbol(SymbolType.Operator, op, nb_line))
    return i
}

// Read a string
Lexer.prototype.read_string = function(input, i, nb_line) {
    var str = '';
    var begin_by = input[i];
    i += 1;
    while (i < input.length && input[i] != begin_by) {
        str += input[i];
        i += 1;
    }
    if (input[i] != begin_by) {
        throw new Error("Unfinished string");
    } else {
        i += 1;
    }
    this.symbols.push(new Symbol(SymbolType.String, str, nb_line));
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
    var error_at;
    if (this.symbols.length != result.length) {
        console.log("length!");
        r = false;
    } else {
        for (var i = 0; i < result.length; i++) {
            //console.log(this.symbols[i].getValue());
            //console.log(result[i][0].toString());
            if (this.symbols[i].getValue() != result[i][0].toString() || this.symbols[i].getType() != result[i][1]) {
                r = false;
                error_at = i;
                break;
            }
        }
    }
    if (DEBUG) {
        for (var i = 0; i < this.symbols.length; i += 1) {
            console.log("" + i + ". " + this.symbols[i]);
        }
        if (!r) {
            throw new Error("ERROR mismatch : " + this.symbols[error_at] + " for result : " + result[error_at]);
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
result = [[2, SymbolType.Integer], ["+", SymbolType.Operator], [3, SymbolType.Integer], ["-", SymbolType.Operator], [4, SymbolType.Integer], [".", SymbolType.Operator], ["to_f", SymbolType.Id], ["+", SymbolType.Operator], ["expr(", SymbolType.Separator], ["true", SymbolType.Boolean], [")", SymbolType.Separator], ["or", SymbolType.Operator], ["False", SymbolType.Boolean], ["xor", SymbolType.Operator], ["True", SymbolType.Boolean], ["**", SymbolType.Operator], [2.3, SymbolType.Float], ["+", SymbolType.Operator], ["0.3", SymbolType.Float], [".", SymbolType.Operator], ["to_i", SymbolType.Id], ["/", SymbolType.Operator], [0, SymbolType.Integer], [".", SymbolType.Operator], ["to_f", SymbolType.Id], ["/", SymbolType.Operator], ["0.", SymbolType.Float], [".", SymbolType.Operator], ["to_f", SymbolType.Id], ["+", SymbolType.Operator], ["unary-", SymbolType.Operator], [3, SymbolType.Integer]];
test_lexer.test(cmd, result) ? console.log("=> 2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3 OK") : console.log("ERROR : 2 + 3 - 4.to_f + (true) or False xor True ** 2.3 + 0.3.to_i / 0.to_f / 0..to_f +- 3");

test_lexer.test("'abc'", [["abc", SymbolType.String]]) ? console.log("=> 'abc' OK") : console.log("ERROR : 'abc'");
test_lexer.test('"abc"', [["abc", SymbolType.String]]) ? console.log('=> "abc" OK') : console.log('ERROR : "abc"');
test_lexer.test("if", [["if", SymbolType.Keyword]]) ? console.log('=> if OK') : console.log('ERROR : if');

//-----------------------------------------------------------------------
// Syntaxic analysis (Expression)
//-----------------------------------------------------------------------

var NodeType = {
    Terminal    : 'Terminal Node',
    BinaryOp    : 'Binary Operator Node',
    UnaryOp     : 'Unary Operator Node',
    FunctionCall: 'Function Call Node',
    Structure   : 'Structure Node',
    ParamList   : 'Parameter List',
    Affectation : 'Affectation',
};

function Node(type, elem1, elem2, elem3, elem4) {
    this.type = type;
    this.suite = [];
    if (typeof elem1 !== 'undefined') { this.suite.push(elem1); }
    if (typeof elem2 !== 'undefined') { this.suite.push(elem2); }
    if (typeof elem3 !== 'undefined') { this.suite.push(elem3); }
}

Node.prototype.terminal = function() {
    return (this.suite.length == 1);
}

Node.prototype.getValue = function() {
    if (this.terminal()) {
        return this.suite[0].getValue();
    } else {
        return null;
    }
}

Node.prototype.getType = function() {
    return this.type;
}

Node.prototype.getLength = function() {
    return this.suite.length;
}

Node.prototype.toString = function() {
    return this.type;
}

function Parser() {
    this.tree = null;
}

// Fetch the operator with the highest priority to execute
Parser.prototype.first_op = function(symbols) {
    var i = 0;
    var best = -1;
    var best_prio = -1;
    var prio = { ')' : 0, ',' : 1, 'and' : 5, 'or' : 5, 'xor' : 5, 
             '>' : 8, '<' : 8, '>=' : 8, '<=' : 8, '==' : 8, '!=' : 8, '<=>' : 8, 
             '<<': 9, '>>' : 9, '+' : 10, '-' : 10, 
             '*' : 20, '/' : 20, '//' : 20, '**' : 30, '%' : 30, '.' : 40, // 'call' : 35,  ???
             'unary-' : 50, 'call(' : 51, 'expr(' : 60 };
    var lvl = 1;
    while (i < symbols.length) {
        symb = symbols[i];
        if (symb.terminal() && (symb.getType() == SymbolType.Operator || symb.getType() == SymbolType.Separator)) {
            if (best == -1) {
                best = i
                best_prio = prio[symb.getValue()]*lvl
            } else {
                if (prio[symb.getValue()]*lvl > best_prio) {
                    best = i
                    best_prio = prio[symb.getValue()]*lvl
                }
            }
            // () for others
            if (symb.getValue() == 'call(' || symb.getValue() == 'expr(') {
                lvl*=10
            } else if (symb.getValue() == ')') {
                lvl/=10
            }
        } else if (symb.getValue() == 'call(') { // not terminal
            if (prio[symb.getValue()]*lvl > best_prio) {
                best = i
                best_prio = prio[symb.getValue()]*lvl
            } else {
                throw new Error("Incorrect expression call");
            }
        }
        i +=1;
    }
    if (best == -1) { // Hack for global
        if (symbols.length == 2 && symbols[0].getType() == SymbolType.Id && symbols[1].getType() == NodeType.ParamList) {
                best = 1;
        } else {
            throw new Error("Incorrect expression");
        }
    }
    return best;
}

Parser.prototype.fetch_closing = function(sep, symbols, i) {
    var lvl = 0;
    var pos = 0;
    var pos = i;
    while (pos < symbols.length) {
        symb = symbols[pos];
        if (sep == '(' && (symb.getValue() == 'call(' || symb.getValue() == 'expr(')) {
            lvl += 1;
        } else if (sep == '(' && symb.getValue() == ')') {
            lvl -= 1;
        }
        if (lvl == 0) {
            break;
        }
        pos += 1;
    }
    if (lvl != 0) {
        throw new Error("Incorrect expression ()");
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
    if (symbols[index].getValue() != value) {
        return true;
    }
    return false;
}

// From a token list make a tree!
Parser.prototype.parse_expression = function(symbols) {
    //this.prepare(symbols);
    while (symbols.length > 1) {    
        var target = this.first_op(symbols);
        if (DEBUG) {
            console.log('>>> target=' + target + ' symb=' + symbols[target]);
        }
        if (symbols[target].getType() == NodeType.ParamList) { // !symbols[target].terminal()) {
            var n = new Node(NodeType.FunctionCall, null, symbols[target-1], symbols[target]); // caller fun params
            symbols.splice(target, 1);
            symbols[target-1] = n;
        } else if (symbols[target].terminal()) {
            if (symbols[target].getValue() == 'unary-') {
                var n = new Node(NodeType.UnaryOp, symbols[target], symbols[target+1]);
                symbols.splice(target+1, 1);
                symbols[target] = n;
            } else if (symbols[target].getValue() == 'expr(') {
                var fin = this.fetch_closing('(', symbols, target);
                var sub = symbols.slice(target+1, fin);
                this.parse_expression(sub);
                var jj = fin;
                while (jj > target) {
                    symbols.splice(jj, 1);
                    jj -= 1;
                }
                symbols[target] = sub[0];
            } else if (symbols[target].getValue() == 'call(') {
                var fin = this.fetch_closing('(', symbols, target);
                var sub = symbols.slice(target+1, fin);
                this.parse_expression(sub);
                jj = fin;
                while (jj > target) {
                    symbols.splice(jj, 1);
                    jj -= 1;
                }
                symbols[target] = new Node(NodeType.ParamList, sub[0]);
            } else if (symbols[target].getValue() == ',') {
                var n = new Node(NodeType.ParamList, symbols[target-1], symbols[target+1]);
                symbols.splice(target+1, 1);
                symbols.splice(target, 1);
                symbols[target-1] = n;
            } else if (target > 0) {
                if (symbols[target].getValue() == '.' && !(typeof symbols[target+1] == "undefined") && symbols[target+1].getType() == SymbolType.Id && !(typeof symbols[target+2] == "undefined") && symbols[target+2].getType() == NodeType.ParamList) { // Ternary .
                    var n = new Node(NodeType.FunctionCall, symbols[target-1], symbols[target+1], symbols[target+2]); // caller fun params
                    symbols.splice(target+2, 1);
                } else {
                    var n = new Node(NodeType.BinaryOp, symbols[target], symbols[target-1], symbols[target+1]); // bin op1 op2
                }
                symbols.splice(target+1, 1);
                symbols.splice(target, 1);
                symbols[target-1] = n;
            } else if (target == -1 && symbols.length > 0) {
                var n = symbols[0];
            } else {
                throw new Error("YOUPI!");
            }
        } else {
            throw new Error("Expression not understood : " + symbols[target]);
        }
        if (DEBUG) {
            for(var ii = 0; ii < symbols.length; ii++) {
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

/*


def make_typed_aff(symbols):
    sub = symbols.core[4:]
    make_tree(sub)
    nx = sub[0]
    nid = Symbol(left=symbols(0), right=symbols(2), val='typed_id', kind=Structure)
    n = Symbol(left=nid, right=nx, val='typed_aff', kind=Structure)
    symbols.clear()
    symbols.add(n)

class Parser:
    """From a list of symbol make an abstract syntax tree"""
    
    def __init__(self):
        pass
    
    def fetch_end(self, symbols, start):
        parcours = start+1
        level = 1
        while parcours < len(symbols):
            #print symbols[parcours].val, level
            if symbols[parcours].val == 'if': level += 1
            elif symbols[parcours].val == 'end': level -= 1
            if level == 0:
                return parcours
            parcours += 1
        return -1
    
    def fetch_x(self, symbols, start, symb):
        parcours = start+1
        while parcours < len(symbols):
            if symbols[parcours].val == symb: return parcours
            parcours += 1
        return -1
    
    def parse(self, symbols):
        #print symbols[0].val
        if symbols.include(';'):
            #print 'parse -> ; detected'
            two_part = symbols.split(';')
            self.parse(SymbolList(two_part[0]))
            self.parse(SymbolList(two_part[1]))
            n = Symbol(val='suite', kind=Structure, left=two_part[0][0], right=two_part[1][0])
            symbols.clear()
            symbols.add(n)
        elif symbols[0].val == 'if':
            #print 'parse -> if detected'
            to = self.fetch_end(symbols, 0)
            if to == -1: raise Exception("Unclosed if")
            elif to == 1: raise Exception("If without condition and body!")
            else:
                then = self.fetch_x(symbols, 0, 'then')
                if then == -1: raise Exception("No then!")
                elif then == 1: raise Exception("No condition!")
                else:
                    condition = SymbolList(symbols[1:then])
                    self.parse(condition)
                    action_else = [None]
                    if to == then + 1: action = [None]
                    else:
                        s_else = self.fetch_x(symbols, 0, 'else')
                        if s_else == -1:
                            action = SymbolList(symbols[then+1:to])
                            self.parse(action)
                        else:
                            action = SymbolList(symbols[then+1:s_else])
                            self.parse(action)
                            action_else = SymbolList(symbols[s_else+1:to])
                            self.parse(action_else)
                    n = Symbol(val='if', kind=Structure, left=condition[0], right=action[0])
                    n.right_else = action_else[0]
                    symbols.clear()
                    symbols.add(n)
        elif not not_exist_or_dif(symbols, 1, True, ':'):
            #print 'parse -> : detected'
            if len(symbols) > 4:
                make_typed_aff(symbols)
            else:
                raise Exception("Incorrect typed declaration")
        else:
            #print 'parse -> standard'
            make_tree(symbols)
*/

Parser.prototype.parse_affectation = function(symbols) {
    var id = symbols.shift();   // id
    symbols.shift();            // =
    this.parse_expression(symbols);
    var n = new Node(NodeType.Affectation, id, this.tree);
    this.tree = n;
}

Parser.prototype.parse = function(symbols) {
    if (!this.not_exist_or_dif(symbols, 1, true, '=')) {
        if (symbols.length > 2) {
            this.parse_affectation(symbols);
        } else {
            throw new Error("Incorrect typed declaration");
        }
    } else {
        this.parse_expression(symbols);
    }
    return this.tree;
}

//-----------------------------------------------------------------------------
// Interpreter
//-----------------------------------------------------------------------------

var ValueType = {
    Object : 'Object',
    String : 'String',
    Float : 'Float',
    Integer : 'Integer',
    Boolean : 'Boolean',
}

function Value(value, type) {
    this.value = value;
    this.type = type;
}

Value.prototype.getValue = function() {
    return this.value;
}

Value.prototype.getType = function() {
    return this.type;
}

Value.prototype.toString = function() {
    if (this.getValue() == null) {
        return 'ValueStr(nihil : ' + this.getType() + ')';
    } else {
        return 'ValueStr(' + this.getValue() + " : " + this.getType() + ')';
    }
}

Value.prototype.toStringValue = function() {
    if (this.getValue() == null) {
        return 'nihil';
    } else {
        return '' + this.getValue();
    }
}

Value.prototype.toStringTypedValue = function() {
    if (this.getValue() == null) {
        return 'nihil : ' + this.getType();
    } else {
        return '' + this.getValue() + " : " + this.getType();
    }
}

Value.prototype.equal = function(v) {
    return (v.getValue() === this.getValue() && v.getType() === this.getType());
}

function Interpreter() {
}

Interpreter.prototype.exec_node = function(node, scope) {
    if (node instanceof Symbol) {
        return this.exec_terminal(node, scope);
    } else if (node instanceof Node) {
        return this.exec_non_terminal(node, scope);
    } else {
        console.log(typeof node);
        console.log(node);
        throw new Error("Node not known");
    }
}

//- Lib

Interpreter.prototype.dispatch = function(target, name, args, scope) {
    if (!(target instanceof Value)) {
        if (target == null) { // Global
            if (Baselib["Base"].hasOwnProperty(name)) {
                return Baselib["Base"][name](target, args, scope);
            } else {
                throw new Error("Dispatch : Global function " + name + " not known.");
            }
        } else {
            throw new Error("Dispatch : Not a value");
        }
    }
    if (Baselib.hasOwnProperty(target.getType())) {
        if (Baselib[target.getType()].hasOwnProperty(name)) {
            return Baselib[target.getType()][name](target, args, scope);
        } else {
            throw new Error("Dispatch : Function " + name + " not known for " + target.getType());
        }
    } else {
        throw new Error("Dispatch : Type not known " + target.getType());
    }
}

// NOT CONVERTED YET
/*
Interpreter.prototype.instance_function = function(target, name, args, scope) {
    if target.__class__ in [int, float, str, bool]:
        pass
    elif target.terminal() and target.getType() in [Integer, Float, String, Boolean]:
        target = exec_node(target)
    elif target.terminal() and target.getType() == Id:
        target = scope[target.getValue()]
    else:
        raise Exception("Bad target for instance function call: %s" % (target,))
    
    if name.terminal() and name.getType() == Id:
        name = name.val
    else:
        raise Exception("Bad name for instance function call: %s" % (name,))
    
    if args is None:
        par = []
    elif args.right.__class__ in [int, float, str, bool]:
        par = [args.right]
    elif args.right.terminal():
        par = [exec_node(args.right, scope)]
    elif args.right.getValue() == 'suite':
        a = args.right
        par = []
        while not a.terminal():
            par.append(exec_node(a.right))
            a = a.left
        par.append(exec_node(a))
    else:
        raise Exception("Bad par for instance function call: %s" % (args.right,))
    r = bb.send(target, name, par, scope)
    return r
}
*/

/*
// NOT DEBUGGED YET
Interpreter.prototype.concordance = function(typ, val) {
    if (typ == 'int') {
        if (!isinstance(val, int)) {
            throw new Error("Reference of type " + typ + " cannot reference value of type " + val.__class__);
        }
    } else if (typ == 'bool') {
        if (!isinstance(val, bool)) {
            throw new Error("Reference of type " + typ + " cannot reference value of type " + val.__class__);
        }
    } else if (typ == 'float') {
        if (!isinstance(val, float)) {
            throw new Error("Reference of type " + typ + " cannot reference value of type " + val.__class__);
        }
    } else {
        throw new Error("Type unknown : " + typ);
    }
    return true;
}
*/

var op_to_fun = {
    "+" : "add",
    "-" : "sub",
    "*" : "mul",
    "/" : "div",
    "//": "intdiv",
    "**": "pow",
    "%" : "mod",
    ">" : "gt",
    "<" : "lt",
    ">=": "ge",
    "<=": "le",
    "==": "equal",
    "!=": "diff",
    "<<": "lshift",
    ">>": "rshift",
    "and": "and",
    "or" : "or",
    "xor": "xor",
    "<=>": "cmp",
};

// SUBSET
Interpreter.prototype.exec_non_terminal = function(node, scope) {
    if (node.type == NodeType.UnaryOp) {
        var op     = node.suite[0].getValue();
        var caller = this.exec_node(node.suite[1], scope);
        
        if (op == 'unary-') {
            return this.dispatch(caller, "inv", [], scope);
        } else {
            throw new Error("Unary operator not known : " + op);
        }
    } else if (node.type == NodeType.BinaryOp) {
        var op = node.suite[0].getValue();
        
        if (op in op_to_fun) {
            var caller = this.exec_node(node.suite[1], scope);
            var param  = this.exec_node(node.suite[2], scope);
            return this.dispatch(caller, op_to_fun[op], [param], scope);
        } else if (op == '.') {
            var caller = this.exec_node(node.suite[1], scope);
            if (node.suite[2].getType() == SymbolType.Id) {         // 2.abs => . 2 abs
                return this.dispatch(caller, node.suite[2].getValue(), [], scope);
            } else {
                throw new Error("Unknown field"); // Thériquement impossible
            }
        } else {
            throw new Error("Binary operator not known : " + op);
        }
    } else if (node.getType() == NodeType.FunctionCall) {
        var caller;
        if (node.suite[0] != null) { // Method
            caller = this.exec_node(node.suite[0], scope);
        } else { // Global
            caller = null;
        }
        var nom_fonction = node.suite[1].getValue();
        var parametres = node.suite[2];
        var le_parametre = this.exec_terminal(parametres.suite[0], scope);
        return this.dispatch(caller, nom_fonction, [le_parametre], scope);
    } else if (node.getType() == NodeType.Affectation) {
        var id = node.suite[0].getValue();
        var value = this.exec_node(node.suite[1], scope);
        marshallIdValue(id, value);
        return new Value(null, ValueType.Object);
    } else if (node.getType() == NodeType.Structure) {
        throw new Error("Structure not yet handled");
    } else {
        throw new Error("Node type not understood : val=" + symbol.getValue() + " left=" + symbol.left + " right=" + symbol.right);
    }
}

function marshallIdValue(name,value) {
    localStorage.setItem(name, value.getType()+"#"+value.getValue());
}

function unmarshallIdValue(name) {
    var n = localStorage.getItem(name);
    if (typeof n != "undefined" && n != null) {
        var tab = n.split("#");
        if (tab[0] === ValueType.Integer) {
            return new Value(parseInt(tab[1]), tab[0]);
        } else if (tab[0] === ValueType.Boolean) {
            if (tab[1] === "true") {
                return new Value(true, tab[0]);
            } else {
                return new Value(false, tab[0]);
            }
        } else {
            throw new Error("How to unmarshall this ? " + tab[0]);
        }
    } else {
        return null;
    }
}

// NOT DEBUGGED YET
/*
    
add sub mul div mod intdiv pow 
return instance_function(exec_node(symbol.left, scope), new Symbol(Id, 'add'), new Symbol(SymbolType.Structure, 'call(', right=exec_node(symbol.right)), scope);
return instance_function(exec_node(symbol.right, scope), new Symbol(Id, 'inv'), null, scope); -unary

        } else if (symbol.getValue() in ['and', 'or', 'xor']) {
            return instance_function(exec_node(symbol.left, scope), new Symbol(Id, symbol.getValue()), new Symbol(SymbolType.Structure, 'call(', right=exec_node(symbol.right)), scope);
        } else if (symbol.getValue() == '.') {
            if symbol.right.getValue() != 'call_with_args') {
                target = exec_node(symbol.left, scope);
                return instance_function(target, symbol.right, None, scope);
            } else if (symbol.right.getValue() == 'call_with_args') {
                call = symbol.right;
                return instance_function(symbol.left, call.left, call.right, scope);
            } else {
                throw new Error("What to do with this symbol ? : " + symbol.right.getValue());
            }
        } else if (symbol.getValue() == '<=>') {
            return instance_function(exec_node(symbol.left, scope), Symbol(Id, 'cmp'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope);
        } else if (symbol.getValue() in ['>', '<', '>=', '<=', '==', '!=']) {
            r = instance_function(exec_node(symbol.left, scope), Symbol(Id, 'cmp'), Symbol(Structure, 'call(', right=exec_node(symbol.right)), scope);

    } else if (symbol.getType() == SymbolType.Structure) {
        if (symbol.getValue() == 'call_with_args') {
            return global_function(symbol.left, symbol.right, scope);
        //} else if (symbol.getValue() == 'prefixed_call':
        //    return instance_function(symbol.left, symbol.right, scope)
        } else if (symbol.getValue() == 'aff') {
            // const
            if (symbol.left.getValue() in scope && symbol.left.getValue()[0].isupper()) {
                throw new Error("Constant reference can't be changed");
            }
            value = exec_node(symbol.right, scope);
            if (symbol.left.getValue()[-1] == '?' && not isinstance(value, bool)) {
                throw new Error("?-ending id must reference boolean value");
            }
            // typ
            id = symbol.left.val;
            if (id in scope && scope[id][1] is not None) {
                concordance(scope[id][1], value);
            }
            // aff
            scope[id] = (value, None);
            return scope[id][0];
        } else if (symbol.getValue() == 'typed_aff') {
            id = symbol.left.left.val;
            typ= symbol.left.right.val;
            val= exec_node(symbol.right, scope);
            // print id
            // print typ
            // print val
            // on essaye de typer quelque chose de deja declare
            if (id in scope) {
                throw new Error("Cannot type reference already declared: %s" % (id,));
            }
            concordance(typ, val);
            scope[id] = (val, typ);
            return scope[id][0];
        } else if (symbol.getValue() == 'suite') {
            exec_node(symbol.left, scope);
            return exec_node(symbol.right, scope);
        } else if (symbol.getValue() == 'if') {
            condition = exec_node(symbol.left);
            action = None;
            if (condition && symbol.right is not None) {
                action = exec_node(symbol.right);
                return action;
            if (not condition && symbol.right_else is not None) {
                action = exec_node(symbol.right_else);
                return action;
            return None;
        } else {
            throw new Error("Invisible Node type not understood");
        }
}
*/
        
Interpreter.prototype.exec_terminal = function(symbol, scope) {
    if (symbol.getType() == SymbolType.Integer) {
        if (symbol.getValue().length > 1 && (symbol.getValue()[1] == 'x' || symbol.getValue()[1] == 'X')) {
            return new Value(parseInt(symbol.getValue()), ValueType.Integer);
        } else if (symbol.getValue().length > 1 && (symbol.getValue()[1] == 'b' || symbol.getValue()[1] == 'B')) {
            return new Value(parseInt(symbol.getValue().slice(2, symbol.getValue().length), 2), ValueType.Integer);
        } else if (symbol.getValue().length > 1 && (symbol.getValue()[1] == 't' || symbol.getValue()[1] == 'T')) {
            return new Value(parseInt("0" + symbol.getValue().slice(2, symbol.getValue().length), 8), ValueType.Integer);
        } else {
            return new Value(parseInt(symbol.getValue()), ValueType.Integer);
        }
    } else if (symbol.getType() == SymbolType.Float) {
        return new Value(parseFloat(symbol.getValue()), ValueType.Float);
    } else if (symbol.getType() == SymbolType.Id) {
        if (!scope.hasOwnProperty(symbol.getValue())) {
            var v = unmarshallIdValue(symbol.getValue());
            if (v == null) {
                throw new Error('unreferenced variable ' + symbol.getValue());
            } else {
                return v;
            }
        } else {
            return scope[symbol.getValue()]
        }
    } else if (symbol.getType() == SymbolType.String) {
        return new Value(symbol.getValue(), ValueType.String);
    } else if (symbol.getType() == SymbolType.Boolean) {
        if (symbol.getValue() == 'true' || symbol.getValue() == 'True' || symbol.getValue() == 'TRUE') {
            return new Value(true, ValueType.Boolean);
        } else {
            return new Value(false, ValueType.Boolean);
        }
    }
    // CASE OF ERRORS
    else if (symbol.getType() == SymbolType.Operator) {
        throw new Error("Operators need one or more operands");
    } else if (symbol.getType() == Separator) {
        throw new Error("Separators alone are meaningless");
    } else {
        throw new Error("TokenType not understood : " + symbol);
    }
}

Interpreter.prototype.do_string = function(cmd, scope) {
    l = new Lexer();
    p = new Parser();
    tokens = l.tokenize(cmd);
    tree   = p.parse(tokens);
    result = this.exec_node(tree);
    marshallIdValue('_', result);
    return result;
}

Interpreter.prototype.test = function(cmd, scope, waiting_for) {
    l = new Lexer();
    p = new Parser();
    tokens = l.tokenize(cmd);
    tree   = p.parse(tokens);
    result = this.exec_node(tree, scope);
    if (!result.equal(waiting_for)) {
        console.warn("ERROR : waiting for " + waiting_for + " and the result was " + result);
        console.warn("Parsed tokens :");
        for (var i=0; i < tokens.length; i++) {
            console.warn(tokens[i]);
        }
        console.warn("Head of the tree :");
        console.warn("    " + tree);
    } else {
        console.log("OK : " + cmd + " => " + result);
    }
    return result;
}

//-----------------------------------------------------------------------------
// Baselib
//-----------------------------------------------------------------------------

Baselib = {
    // Base
    "Base" : {
        "print" : function(target, args, scope) {
            p = args[0];
            console.log(p);
            return new Value(null, ValueType.Object);
        }
    },
    // String
    "String" : {
        "add" : function (target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.String || p.getType() != ValueType.String) {
                throw new Error("Bad param for function String#add");
            }
            return new Value(target.getValue().concat(p.getValue()), ValueType.String);
        },
        "mul" : function (target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.String || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function String#mul");
            }
            if (p.getValue() < 0 || p.getValue() === 1) { new Value(target.getValue(), ValueType.String); }
            else if (p.getValue() === 0) { new Value("", ValueType.String); }
            else if (p.getValue() > 0) {
                s = target.getValue();
                for (var i=0; i < p.getValue()-1; i++) {
                    s = s.concat(target.getValue());
                }
            }
            return new Value(s, ValueType.String);
        },
        "to_s" : function(target, args, scope) {
            if (target.getType() != ValueType.String) {
                throw new Error("Bad param type for function String#to_s");
            }
            return new Value(target.getValue(), ValueType.String);
        }
    },
    // Float
    "Float" : {
        "add" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float || p.getType() == ValueType.Integer) {
                return new Value(target.getValue() + p.getValue(), ValueType.Float);
            } else {
                throw new Error("Bad param type for function Float#add");
            }
        },
        "sub" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float || p.getType() == ValueType.Integer) {
                return new Value(target.getValue() - p.getValue(), ValueType.Float);
            } else {
                throw new Error("Bad param type for function Float#sub");
            }
        },
        "mul" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float || p.getType() == ValueType.Integer) {
                return new Value(target.getValue() * p.getValue(), ValueType.Float);
            } else {
                throw new Error("Bad param type for function Float#mul");
            }
        },
        "div" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float || p.getType() == ValueType.Integer) {
                if (p.getValue() == 0) {
                    throw new Error("Error: divided by zero");
                }
                return new Value(target.getValue() / p.getValue(), ValueType.Float);
            } else {
                throw new Error("Bad param type for function Float#div");
            }
        },
        "mod" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float || p.getType() == ValueType.Integer) {
                return new Value(target.getValue() % p.getValue(), ValueType.Float);
            } else {
                throw new Error("Bad param type for function Float#mod");
            }
        },
        "pow" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float || p.getType() == ValueType.Integer) {
                return new Value(Math.pow(target.getValue(), p.getValue()), ValueType.Float);
            } else {
                throw new Error("Bad param type for function Float#pow");
            }
        },
        "abs" : function(target, args, scope) {
            var v = target.getValue();
            if (v < 0.0) { v = v * -1; }
            return new Value(v, ValueType.Float);
        },
        "inv" : function (target, args, scope) {
            return new Value(-target.getValue() , ValueType.Float);
        },
        "round" : function (target, args, scope) {
            return new Value(Math.round(target.getValue()) , ValueType.Integer);
        },
        "trunc" : function (target, args, scope) {
            return new Value(Math.floor(target.getValue()) , ValueType.Float);
        },
        "floor" : function (target, args, scope) {
            return new Value(Math.floor(target.getValue()) , ValueType.Float);
        },
        "ceil" : function (target, args, scope) {
            return new Value(Math.ceil(target.getValue()) , ValueType.Float);
        },
        "to_s" : function(target, args, scope) {
            return new Value(target.getValue().toString(), ValueType.String);
        },
        "to_i" : function(target, args, scope) {
            return new Value(Math.floor(target.getValue()) , ValueType.Float);
        },
        "to_f" : function(target, args, scope) {
            return new Value(target.getValue(), ValueType.Float);
        },
        "equal" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float) {
                if (target.value === p.value) {
                    return new Value(true, ValueType.Boolean);
                } else {
                    return new Value(false, ValueType.Boolean);
                }
            } else {
                throw new Error("Bad param type for function Float#equal");
            }
        },
        "diff" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Float) {
                if (target.value !== p.value) {
                    return new Value(true, ValueType.Boolean);
                } else {
                    return new Value(false, ValueType.Boolean);
                }
            } else {
                throw new Error("Bad param type for function Float#diff");
            }
        },
        "gt" : function(target, args, scope) {
            var r = Baselib["Float"]["cmp"](target, args, scope);
            if (r.value === 1) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "ge" : function(target, args, scope) {
            var r = Baselib["Float"]["cmp"](target, args, scope);
            if (r.value === 1 || r.value === 0) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "lt" : function(target, args, scope) {
            var r = Baselib["Float"]["cmp"](target, args, scope);
            if (r.value === -1) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "le" : function(target, args, scope) {
            var r = Baselib["Float"]["cmp"](target, args, scope);
            if (r.value === -1 || r.value === 0) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "cmp" : function(target, args, scope) {
            p = args[0];
            if (p.getType() != ValueType.Integer && p.getType() != ValueType.Float) {
                throw new Error("Bad param type for function Float#cmp");
            }
            if (target.getValue() == p.getValue()) { return new Value(0, ValueType.Integer); }
            else if (target.getValue() > p.getValue()) { return new Value(1, ValueType.Integer); }
            else { return new Value(-1, ValueType.Integer); }
        }, 
    },
    "Boolean" : {
        "and" : function (target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Boolean) {
                return new Value(target.getValue() && p.getValue(), ValueType.Boolean);
            } else {
                throw new Error("Bad param type for function Boolean#and");
            }
        },
        "or" : function (target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Boolean) {
                return new Value(target.getValue() || p.getValue(), ValueType.Boolean);
            } else {
                throw new Error("Bad param type for function Boolean#or");
            }
        },
        "xor" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Boolean) {
                var r = false;
                if (target.getValue() && p.getValue) {
                    r = false;
                } else if (target.getValue()) {
                    r = true;
                } else if (p.getValue()) {
                    r = true;
                }
                return new Value(r, ValueType.Boolean);
            } else {
                throw new Error("Bad param type for function Boolean#xor");
            }
        },
        "inv" : function(target, args, scope) {
            return new Value(!target.getValue(), ValueType.Boolean);
        },
        "to_s" : function(target, args, scope) {
            if (target.getValue()) {
                return new Value("true", ValueType.String);
            } else {
                return new Value("false", ValueType.String);
            }
        },
        "to_i" : function(target, args, scope) {
            if (target.getValue()) {
                return new Value(1, ValueType.Integer);
            } else {
                return new Value(0, ValueType.Integer);
            }
        },
        "to_f" : function(target, args, scope) {
            if (target.getValue()) {
                return new Value(1.0, ValueType.Float);
            } else {
                return new Value(0.0, ValueType.Float);
            }
        },
        "equal" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Boolean) {
                if (target.value === p.value) {
                    return new Value(true, ValueType.Boolean);
                } else {
                    return new Value(false, ValueType.Boolean);
                }
            } else {
                throw new Error("Bad param type for function Boolean#equal");
            }
        },
        "diff" : function(target, args, scope) {
            p = args[0];
            if (p.getType() == ValueType.Boolean) {
                if (target.value !== p.value) {
                    return new Value(true, ValueType.Boolean);
                } else {
                    return new Value(false, ValueType.Boolean);
                }
            } else {
                throw new Error("Bad param type for function Boolean#diff");
            }
        },
    },
    // Integer
    "Integer" : {
        "add" : function (target, args, scope) {
            var p = args[0];
            if (p.getType() == ValueType.Float) {
                return new Value(target.getValue() + p.getValue(), ValueType.Float);
            } else if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#add");
            }
            return new Value(target.getValue() + p.getValue(), ValueType.Integer);
        },
        "sub" : function (target, args, scope) {
            var p = args[0];
            if (p.getType() == ValueType.Float) {
                return new Value(target.getValue() - p.getValue(), ValueType.Float);
            } else if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#sub");
            }
            return new Value(target.getValue() - p.getValue(), ValueType.Integer);
        },
        "mul" : function (target, args, scope) {
            var p = args[0];
            if (p.getType() == ValueType.Float) {
                return new Value(target.getValue() * p.getValue(), ValueType.Float);
            } else if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#mul");
            }
            return new Value(target.getValue() * p.getValue(), ValueType.Integer);
        },
        "div" : function (target, args, scope) {
            var p = args[0];
            if (p.getType() != ValueType.Integer && p.getType() != ValueType.Float) {
                throw new Error("Bad param type for function Integer#div");
            }
            if (p.getValue() == 0) {
                throw new Error("Error: divided by zero");
            }
            var r = target.getValue() / p.getValue();
            if (r == Math.floor(r) && p.getType() == ValueType.Integer) {
                return new Value(r, ValueType.Integer);
            } else {
                return new Value(r, ValueType.Float);
            }
        },
        "mod" : function (target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#mod");
            }
            return new Value(target.getValue() % p.getValue(), ValueType.Integer);
        },
        "pow" : function (target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#pow");
            }
            return new Value(Math.pow(target.getValue(), p.getValue()), ValueType.Integer);
        },
        "intdiv" : function (target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#intdiv");
            }
            return new Value(Math.floor(target.getValue() / p.getValue()), ValueType.Integer);
        },
        "inv" : function (target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#inv");
            }
            return new Value(-target.getValue() , ValueType.Integer);
        },
        "to_s" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#to_s");
            }
            return new Value(target.getValue().toString(), ValueType.String);
        },
        "to_i" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#to_i");
            }
            return new Value(target.getValue(), ValueType.Integer);
        },
        "to_f" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#to_f");
            }
            return new Value(target.getValue(), ValueType.Float);
        },
        "abs" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#to_s");
            }
            var v = target.getValue();
            if (v < 0) { v = v * -1; }
            return new Value(v, ValueType.Integer);
        },
        "lshift" : function(target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#lshift");
            }
            return new Value(target.getValue() << p.getValue(), ValueType.Integer);
        },
        "rshift" : function(target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#rshift");
            }
            return new Value(target.getValue() >> p.getValue(), ValueType.Integer);
        }, 
        "and" : function(target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#and");
            }
            return new Value(target.getValue() & p.getValue(), ValueType.Integer);
        },
        "or" : function(target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#or");
            }
            return new Value(target.getValue() | p.getValue(), ValueType.Integer);
        }, 
        "xor" : function(target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || p.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#xor");
            }
            return new Value(target.getValue() ^ p.getValue(), ValueType.Integer);
        }, 
        "invbin" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#invbin");
            }
            return new Value(~ target.getValue(), ValueType.Integer);
        },
        "cmp" : function(target, args, scope) {
            p = args[0];
            if (target.getType() != ValueType.Integer || (p.getType() != ValueType.Integer && p.getType() != ValueType.Float)) {
                throw new Error("Bad param type for function Integer#cmp");
            }
            if (target.getValue() == p.getValue()) { return new Value(0, ValueType.Integer); }
            else if (target.getValue() > p.getValue()) { return new Value(1, ValueType.Integer); }
            else { return new Value(-1, ValueType.Integer); }
        }, 
        "size" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#size");
            }
            return new Value(roughSizeOfObject(target), ValueType.Integer);
        }, 
        "gt" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#gt");
            }
            var r = Baselib["Integer"]["cmp"](target, args, scope);
            if (r.value === 1) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "ge" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#ge");
            }
            var r = Baselib["Integer"]["cmp"](target, args, scope);
            if (r.value === 1 || r.value === 0) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "lt" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#lt");
            }
            var r = Baselib["Integer"]["cmp"](target, args, scope);
            if (r.value === -1) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "le" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer) {
                throw new Error("Bad param type for function Integer#le");
            }
            var r = Baselib["Integer"]["cmp"](target, args, scope);
            if (r.value === -1 || r.value === 0) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "equal" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer && target.getType() != ValueType.Float) {
                throw new Error("Bad param type for function Integer#size");
            }
            var r = Baselib["Integer"]["cmp"](target, args, scope);
            if (r.value === 0) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
        "diff" : function(target, args, scope) {
            if (target.getType() != ValueType.Integer && target.getType() != ValueType.Float) {
                throw new Error("Bad param type for function Integer#size");
            }
            var r = Baselib["Integer"]["cmp"](target, args, scope);
            if (r.value !== 0) {
                return new Value(true, ValueType.Boolean);
            } else {
                return new Value(false, ValueType.Boolean);
            }
        },
    }
};

// http://stackoverflow.com/questions/1248302/javascript-object-size
function roughSizeOfObject( object ) {

    var objectList = [];
    var stack = [ object ];
    var bytes = 0;

    while ( stack.length ) {
        var value = stack.pop();

        if ( typeof value === 'boolean' ) {
            bytes += 4;
        }
        else if ( typeof value === 'string' ) {
            bytes += value.length * 2;
        }
        else if ( typeof value === 'number' ) {
            bytes += 8;
        }
        else if
        (
            typeof value === 'object'
            && objectList.indexOf( value ) === -1
        )
        {
            objectList.push( value );

            for(var i in value ) {
                stack.push( value[ i ] );
            }
        }
    }
    return bytes;
}

root_scope = {
    'Pi' : Value(Math.PI, ValueType.Float),
    'PI' : Value(Math.PI, ValueType.Float),
    '_'  : Value(null, ValueType.Object),
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

test_interpreter.test("2", root_scope, new Value(2, ValueType.Integer));
test_interpreter.test("0b10", root_scope, new Value(2, ValueType.Integer));
test_interpreter.test("0xA", root_scope, new Value(10, ValueType.Integer));
test_interpreter.test("0t10", root_scope, new Value(8, ValueType.Integer));

function i(v) {
    return new Value(v, ValueType.Integer);
}

function b(v) {
    return new Value(v, ValueType.Boolean);
}

function nihil() {
    return new Value(null, ValueType.Object);
}

// Test from nn
// Integer
test_interpreter.test('2+3', root_scope, i(5));
test_interpreter.test('2', root_scope, i(2));
test_interpreter.test('(2+2)*3', root_scope, i(12));
test_interpreter.test('3*(2+2)', root_scope, i(12));
test_interpreter.test('3*2+2', root_scope, i(8));
test_interpreter.test('(3+2)*(2*2)', root_scope, i(20));
test_interpreter.test('(3)', root_scope, i(3));
// Boolean
test_interpreter.test('a = true', root_scope, nihil()); //v(true))
test_interpreter.test('true == true', root_scope, b(true));
test_interpreter.test('true == false', root_scope, b(false));
test_interpreter.test('false == false', root_scope, b(true));
//test_interpreter.test('not true', root_scope, b(false));
//test_interpreter.test('not false', root_scope, b(true));
test_interpreter.test('a', root_scope, b(true));
//test_interpreter.test('not a', root_scope, b(false));
test_interpreter.test('true and true', root_scope, b(true));
test_interpreter.test('true and false', root_scope, b(false));
test_interpreter.test('false and true', root_scope, b(false));
test_interpreter.test('false or true', root_scope, b(true));
test_interpreter.test('true or false', root_scope, b(true));
test_interpreter.test('true and true and false', root_scope, b(false));
test_interpreter.test('false or false or true', root_scope, b(true));
test_interpreter.test('false and false or true', root_scope, b(true));
test_interpreter.test('false and (false or true)', root_scope, b(false));
            
//-----------------------------------------------------------------------------
// GUI
//-----------------------------------------------------------------------------

function do_node(node) {
    var s = '';
    if (node == null) {
        s = '';
    } else if (node.terminal()) {
        s = "<li>" + node.toString() + "</li>"; //node.getValue() + " : " + node.getType() + "</li>";
    } else {
        s = "<li>" + node.toString();
        //if (node.getValue() == null) { s = "<li>" + node.toString(); }
        //else { s = "<li>" + node.getValue() + " : " + node.getType(); }
        s += "<ol start='0'>";
        for(var i = 0; i < node.getLength(); i++) {
            s += do_node(node.suite[i]);
        }
        s += "</ol></li>";
    }
    return s;
}
