-------------------------------------------------
-- Dealing with the console
-------------------------------------------------

local write = io.write

print("hello 1")
print("hello 2");
write("hello 3 "); write("world") ; write("\n")
write("hello 4\n")
print("hello 5") print("hello 6")
local a = 5 local b = 22 -- valid !!!
print(a) b = b + 1 -- valid !!!
print(b)

-------------------------------------------------
-- SEQUENCE
-------------------------------------------------

-- ; is not a separator but an optional terminator
-- Grammar : chunk ::= {stat [`;´]}

local c = 5 local d = 6 -- New line doesn't mean anything
print(c + d) -- display 11
local e = { 10, 20, 30, 40, 50}
print(#e) -- display 5
local f = { alpha = 55, beta = 66, zeta = nil, ["zorba"] = "youpi" }
print(#f) -- display 0. The operator # doesn't know how to count tables with non numeric keys.

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

-- no a x= operator with assign
-- no else after while

-------------------------------------------------
-- FOR
-------------------------------------------------

-- i=min, max[, step]
for i=1, 5, 2 do
    print("i=", i)
end
-- no else
-- i is local to the for, must not be modified in the loop
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
        print("hello")
    end
end

local tab = {1, 3, 7, 8, 22}
for index, value in ipairs(tab) do
    print(index, " => ", value)
end
print(#tab) -- display 5

for key, value in pairs(f) do
    print(key, ' => ', value) -- zeta is not treated
end

if f.zeta then
    print("never will be")
else
    print("zeta key value is nil") -- goes here
end

if f.nokey then
    print("never will be")
else
    print("nokey doesn't exist") -- goes here
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
local s = "abc" or 'abc'
print(s)
s = "ab" .. "c" -- concat
print(s)

-- Boolean
local ba = true
local bb = false
print(tostring(ba) .. ' vs ' .. tostring(bb)) -- true vs false
local bc = not bb
print(bc) -- true

-- Numbers
local num1 = 1.0
local num2 = 1
print(num1 == num2) -- true

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
local matrix = {
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
local people_instance_methods = {
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

local people_class_methods = {
    new = function(default_name)
        local i = {}
        setmetatable(i, {__index = people_instance_methods})
        i:init(default_name)
        return i
    end
}

local p1 = people_class_methods.new("Bob")
p1:hello() -- display Hello! I'm Bob
p1:setname("Zorba") -- Hello! I'm Zorba
p1:hello()

-------------------------------------------------
-- OO
-------------------------------------------------

local Class = {}
Class.to_s = "Class"
Class.class = Class
Class.methods = {}
setmetatable(Class, {
    __index = Class.methods
})

local Person = {}
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
    local aa = {}
    aa.name = name
    aa.age = age
    aa.class = Person
    local mt = getmetatable(Person)
    setmetatable(aa, mt)
    Person.count = Person.count + 1
    return aa
end
function Person.to_s()
    return "Person"
end

print(Person.count)
local Bob = Person.new("Bob", 32)
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
local file = io.open("pipo.txt", "w")
if file == nil then
    print("Pb to open in w mode")
else
    file:write("hello pipo!\n")
    file:write("another line to the pipo!\n")
    file:close()
end

file = io.open("pipo.txt", "r")
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
local function create_layer(size, base)
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

local function print_layer(layer)
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
local function create_map(size, base, layer)
    local map = {}
    -- print(type(layer))
    if type(layer) == "number" then
        for i = 1, layer do
            map[i] = create_layer(size, base)
        end
    elseif type(layer) == "table" then
        for _, v in ipairs(layer) do
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
local world1 = create_map(10, 0, 3)
if world1 ~= nil then
    print(world1[3][10][10])
    print_layer(world1[3])
end

local world2 = create_map(10, 22, { "sol", "brou", "unit" })
if world2 ~= nil then
    print(world2.sol[10][10])
    print_layer(world2.sol)
end

-- 15h43 ça marche !

local function get_not_free(layer, x1, y1, x2, y2)
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

local function is_free(layer, x1, y1, x2, y2)
    return #get_not_free(layer, x1, y1, x2, y2) == 0
end

local function print_table(tbl)
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

local layer1 = create_layer(10, 0)
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
for _=1, 10 do
    local r = math.random(20)
    io.write(r, '  ')
end
print()

local function create_room(world, layer, x, y, w, h, content)
    for i = x, x+w do
        for j = y, y+h do
            world[layer][i][j] = content
        end
    end
    return x, y, w, h
end

local function create_random_room(world, layer, max_w, max_h, content)
    local w = math.random(max_w)
    local h = math.random(max_h)
    local x = math.random(world.size - w - 1)
    local y = math.random(world.size - h - 1)
    create_room(world, layer, x, y, w, h, content)
end

local world3 = create_map(30, 0, { "sol", "brou", "unit" })
if world3 ~= nil then
    for _=1, 3 do
        create_random_room(world3, "sol", 5, 5, '_')
    end
    print_layer(world3.sol)
end

-- 15h23

-------------------------------------------------
-- Brouillard calc (~04/01/2017)
-------------------------------------------------

local x = 5
local y = 7
local function localize()
    print("x=", x) -- 5
    print("y=", y) -- 7 recognize
end
localize()

local function brou(x, y, vision)
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
local vision = 3
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
