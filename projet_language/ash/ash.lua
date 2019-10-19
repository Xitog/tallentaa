-------------------------------------------------------------------------------
-- Strengths and weaknesses of Lua
-------------------------------------------------------------------------------

-- Specific Strengths
--      -- for comments
--      # for length
--      = for key, val in table

-- Strenghs shared with other dynamic languages
--      no need to define or declare a function before calling it

-- Weaknesses
--      no combined arithmethic operator += -=
--      ~= for !=
--      pas de tuples, list et dict fusionnés
--          => on ne peut pas tester simplement si une clé existe ! a = {'bbb'} ; a['bbb'] = nil comme a['ccc'] = nil !
--          => on peut faire des trous ! a[0] = 'aaa' mais aussi a['5'] = 'ccc'
--      elseif au lieu de elif
--      obligation de mettre local => sinon c'est global !
--      no const
--      no check of the number of parameters passed to a function
--      no type hint
--      in ne s'utilise qu'avec pairs ou ipairs, on peut pas faire for i in var
--      string key must be surrounded by [] => ['key'] = val
--      no line separator!
--      fusion de int et float en number

-------------------------------------------------------------------------------
-- List of functions
-------------------------------------------------------------------------------

-- read(filepath)                           Read the content of a file
-- tokenize(code)                           Transform a string of content into a table of tokens
-- read_string(code, start, tokens)         Read a string (called by tokenize)
-- read_number(code, start, tokens)         Read a number (called by tokenize)
-- read_identifier(code, start, tokens)     Read an identifier (called by tokenize)
-- read_special_char(code, start, tokens)   Read a special char (called by tokenize)

-- string.sub renvoie "" si pos > #code et donc string.match("", whatever) renvoie nil comme si elle ne le trouvait pas !

-------------------------------------------------------------------------------
-- Definition of token types
-------------------------------------------------------------------------------

STRING       = 'string'
INTEGER      = 'integer'
FLOAT        = 'float'
BOOLEAN      = 'boolean'

NEWLINE      = 'newline'

IDENTIFIER   = 'identifier'
KEYWORD      = 'keyword'

OPEN_PAR     = 'opening parenthesis'
CLOSE_PAR    = 'closing parenthesis'

DOUBLE_QUOTE = 'double quote'

OPERATOR     = 'operator'

KEYWORD_LIST = {['if'] = true, ['then'] = true, ['else'] = true, ['elif'] = true, ['end'] = true, ['for'] = true, ['do'] = true, ['in'] = true, 
                ['true'] = true, ['false'] = true, ['and'] = true, ['or'] = true, ['not'] = true}

-------------------------------------------------------------------------------
-- Tool functions
-------------------------------------------------------------------------------

function read(filepath)
    local file = assert(io.open(filepath, "rb"))
    local data = file:read("*all")
    file:close()
    return data
end

function error(message)
    print(message)
    os.exit(1)
end

-------------------------------------------------------------------------------
-- Tokenizer
-------------------------------------------------------------------------------

function tokenize(code)
    local tokens = {}
    local line = 1
    local col = 0
    local i = 1
    while i <= #code do
        c = string.sub(code, i, i)
        --print(c, i)
        col = col + 1
        if col == 1 and c == '-' and i+1 <= #code and string.sub(code, i+1, i+1) == '-' then
            while c ~= '\n' do
                i = i + 1
                c = string.sub(code, i, i)
            end
        end -- not else : we want to activate the c == '\n' treatment
        if string.match(c, '"') ~= nil then
            index_last = read_string(code, i, tokens)
            str = string.sub(code, i, index_last)
            tokens[#tokens+1] = STRING .. '::' .. str
            i = index_last + 1
        elseif string.match(c, "%d") ~= nil then
            index_last, is_float = read_number(code, i, tokens)
            num = string.sub(code, i, index_last)
            if is_float then
                typ= FLOAT
            else
                typ = INTEGER
            end
            tokens[#tokens+1] = typ .. '::' .. num
            i = index_last + 1
        elseif string.match(c, "%a") ~= nil then
            index_last = read_identifier(code, i, tokens)
            id = string.sub(code, i, index_last)
            if KEYWORD_LIST[id] then
                if id == 'false' or id == 'true' then
                    typ = BOOLEAN
                else
                    typ = KEYWORD
                end
            else
                typ = IDENTIFIER
            end
            tokens[#tokens+1] = typ .. '::' .. id
            i = index_last + 1
        elseif c == '\n' then
            tokens[#tokens+1] = NEWLINE
            line = line + 1
            col = 0
            i = i + 1
        elseif string.match(c, "[(\"')+-=.]") then
            tt, index_last = read_special_char(code, i, tokens)
            sc = string.sub(code, i, index_last)
            tokens[#tokens+1] = tt .. '::' .. sc
            i = index_last + 1
        elseif string.match(c, "[ \t\r]") then
            i = i + 1
        else
            error("[ERROR] Unknown char at line " .. line .. ", column " .. col .. ": [" .. c .. "]")
        end
    end
    return tokens
end

function read_string(code, start, tokens)
    local i = start + 1
    local c = string.sub(code, i, i)
    while c ~= "" and c ~= '"' do
        i = i + 1
        c = string.sub(code, i, i)
    end
    if c == "" then
        error("[ERROR] Non terminated string.")
    end
    return i
end

function read_number(code, start, tokens)
    local i = start
    local c = string.sub(code, i, i)
    local is_float = false
    while string.match(c, "%d") ~= nil or (c == '.' and not is_float)  do
        if c == '.' then
            if i+1 <= #code and string.sub(code, i+1, i+1) == '.' then -- case 1..5 => a float will always be 1.0 never 1.
                break
            end
            is_float = true
        end
        i = i + 1
        c = string.sub(code, i, i)
    end
    return i - 1, is_float
end

function read_identifier(code, start, tokens)
    local i = start
    local c = string.sub(code, i, i)
    while string.match(c, "%a") ~= nil do
        i = i + 1
        c = string.sub(code, i, i)
    end
    return i - 1
end

function read_special_char(code, start, tokens)
    local i = start
    local c = string.sub(code, i, i)
    if c == '(' then
        return OPEN_PAR, i
    elseif c == ')' then
        return CLOSE_PAR, i
    elseif c == '"' then
        return DOUBLE_QUOTE, i
    elseif c == '+' then
        return OPERATOR, i
    elseif c == '-' then
        return OPERATOR, i
    elseif c == '.' then
        if i+1 <= #code and string.sub(code, i+1, i+1) == '.' then
            return OPERATOR, i+1
        else
            return OPERATOR, i
        end
    elseif c == '=' then
        if i+1 <= #code and string.sub(code, i+1, i+1) == '=' then
            return OPERATOR, i+1
        else
            return OPERATOR, i
        end
    end
    print("Unknown char :" .. c)
end

-------------------------------------------------------------------------------
-- Parser
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- Interpreter
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- Lua transpiler
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- Main code
-------------------------------------------------------------------------------

code = read("code.ash")
--io.write(code)
tokens = tokenize(code)
for i, tok in ipairs(tokens) do
    print(i, tok)
end
