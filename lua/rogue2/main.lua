-- 21.1 – The Simple I/O Model
-- https://www.lua.org/pil/21.1.html

function main()
    -- s = io.read("*number")
    s = tonumber(io.stdin:read())
    s = s + 1
    print(s)
end

-- 8.4 Error Handling and Exceptions
-- https://www.lua.org/pil/8.4.html
-- pcall = protected call

--a, b = pcall(main) -- si on met pas b, il ne peuple que a !!!
print(type(a)) -- boolean
print(a)       -- false
print(type(b)) -- string
print(b)       -- filepath:line: attempt to perform arithmetic on a nil value (global 's')

do
    local i = 5
end

-- 4.2 Local Variables and Blocks
-- https://www.lua.org/pil/4.2.html

print(type(i))
print(i)
if i == nil then
    print("i is nil")
end

-- Assert

a = 5
assert(a == 5, "A is not 5")

-- Create a map

--io.write("Width?\n")
--io.flush()
--width = tonumber(io.stdin:read()) -- "*number")

--io.write("Height?\n")
--io.flush()
--height = tonumber(io.stdin:read()) --"*number")

MAX_CONNECTIVITY = 1

STRATEGY = MAX_CONNECTIVITY

MATRIX_SIZE = 6 --20

width = MATRIX_SIZE
height = MATRIX_SIZE

HAUT = 8
BAS = 4
GAUCHE = 2
DROITE = 1

layer = {}
for j=1, width do
    layer[j] = {}
    for i=1, height do
        r = 0
        if i == 1 then -- can't go to left but to right it's OK
            r = r + DROITE
        elseif i == width then
            r = r + GAUCHE
        else
            r = r + DROITE + GAUCHE
        end
        if j == 1 then -- can't go up but can go down
            r = r + BAS
        elseif j == height then
            r = r + HAUT
        else
            r = r + BAS + HAUT
        end
        layer[j][i] = r
    end
end
layer.width = width
layer.height = height

function print_matrix(matrix)
    for i=1, matrix.width do
        for j=1, matrix.height do
            io.stdout:write(tostring(layer[i][j]) .. ' ')
        end
        print()
    end
end

print("-------------------------------------------------")
print_matrix(layer)
print("-------------------------------------------------")

-- 16h28 ça encode bien !!!

-- Haut Bas Gauche  Droit                       overture     template ok
--  8   4   2       1
--  0   0   0       d       = 1        d            1  => ok = 1,
--  0   0   g       0       = 2      g              1  => ok =    2,
--  0   0   g       d       = 3      g d            2  => ok = 1, 2, 3,
--  0   b   0       0       = 4    b                1  => ok =          4,
--  0   b   0       d       = 5    b   d            2  => ok = 1,       4, 5, 
--  0   b   g       0       = 6    b g              2  => ok =    2,    4,    6,
--  0   b   g       d       = 7    b g d            3  => ok = 1, 2, 3, 4, 5, 6, 7,
--  h   0   0       0       = 8  h                  1  => ok =                      8,
--  h   0   0       d       = 9  h     d            2  => ok = 1                    8, 9, 
--  h   0   g       0       = 10 h   g              2  => ok = 2                    8,    10,
--  h   0   g       d       = 11 h   g d            3  => ok = 1, 2, 3,             8, 9, 10, 11
--  h   b   0       0       = 12 h b                2  => ok =          4           8             12
--  h   b   0       d       = 13 h b   d            3  => ok = 1,       4, 5,       8, 9,         12, 13
--  h   b   g       0       = 14 h b g              3  => ok =    2,    4,    6,    8,    10,     12,     14
--  h   b   g       d       = 15 h b g d            4  => ok = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

templates = {
    template01 = {
        content = {
            "### ###",
            "#     #",
            "# # # #",
            "       ",
            "# # # #",
            "#     #",
            "### ###",
        },
        value = 15, -- h b g d
        id = 1,
    },
    template02 = {
        content = {
            "#######",
            "#      ",
            "#      ",
            "#      ",
            "#      ",
            "#      ",
            "#######",
        },
        value = 1,
        id = 2,
    },
    template03 = {
        content = {
            "#######",
            "      #",
            "      #",
            "      #",
            "      #",
            "      #",
            "#######",
        },
        value = 2,
        id = 3,
    },
    template04 = {
        content = {
            "#     #",
            "#     #",
            "#     #",
            "#     #",
            "#     #",
            "#     #",
            "#######",
        },
        value = 8,
        id = 4,
    },
    template05 = {
        content = {
            "#######",
            "#     #",
            "#     #",
            "#     #",
            "#     #",
            "#     #",
            "#     #",
        },
        value = 4,
        id = 5,
    },
    template06 = {
        content = {
            "#######",
            "#      ",
            "#      ",
            "#      ",
            "#      ",
            "#      ",
            "#      ",
        },
        value = 5,
        id = 6,
    },
}

-- Randomly assign template to map coordinate

-- If the square of the map has X it can be ok for template of value {V1, V2, ...}

magic_table = {
    {1},                        --  1
    {2},                        --  2
    {1, 2, 3},                  --  3
    {4},                        --  4
    {1, 4, 5},                  --  5
    {2, 4, 6},                  --  6
    {1, 2, 3, 4, 5, 6, 7},      --  7
    {8},                        --  8
    {1, 8, 9},                  --  9
    {2, 8, 10},                 -- 10
    {1, 2, 3, 8, 9, 10, 11},    -- 11
    {4, 8, 12},                 -- 12
    {1, 4, 5, 8, 9, 12, 13},    -- 13
    {2, 4, 6, 8, 10, 12, 14},   -- 14
    {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}, -- 15
}

-- For value X in magic_table2 there is v1 overtures

magic_table2 = {
    1,  --  1
    1,  --  2
    2,  --  3
    1,  --  4
    2,  --  5
    2,  --  6
    3,  --  7
    1,  --  8
    2,  --  9
    2,  -- 10
    3,  -- 11
    2,  -- 12
    3,  -- 13
    3,  -- 14
    4,  -- 15
}

print("Info before")
print(type(table))
print(table)

function has(atable, val)
    for index, value in ipairs(atable) do
        if value == val then
            return true
        end
    end
    return false
end

print("Info after")
print(type(table))
print(table) -- table est écrasée !!! Purée !!!

function zorba(zorbi)
    zorbi = "youpi"
end

print(type(zorbi)) -- ok là c'est bien supprimé
print(zorbi) -- donc c'est le fait de mettre en param table... ok !!!


function count(atable)
    local cpt = 0
    for key, value in pairs(atable) do
        cpt = cpt + 1
    end
    return cpt
end

function display(atable)
    local cpt = 1
    local max = count(atable)
    for key, value in pairs(atable) do
        io.stdout:write(key .. ' = ' .. tostring(value))
        if cpt < max then
            io.stdout:write(', ')
        end
        cpt = cpt + 1
    end
    io.stdout:write("\n")
    io.stdout:flush()
end

function get_tmp(x, templates)
    --print("Looking for x = " .. tostring(x))
    -- get all templates ok
    local are_ok = magic_table[x]
    --display(are_ok)
    
    local ok_found = {}
    for tkey, tval in pairs(templates) do
        --print("  Testing templates id =" .. templates[tkey].id .. " with value = " .. templates[tkey].value)
        if has(are_ok, tval.value) then
            --print("  is ok")
            ok_found[tkey] = tval
        else
            --print("  is not ok")
        end
    end
    print("I found " .. count(ok_found) .. " compatible templates :")
    display(ok_found)
    
    -- select the most open ended
    local max = 0
    local max_key = nil
    for tkey, tval in pairs(ok_found) do
        if magic_table2[tval.value] > max then
            max = magic_table2[tval.value]
            max_key = tkey
        end
    end
    assert(max_key ~= nil, "No template found!")
    print("The best with " .. max .. " overtures is " .. max_key)
    return max_key
end

function assign_tmp(matrix)
    for i=1, matrix.width do
        for j=1, matrix.height do
            tmp = get_tmp(matrix[j][i], templates)
            matrix[j][i] = templates[tmp].id
        end
    end
end

--assign_tmp(layer)
print_matrix(layer)

-------------------------------------------------------------------------------
-- New strategy
-------------------------------------------------------------------------------

math.randomseed(os.time())

-- Diminish : 4 -> 3, 3 -> 2, 2 -> 1, 1 -> 1
-- En gros, il suffit de combiner magic_table (qui donne pour hbg => h, b, g) et magic_table2 qui donne pour hgb = 3
-- Il faut supprimer 7 -> 7 et 7 -> 1, 2, 4 qui sont des trucs à 1 possibilité (car on a d'autres !!!)
diminish_one = {
    {1},                        --  1
    {2},                        --  2
    {1, 2},                     --  3
    {4},                        --  4
    {1, 4},                     --  5
    {2, 4},                     --  6
    {3, 5, 6},                  --  7
    {8},                        --  8
    {1, 8},                     --  9
    {2, 8},                     -- 10
    {3, 9, 10},                 -- 11
    {4, 8},                     -- 12
    {5, 9, 12},                 -- 13
    {6, 10, 12},                -- 14
    {3, 5, 6, 7, 9, 10, 11, 12, 13, 14}, -- 15
}

-- !!! NEVER USE TABLE AS A PARAM OR VARIABLE NAME WITHOUT LOCAL BEFORE !!!
function diminish_openess(matrix)
    for i=1, matrix.width do
        for j=1, matrix.height do
            --table = magic_table[matrix[j][i]] -- all possibilities. For example : 5(bd) is 1 (d), 4 (b), 5 (bd)
            --matrix[j][i] = table[math.random(1, #table)]
            local table = diminish_one[matrix[j][i]]
            matrix[j][i] = table[math.random(1, #table)]
        end
    end
end

diminish_openess(layer)

-------------------------------------------------------------------------------
-- Worm tactics
-------------------------------------------------------------------------------

function worm()
    local x = math.random(1, MATRIX_SIZE)
    local y = 1
    local stay_on_line = 0
    local line_direction = nil
    local RIGHT = 1
    local LEFT = -1
    local path = {}
    local step = 1
    while y <= MATRIX_SIZE do
        path[step] = {x, y}
        if stay_on_line == 0 then
            if x < MATRIX_SIZE / 2 then
                line_direction = RIGHT
            else
                line_direction = LEFT
            end
        end
        dice = math.random(stay_on_line, MATRIX_SIZE)
        if dice > MATRIX_SIZE / 2  or (x == 1 and stay_on_line > 0) or (x == MATRIX_SIZE and stay_on_line > 0) then
            y = y + 1
            stay_on_line = 0
        else
            x = x + line_direction
            stay_on_line = stay_on_line + 1
        end
        step = step + 1
    end

    for step, pos in ipairs(path) do
        print(step .. '. ' .. pos[1] .. ', ' .. pos[2])
    end
    return path
end

worm_hole = worm()

function in_path(x, y, path)
    for step, pos in ipairs(path) do
        if pos[1] == x and pos[2] == y then
            return true
        end
    end
    return false
end
    
-------------------------------------------------------------------------------
-- New with pic
-------------------------------------------------------------------------------

textures = {}
textures_green = {}

function load_textures()
    textures = {                            -- val ind
        love.graphics.newImage('____.png'), --  0   1
        love.graphics.newImage('___d.png'), --  1   2
        love.graphics.newImage('__g_.png'), --  2   3
        love.graphics.newImage('__gd.png'), --  3   4
        love.graphics.newImage('_b__.png'), --  4   5
        love.graphics.newImage('_b_d.png'), --  5   6
        love.graphics.newImage('_bg_.png'), --  6   7
        love.graphics.newImage('_bgd.png'), --  7   8
        love.graphics.newImage('h___.png'), --  8   9
        love.graphics.newImage('h__d.png'), --  9  10
        love.graphics.newImage('h_g_.png'), -- 10  11
        love.graphics.newImage('h_gd.png'), -- 11  12
        love.graphics.newImage('hb__.png'), -- 12  13
        love.graphics.newImage('hb_d.png'), -- 13  14
        love.graphics.newImage('hbg_.png'), -- 14  15
        love.graphics.newImage('hbgd.png'), -- 15  16
    }

    textures_green = {
        love.graphics.newImage('green/____.png'), --  0   1
        love.graphics.newImage('green/___d.png'), --  1   2
        love.graphics.newImage('green/__g_.png'), --  2   3
        love.graphics.newImage('green/__gd.png'), --  3   4
        love.graphics.newImage('green/_b__.png'), --  4   5
        love.graphics.newImage('green/_b_d.png'), --  5   6
        love.graphics.newImage('green/_bg_.png'), --  6   7
        love.graphics.newImage('green/_bgd.png'), --  7   8
        love.graphics.newImage('green/h___.png'), --  8   9
        love.graphics.newImage('green/h__d.png'), --  9  10
        love.graphics.newImage('green/h_g_.png'), -- 10  11
        love.graphics.newImage('green/h_gd.png'), -- 11  12
        love.graphics.newImage('green/hb__.png'), -- 12  13
        love.graphics.newImage('green/hb_d.png'), -- 13  14
        love.graphics.newImage('green/hbg_.png'), -- 14  15
        love.graphics.newImage('green/hbgd.png'), -- 15  16
    }
end

if love ~= nil then
    function love.load()
        load_textures()
        print("hello love")
        canvas = love.graphics.newCanvas(MATRIX_SIZE * 32, MATRIX_SIZE * 32)
        -- draw to a canvas
        love.graphics.setCanvas(canvas)
        for i=1, layer.width do
            for j=1, layer.height do
                print("Printing for " .. i .. ", " .. j)
                if in_path(j, i, worm_hole) then
                    love.graphics.draw(textures_green[layer[i][j]+1], (j-1)*32, (i-1)*32)
                else
                    love.graphics.draw(textures[layer[i][j]+1], (j-1)*32, (i-1)*32)
                end
            end
        end
        -- redraw to the screen
        love.graphics.setCanvas()
        love.filesystem.setIdentity("MyDir")
        data = canvas:newImageData( )
        --TO WRITE
        --data:encode('png', os.time() .. '.png')
    end
end

print("------------------------------------- END ----------------------------------")

-- 17h42 stop

-------------------------------------------------------------------------------
-- Utility library
-------------------------------------------------------------------------------

print('Start Utility Library')

-- Read a file (given its filepath) and return a string containing all its content.
-- @param filepath : string
-- @return : string
function read(filepath)
    local file = io.open(filepath)
    local cpt = 1
    local content = ''
    for line in file:lines() do
        -- print(cpt .. '. ' .. line)
        cpt = cpt + 1
        content = content .. line .. '\n'
    end
    return content
end

-- Read a file (given its filepath) and return a table containing all its content.
-- @param filepath : string
-- @return : table of string (without the \n)
function readlines(filepath)
    local file = io.open(filepath)
    local cpt = 1
    local content = {}
    for line in file:lines() do
        -- print(cpt .. '. ' .. line)
        cpt = cpt + 1
        table.insert(content, line)
    end
    return content
end

function write(content)
    io.stdout:write(content)
    io.flush()
end

function writeln(content)
    print(content)
end

-- Pour faire une sous chaîne [ ] ne marche pas !!! string.sub
-- 16h56 : split pseudo marche yeah ! 17h05 : split marche vraiment :-)
function split(content, separator)
    --print("Split")
    local cpt_ok = 1
    local blocks = {}
    local word = ''
    for index=1, #content do
        char = string.sub(content, index, index)
    --  print(index .. ". " .. char .. ' and separator[cpt_ok] is = ' .. string.sub(separator, cpt_ok, cpt_ok) .. ' cpt_ok = ' .. cpt_ok)
    --for index, char in ipairs(content) do
        if char == string.sub(separator, cpt_ok, cpt_ok) then
            cpt_ok = cpt_ok + 1
            --print("Youpi ! cpt_ok = " .. cpt_ok .. " lenght = " .. #separator)
        else
            cpt_ok = 1
        end
        if char ~= ' ' then
            word = word .. char
        else
            word = word .. '#'
        end
        --print("word = " .. word)
        if cpt_ok > #separator then
            cpt_ok = 1
            table.insert(blocks, string.sub(word, 1, #word-3))
            word = ''
        end
    end
    return blocks
end

function display_tab(tab)
    for index, value in ipairs(tab) do
        print(index .. '. ' .. value)
    end
end

TARGET = "pipo.txt" -- "D:\\pipo.txt"

print("1. Test 1 : lire tout le fichier")
content = read(TARGET)
write(content)

print("2. Test 2 : lire le fichier par ligne")
content = readlines(TARGET)
display_tab(content)

print("3. Test 3 : split")
content = "zorba   zorbi   cooli   extramdure    ext4"
blocks = split(content, "   ")
display_tab(blocks)

CString = {
    new = function(s)
        i = { content = s, class = CString}
        setmetatable(i, { __index = CString.instance_methods, __add = CString.instance_methods.add})
        return i
    end,
    instance_methods = {
        add = function(self, s)
            --print("s is : " .. tostring(s) .. " type = " .. type(s))
            return CString.new(self.content .. s.content)
        end,
        writeln = function(self)
            print(self.content)
        end,
    },
    name = "CString",
}

local h = CString.new("hello")
h:writeln()
print(h.class.name)

local w = CString.new(" world!")
w:writeln()
print(w.class.name)

local z = (h + w)
z:writeln() -- 17h16 ça marche !

print(type((h+w)))

--(h:add(w)):writeln()
--(h+w):writeln()

-- 17h10 ça marche CString !!!
 
--(2+2) marche pas
--2+2 marche pas

player = {}
player.x = 5
player.y = 5
player.x32 = 0
player.y32 = 0
player.rate = 100

if love ~= nil then
    -- https://love2d.org/wiki/love.update
    function love.update(dt)
        --print(dt)
        speed = (dt * player.rate)
        if love.keyboard.isDown("up") then
            player.y = player.y - speed
        end
        if love.keyboard.isDown("down") then
            player.y = player.y + speed
        end
        if love.keyboard.isDown("left") then
            player.x = player.x - speed
        end
        if love.keyboard.isDown("right") then
            player.x = player.x + speed
        end
        if love.keyboard.isDown("space") then
            local buttons = {"Yeah!", "Up!", enterbutton = 1, escapebutton = 2} -- bug detected
            local res = love.window.showMessageBox("Hello", "You have pressed space. Are you happy?", buttons, "info", true)
            print(res)
            if res == 1 then
                print("Yeah!")
            else
                print("Up!")
            end
        end
        player.x32 = math.floor(player.x / 32)
        player.y32 = math.floor(player.y / 32)
    end
end

if love ~= nil then
    function love.draw()
        local cam = {}
        cam.width = 25
        cam.height = 18
        for lin=0, cam.height-1 do
            for col=0, cam.width-1 do
                if col == player.x32 and lin == player.y32 then
                    love.graphics.draw(textures_green[1], col*32, lin*32)
                else
                    love.graphics.draw(textures[1], col*32, lin*32)
                end
            end -- for
        end  -- for
        love.graphics.setColor(0, 255, 0)
        love.graphics.circle("fill", player.x, player.y, 5)
        love.graphics.setColor(255, 255, 255)
    end -- fun
end

print('End')
