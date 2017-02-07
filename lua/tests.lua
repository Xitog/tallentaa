-------------------------------------------------
-- Dealing with the console
-------------------------------------------------

write = io.write

print("hello 1")
print("hello 2");
write("hello 3 "); write("world") ; write("\n")
write("hello 4\n")
print("hello 5") print("hello 6")
a = 5 b = 22 -- valid !!!
print(a) b = b + 1 -- valid !!!
print(b)

-------------------------------------------------
-- SEQUENCE
-------------------------------------------------

-- ; is not a separator but an optional terminator
-- Grammar : chunk ::= {stat [`;´]}

a = 5 b = 6 -- New line doesn't mean anything
c = { 10, 20, 30, 40, 50}
d = { alpha = 55, beta = 66, zeta = null, ["zorba"] = "youpi" }

-------------------------------------------------
-- Selection
-------------------------------------------------

-- (for me) A condition should always be a boolean.
-- is false = nil, false
-- is true = {}, "", 0

if {} then
    print("empty table is true")
else
    print("empty table is false")
end

if "" then
    print("empty string is true")
else
    print("empty string is false")
end

if 0 then
    print("0 is true")
else
    print("0 is false")
end

if nil then
    print("nil is true")
else
    print("nil is false")
end

if false then
    print("false is true")
else
    print("false is false")
end

a = 5
if a == 5 then
    print("a = 5")
elseif a == 6 then
    print("a = 6")
else
    print("a = undefined")
end

-- operator boolean : and or not
if a == 5 and b == 6 then
    print("a equals 5 and b equals " .. b) -- concat string with ..
end

if not false then -- test it
    print("true")
end

-------------------------------------------------
-- Itération
-------------------------------------------------

-------------------------------------------------
-- WHILE / UNTIL
-------------------------------------------------

a = 5
while a > 0 do
    print("while a > 0 and a=", a)
    a = a - 1 -- no x= operators
end -- no else in while loop

a = 5
repeat
    print("until a == 0 and a=", a)
    a = a - 1
until a == 0

-- no a x= operator
-- no else after while

-------------------------------------------------
-- FOR
-------------------------------------------------

-- i=min, max[, step]
for i=1, 5, 2 do
    print("i=", i)
end
-- no else
-- i is local to the for
print(i) -- print nil

for i=1, 5 do
    print("for will break at 3, i=", i) 
    if i == 3 then
        break
    end
end
-- no continue or next

for i=1, 5 do
    if i % 2 == 0 then
    end
end

a = {1, 3, 7, 8, 22}
for index, value in ipairs(a) do
    print(index, " => ", value)
end
print(#a)

for key, value in pairs(d) do
    print(key, ' => ', value) -- zeta is not treated
end

if d.zeta then
    print("never will be")
else
    print("zeta key value is null")
end

if d.nokey then
    print("never will be")
else
    print("nokey doesn't exist")
end

repeat
    print(a)
    a = a + 1
until a >= 5

-------------------------------------------------
-- TYPES
-------------------------------------------------

print(type(4))
print(type("abc"))
print(type({}))

-- String
a = "abc"
a = 'abc'
a = "ab" .. "c" -- concat
print(a)

-- Boolean
a = true
b = false
c = not b
print(c)

-- Numbers
a = 1.0
b = 1

-- Table (list)
a = { 1, 2, 3, 4, 5}
print(a)
print(#a)
print(a[5])
-- print(a.5) forbidden

-- http://lua-users.org/wiki/CopyTable

-- Table (dict)
a = { abc = 1, def = 2, ["ghi"] = 3, zyg = nil }
print(a.abc)
print(a["def"])
print(#a) -- return 0 !
print(a.ghi)
if a.zyg then -- value is nul
    print("a.zyg is true")
else
    print("a.zyg is false")
end
if a.zem then -- key is not defined
    print("a.zem is true")
else
    print("a.zem is false")
end

-- Matrix
matrix = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0},
    {0, 0, 0, 0, 1, 0},
    {0, 0, 2, 1, 1, 0},
    {0, 0, 1, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
}
matrix.size = 6
for line, vline in ipairs(matrix) do
    for col, value in ipairs(vline) do
        io.stdout:write(value .. ' ')
    end
    print()
end
print("Line 4 Column 3 =" .. matrix[4][3]) -- y puis x
print(matrix.size)

-- Table & metatable (10h38 : that's ok :-)
people_class_methods = {
    new = function(default_name)
        i = {}
        setmetatable(i, {__index = people_instance_methods})
        i:init(default_name)
        return i
    end
}
people_instance_methods = {
    init = function(self, default_name)
        self.name = default_name
    end,
    hello = function(self)
        print("Hello! I'm " .. self.name)
    end,
    setname = function(self, new_name)
        self.name = new_name
    end,
}

p1 = people_class_methods.new("Bob")
p1:hello()
p1:setname("Zorba")
p1:hello()

-------------------------------------------------
-- OO
-------------------------------------------------

Class = {}
Class.to_s = "Class"
Class.class = Class
Class.methods = {}
setmetatable(Class, {
    __index = Class.methods
})

Person = {}
Person.count = 0 -- static var
Person.to_s = "Person prop"
Person.class = Class
Person.methods = {} -- instance methods
setmetatable(Person, {
    __index = Person.methods
})
function Person.methods.birthday(obj) -- declaration of an instance method
    print("Happy birthday " .. obj.name .. "!")
end
function Person.new(name, age) -- declaration of a static method
    -- local a = {table.unpack(Person)} -- necessary?
    local a = {}
    a.name = name
    a.age = age
    a.class = Person
    local mt = getmetatable(Person)
    setmetatable(a, mt)
    Person.count = Person.count + 1
    return a
end
function Person.to_s()
    return "Person"
end

print(Person.count)
Bob = Person.new("Bob", 32)
print(Person.count)
Bob:birthday()
Bob.birthday(Bob)
print(Bob.name)
print(Bob.class.to_s())
print(Bob.class.to_s) -- Effacement de la prop au profit de la fonction !
-- Person.birthday() -- attempt to index a nil value (local 'obj') Parfait !
print(Bob.class.class.to_s)

-- 14h04 it's working!

-------------------------------------------------
-- Standard lib
-------------------------------------------------

-- Open / Write files
f = io.open("pipo.txt", "w")
if f == nil then
    print("Pb to open in w mode")
end
f:write("hello pipo!\n")
f:write("another line to the pipo!\n")
f:close()

f = io.open("pipo.txt", "r")
s = f:read("*line") -- read only one line by default, () equivalent to ("*line")
print("read one (text, line): " .. s)
f:close()

f = io.open("pipo.txt", "r") -- in C, when you read in text mode, end of line are converted to standard "\n"
s = f:read("*all")
print("read two (text, all): " .. s)
f:close()

f = io.open("pipo.txt", "rb")
s = f:read("*all")
print("read three (binary, all): " .. s)
f:close()

lines = 0
for line in io.lines("pipo.txt") do
    print(lines .. " : " .. line)
    lines = lines + 1
end

-- Read / write on stdin
io.stdout:write("Enter a line:\n")
s = io.stdin:read()
print(s)

-------------------------------------------------
-- Map (~04/01/2017)
-------------------------------------------------

-- ne pas savoir simplement la longueur d'une table "hash/dict" et non "array/list" (alors que les versions précédentes le permettait avec getn : non ct équivalent à #).

-- A layer is a simple matrix of size*size full of base
function create_layer(size, base)
    local layer = {}
    for i = 1, size do
        layer[i] = {}
        for j = 1, size do
            layer[i][j] = base
        end
    end
    layer.base = base
    layer.size = size
    return layer
end

function print_layer(layer)
    print("++ Print layer ++")
    print("Size : " .. layer.size .. " x " .. layer.size)
    for i = 1, layer.size do
        for j = 1, layer.size do
            io.write(layer[i][j])
        end
        print()
    end
    print("-- Print layer --")
end

-- A map consist of layers
-- layers can be indexed by numbers or keys
function create_map(size, base, layer)
    local map = {}
    -- print(type(layer))
    if type(layer) == "number" then
        for i = 1, layer do
            map[i] = create_layer(size, base)
        end
    elseif type(layer) == "table" then
        for i, v in ipairs(layer) do
            map[v] = create_layer(size, base)
        end
    else
        return nil
    end
    map.size = size
    map.base = base
    return map
end

-- Test layers & map
world1 = create_map(10, 0, 3)
print(world1[3][10][10])
print_layer(world1[3])

world2 = create_map(10, 22, { "sol", "brou", "unit" })
print(world2.sol[10][10])
print_layer(world2.sol)

-- 15h43 ça marche !

function is_free(layer, x1, y1, x2, y2)
    return #get_not_free(layer, x1, y1, x2, y2) == 0
end

function get_not_free(layer, x1, y1, x2, y2)
    local x_max = math.max(x1, x2)
    local x_min = math.min(x1, x2)
    local y_max = math.max(y1, y2)
    local y_min = math.min(y1, y2)
    local not_free = {}
    for i = x_min, x_max do
        for j = y_min, y_max do
            -- io.write(layer[i][j])
            if layer[i][j] ~= layer.base then
                table.insert(not_free, {i, j})
            end
        end
        --print()
    end
    return not_free
end

function print_table(tbl)
    print("++ Print table ++")
    if tbl ~= nil and #tbl > 0 then
        io.write('Table : ')
        for k, v in pairs(tbl) do
            io.write(k, ' = ', v[1], ':', v[2], '  , ')
        end
        print()
    elseif tbl ~= nil then
        print("Empty table")
    end
    print("-- Print table --")
end

--[[
a = {1, 2, 3}
print_table(a)

function ret_table()
    local b = {1, 2, 3}
    return b
end
print_table(ret_table())
--]]

layer1 = create_layer(10, 0)
layer1[5][5] = 1
print(layer1[5][5])
print(type(is_free(layer1, 5, 5, 5, 5)))
print_table(get_not_free(layer1, 5, 5, 5, 5))
print(is_free(layer1, 5, 5, 5, 5))
print_table(get_not_free(layer1, 1, 1, 1, 1))
print(is_free(layer1, 1, 1, 1, 1))
print_table(get_not_free(layer1, 1, 1, 10, 10))
print(is_free(layer1, 1, 1, 10, 10))

layer1[7][3] = 2
layer1[9][2] = 3
print_table(get_not_free(layer1, 1, 1, 10, 10))
print(is_free(layer1, 1, 1, 10, 10))

math.randomseed(os.time())
for i=1, 10 do
    r = math.random(20)
    io.write(r, '  ')
end
print()

function create_room(world, layer, x, y, w, h, content)
    for i = x, x+w do
        for j = y, y+h do
            world[layer][i][j] = content
        end
    end
    return x, y, w, h
end

function create_random_room(world, layer, max_w, max_h, content)
    local w = math.random(max_w)
    local h = math.random(max_h)
    local x = math.random(world.size - w - 1)
    local y = math.random(world.size - h - 1)
    create_room(world, layer, x, y, w, h, content)
end

world3 = create_map(30, 0, { "sol", "brou", "unit" })
for i=1, 3 do
    create_random_room(world3, "sol", 5, 5, '_')
end
print_layer(world3.sol)

-- 15h23

-------------------------------------------------
-- Brouillard calc (~04/01/2017)
-------------------------------------------------

x = 5
local y = 7
function localize()
    print("x=", x) -- 5
    print("y=", y) -- 7 recognize
end
localize()

function brou(x, y, vision)
    local xstart = x - vision
    local xend = x + vision
    local ystart = y - vision
    local yend = y + vision
    print("X =", x, "Y =", y)
    print("X from ", xstart, "to", xend)
    print("Y from ", ystart, "to", yend)
    for i = xstart, xend do
        for j = ystart, yend do
            local brou = vision - math.max(math.abs(x-i), math.abs(y-j)) -- 15h51 : working (vision -) !!!
            if i == x or j == y then 
                brou = brou + 1
            end
            io.write(brou .. ' ')
        end
        print()
    end
end

x = 5
y = 5
vision = 3
brou(x, y, vision)

x = 10
y = 10

vision = 4
brou(x, y, vision)

vision = 5
brou(x, y, vision)

-- V3 7x7 => Vision x 2 + 1
-- [0, 0, 0, 1, 0, 0, 0]
-- [0, 1, 1, 2, 1, 1, 0]
-- [0, 1, 2, 3, 2, 1, 0]
-- [1, 2, 3, _, 3, 2, 1]
-- [0, 1, 2, 3, 2, 1, 0]
-- [0, 1, 1, 2, 1, 1, 0]
-- [0, 0, 0, 1, 0, 0, 0]

-- 16h00 tout marche, c'est beau :-) Cela me servira pour Python aussi.

-- get adjacent space

-- choisi un sens (S, O, E, N)
-- regarde si tu peux construire une salle à 1 case en fonction des tailles.
-- Une salle à forcément une "next salle" et potentiellement une "adjacente salle" (impasse avec trésors).

-------------------------------------------------
-- LÖVE
-------------------------------------------------

f = io.open("bonjour.txt", "r")
nb = 1
for line in f:lines() do
    print(nb, line)
    --for cha = 1, #line do
        -- print(line:sub(cha, cha))
        --if cha == " " then
         --   spaces = spaces + 1
        --end
        --if spaces % 4 == 0 then
        --    print("it's a tab!", line)
        --end
    --end
    if #line > 4 and line:sub(1, 4) == "    " then
        print("it's a tab!", line)
    end
    nb = nb + 1
end
io.close(f)

-- Metatables I

instance = {age = 32, nom = "Bob"}
fonctions_instance = {
    birthday = function(i)
        i.age = i.age + 1
    end,
    to_s = function(i)
        return i.nom .. " (" .. i.age .. ")"
    end
}
metatable = {
    __index = fonctions_instance
}
setmetatable(instance, metatable)
print(instance.to_s(instance))
print(instance:to_s())

-- 9h52 : c'est bon.

-- Metatables II
--[[ On fusionne la table des fonctions et la metatable

instance2 = {age = 32, nom = "Bob"}
fonctions_instance2 = {
    birthday = function(i)
        i.age = i.age + 1
    end,
    to_s = function(i)
        return i.nom .. " (" .. i.age .. ")"
    end,
    __index = fonctions_instance2 -- semble pas lui convenir.
}
setmetatable(instance2, fonctions_instance2)
print(instance2.to_s(instance2))
print(instance2:to_s())

-- 9h54 : c'est bon : non en fait, il regardait l'ancienne...]]

a = { [1] = "abc", [10] = "cde" }
for k, v in ipairs(a) do
    print(k, v)
end
-- print 1 abc

a = { [1] = "abc", [2] = "cde", [10] = "fgh" }
for k, v in ipairs(a) do
    print(k, v)
end
-- print 1 abc
-- print 2 cde
-- s'arrête dès qu'il y a un nil


f = io.open("bonjour.txt", "r")
content = f:read("*all")
f:close()
print(content)
letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'é', 'è', 'ë', 'ê', 'â', 'œ', 'ç', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'É', 'x', 'Ë', 'Ê'; 'Â', 'x', 'x', 'Ç'}
symbols = {',', ';', '!', '?', '.'}
table_fct_methods = {
    has = function (table, value)
        for k, v in pairs(table) do
            if v == value then
                return true
            end
        end
        return false
    end,
}
table_meta = {
    __index = table_fct_methods
}
setmetatable(letters, table_meta)

function info(table)
    print("-- Content of the table :")
    for key, value in pairs(table) do
        print(" ", key, value)
    end
    print("-- End content")
end
info(getmetatable(letters))

-- Create tex dico
local tex_dico = {}
local word = ""
for i=1, #content do
    -- print(content:sub(i, i))
    local c = content:sub (i, i)
    if letters:has(c) then
        word = word .. c
    else
        if word ~= "" then
            print("Word = ", word)
            table.insert(tex_dico, word)
            word = ""
        end
    end
end
if word ~= "" then
    print("Last word = ", word)
end

-- Load old dico
f = io.open("dico.txt", "r")
local old_dico = {}
if f ~= nil then
    for line in f:lines() do
        line:gsub("\n", "")
        table.insert(old_dico, line)
    end
    f:close()
else
    print("Dictionary file not found.")
end
setmetatable(old_dico, table_meta)
info(old_dico)

-- Check tex dico against old dico
new_dico = {}
for i, v in ipairs(tex_dico) do
    if old_dico:has(v) then
        print('old word :', v)
    else
        print('new word :', v)
        table.insert(new_dico, v)
    end
end

-- Save new words
f = io.open("dico.txt", "a")
for i, v in ipairs(new_dico) do
    f:write(v .. '\n')
end
f:close()


--for line in f:read() do
--    print(line)
--end

-- 15h05 : ça marche :-) !

-- http://lua-users.org/wiki/TablesTutorial
-- http://lua-users.org/wiki/CommonFunctions ***
-- exemple de split
--[[
function assert_equal(a, b)
  if a ~= b then error(tostring(a) .. " == " .. tostring(b), 2) end
end
--]]
-- http://lua-users.org/wiki/StringLibraryTutorial
-- read(*all)
-- https://www.lua.org/pil/21.1.html
-- https://www.lua.org/pil/21.2.html
-- https://www.lua.org/pil/2.4.html

---------------------------------------------------------------------
-- Exemple de Löve
---------------------------------------------------------------------

-- Lecture de fichier
f = io.open("bonjour.txt", "r")
for line in f:lines() do
    print(line)
    if #line > 4 and line:sub(0, 4) == "wall" then
        print("It's a wall!")
        coordinates = line:sub(6)
        print(coordinates)
        -- 1h37 Yes ! Pas de split en Lua
        for x1, y1, x2, y2 in coordinates:gmatch("(%d+),(%d+) %- (%d+),(%d+)") do
            print(x1, y1, x2, y2)
            wall = { x1, y1, x2, y2 }
        end
    end
end

-- Dessin

player = {
    x = 10,
    y = 10
}

SPEED = 200

function love.update(deltatime)
    x, y = love.mouse.getPosition()
    if love.keyboard.isDown("right") then
        player.x = player.x + SPEED * deltatime
    end
    if love.keyboard.isDown("left") then
        player.x = player.x - SPEED * deltatime
    end
    if love.keyboard.isDown("down") then
        player.y = player.y + SPEED * deltatime
    end
    if love.keyboard.isDown("up") then
        player.y = player.y - SPEED * deltatime
    end
end

function love.draw()
    -- 1h43 : Yes ! Une ligne . Le dernier est l'alpha...
    love.graphics.setColor( 0, 0, 0, 255)
    love.graphics.rectangle( "fill", 10, 10, 100, 100 )
    love.graphics.setColor( 255, 255, 255, 255)
    love.graphics.line(player.x, player.y, 100, 10)
end

-- 1h44 : on a les bases :-)

---------------------------------------------------------------------
-- Metatable
---------------------------------------------------------------------

str = "Bonjour, Tom. Tu vas bien ?"
word = ""
separators = { " ", ".", "?", "!" }

-- même pas de fonction "in" en Lua...
function has (table, value)
    for k, v in pairs(table) do
        if v == value then
             return true
        end
    end
    return false
end

-- metatable_for_table = { ["has"] = has }
-- metatable_for_table = { has = has }

metatable_for_table = {
    xhas = function (table, value)
        print("this language is crazy")
        return has(table, value)
    end,
    __add = function (t1, t2)
        print("pipo1")
    end,
    __index = function(t, key)
        if key == "foo" then
            return 0
        else
            return metatable_for_table[key] -- la solution est là !!!
        end
  end
}

print(1, metatable_for_table.xhas)
setmetatable(separators, metatable_for_table)
print(2, metatable_for_table.xhas)
print(3, separators.xhas)

a = {1, 2, 3}
ma_table_des_fonctions = {
    foo = 3
}
ma_metatable = {
    __index = ma_table_des_fonctions
}
function ma_table_des_fonctions.pipo()
    print("pipoX")
    print("oups")
    return "ouf!"
end
setmetatable(a, ma_metatable)
print("Victoire?", a.foo)
print("Victoire2?", a.pipo())

--function metatable_for_table.xhas (table, value)
--    return has(table, value)
--end

--[[print(getmetatable(separators))
for k, i in pairs(getmetatable(separators)) do
    print(k, v)
    if v == nil then
        getmetatable(separators)[k] = function ()
            print("pipo2")
        end
    end
    
end]]

-- http://www.blitzbasic.com/Products/blitzmax.php

-- Je comprends pas... putain, je comprends pas...

print("1")
a = separators + separators --00h06 it's WORKING !!!
print("2")
b = separators.xhas
print(separators:xhas(" ")) -- 00h06 : WORKING !!! marche pas, rien à faire :-(

-- type(separators[c]) ~= "nil"
-- pb de a.key_def avec valeur nil et a.key_undef qui retourne aussi une valeur nil !!!

for i=1, #str do
    c = str:sub(i, i)
    if has(separators, c) then
        if word ~= "" then
            print("Word =", word)
            word = ""
        end
    else
        word = word .. c
    end
    -- print(str:sub(i, i))
end

print("end")

-- 1h44 : on a les bases :-)

print("Hello Lua World")

name = "Bob"
life = 45
print(("My name is %s, I have %d life points."):format(name, life))

print(type("abc"))

--[[
    http://lua-users.org/wiki/CompatibilityWithLuaFive
    http://stackoverflow.com/questions/31452871/table-getn-is-deprecated-how-can-i-get-the-length-of-an-array
    https://www.lua.org/pil/19.1.html
    http://www.moonsharp.org/
    http://luatut.com/crash_course.html
    https://www.lua.org/cgi-bin/demo
    https://www.lua.org/pil/4.2.html
    http://lua-users.org/wiki/StoringNilsInTables
--]]

a = {[1] = 1, [2] = 2}
print(#a) -- 2
a = {[1] = 1, [2] = 2, [10] = 10}
print(#a) -- 2
a = {[1] = 1, [2] = 2, [3] = nil, [10] = 10}
print(#a) -- 2
a = {[1] = 1, [2] = 2, [3] = 3, [10] = 10}
print(#a) -- 3

print("----")
for k,v in pairs(a) do
    print(k, v) -- affiche tout, en partant de 10,10 puis 1,1 2,2, 3,3
end

print("----")
for k,v in ipairs(a) do
    print(k, v) -- affiche 1,1 2,2, 3,3 en ordre mais arrête au 1er nil...
end

--[[

function ID (PARAMETRES)
    CORPS
end

if CONDITION then
    INSTRUCTIONS
else
    INSTRUCTIONS
end

while CONDITION do
    INSTRUCTIONS
end

for VAR = MIN, MAX, STEP do
    INSTRUCTIONS
end

for VAR in EXPRESSION do
    INSTRUCTIONS
end

DECL_VAR
    local VAR = EXPRESSION

TABLE
    VAR = { [LITTERAL] = EXPRESSION, ... }
    VAR = { CLE = EXPRESSION, ... }

LITTERAL
    STRING | NUMBER | nil
    
CLE

BLOCK
    do
        INSTRUCTIONS
    end
    !Pas d'exceptions en Lua

KEYWORD
    return EXPRESSION, EXPR2...
    
OPERATOR
    ~= diff
    # last continuous integer key
    [EXPRESSION] retourne nil si la clé n'est pas défini ou si table[clé] == nil !
    .CLE
    .. concaténation de chaîne
    !Pas d'opérateurs d'affectation combinés X=
    
MAGIC FUNCTIONS
    type(VAR) -> string
    setmetatable(TABLE, METATABLE)
    getmetatable(TABLE)
    print(EXPRESSION, EXPR2...)
]]

--[[
function love.load(arg)
  if arg[#arg] == "-debug" then require("mobdebug").start() end
end
function love.draw()
  love.graphics.setColor(20,255,0,255)
  love.graphics.print("Hello", 100, 100)
end]]
