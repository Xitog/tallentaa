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
            io.stdout:write(tostring(matrix[i][j]) .. ' ')
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

-- !!! NEVER USE THE 'SPECIAL WORD' TABLE AS A PARAM OR VARIABLE NAME WITHOUT LOCAL BEFORE !!!
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
    --print(os.execute("cd"))
    --print(love.filesystem.getWorkingDirectory())
    --local s = "C:\\Users\\damie_000\\Documents\\GitHub\\tallentaa\\assets\\tiles32x32\\basic\\dungeon_white\\"
    textures = {                            -- val ind
        love.graphics.newImage('basic/dungeon_white/____.png'), --  0   1
        love.graphics.newImage('basic/dungeon_white/___d.png'), --  1   2
        love.graphics.newImage('basic/dungeon_white/__g_.png'), --  2   3
        love.graphics.newImage('basic/dungeon_white/__gd.png'), --  3   4
        love.graphics.newImage('basic/dungeon_white/_b__.png'), --  4   5
        love.graphics.newImage('basic/dungeon_white/_b_d.png'), --  5   6
        love.graphics.newImage('basic/dungeon_white/_bg_.png'), --  6   7
        love.graphics.newImage('basic/dungeon_white/_bgd.png'), --  7   8
        love.graphics.newImage('basic/dungeon_white/h___.png'), --  8   9
        love.graphics.newImage('basic/dungeon_white/h__d.png'), --  9  10
        love.graphics.newImage('basic/dungeon_white/h_g_.png'), -- 10  11
        love.graphics.newImage('basic/dungeon_white/h_gd.png'), -- 11  12
        love.graphics.newImage('basic/dungeon_white/hb__.png'), -- 12  13
        love.graphics.newImage('basic/dungeon_white/hb_d.png'), -- 13  14
        love.graphics.newImage('basic/dungeon_white/hbg_.png'), -- 14  15
        love.graphics.newImage('basic/dungeon_white/hbgd.png'), -- 15  16
    }

    textures_green = {
        love.graphics.newImage('basic/dungeon_green/____.png'), --  0   1
        love.graphics.newImage('basic/dungeon_green/___d.png'), --  1   2
        love.graphics.newImage('basic/dungeon_green/__g_.png'), --  2   3
        love.graphics.newImage('basic/dungeon_green/__gd.png'), --  3   4
        love.graphics.newImage('basic/dungeon_green/_b__.png'), --  4   5
        love.graphics.newImage('basic/dungeon_green/_b_d.png'), --  5   6
        love.graphics.newImage('basic/dungeon_green/_bg_.png'), --  6   7
        love.graphics.newImage('basic/dungeon_green/_bgd.png'), --  7   8
        love.graphics.newImage('basic/dungeon_green/h___.png'), --  8   9
        love.graphics.newImage('basic/dungeon_green/h__d.png'), --  9  10
        love.graphics.newImage('basic/dungeon_green/h_g_.png'), -- 10  11
        love.graphics.newImage('basic/dungeon_green/h_gd.png'), -- 11  12
        love.graphics.newImage('basic/dungeon_green/hb__.png'), -- 12  13
        love.graphics.newImage('basic/dungeon_green/hb_d.png'), -- 13  14
        love.graphics.newImage('basic/dungeon_green/hbg_.png'), -- 14  15
        love.graphics.newImage('basic/dungeon_green/hbgd.png'), -- 15  16
    }
    
    textures_colored = {
        love.graphics.newImage('basic/textures/blue.png'),  -- 1
        love.graphics.newImage('basic/textures/brown.png'), -- 2
        love.graphics.newImage('basic/textures/green.png'), -- 3
        love.graphics.newImage('basic/textures/grey.png'),  -- 4
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
        -- EUH ??? data = canvas:newImageData( )
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

TARGET = "./pipo.txt" -- "D:\\pipo.txt"

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
 
 print('Tests')
--(2+2) marche pas
--2+2 marche pas
--=2+2 mache pas

require "common" 
game = {}
game.map = create_map()
populate(game.map)

camera = {}
game.players = {}
units = {}

require "rts"

Xitog = create_player(game, "Xitog", "Yellow")
Zorba = create_player(game, "Zorba", "Green")

camera.player = Xitog -- game.players[1]

units[#units+1] = create_unit(Xitog, 16, 16, 10, 2)
units[#units+1] = create_unit(Xitog, 50, 50, 20, 2)
units[#units+1] = create_unit(Xitog, 180, 180, 20, 2)
units[#units+1] = create_unit(Zorba, 300, 200, 15, 6)
units[#units+1] = create_unit(Zorba, 400, 400, 22, 2)

-- print("Are you defined, u?", u) do / end for local

-- Choix :
-- soit on abandonne le x et le y
-- On dit qu'il s'agit d'une valeur dérivée de x32 et y32.
-- Pb c'est que non !!! Lorsqu'il est en transition, c'est ça qu'il faut regarder !!!

function select_simple(x, y)
    x32 = math.floor(x/32) + 1
    y32 = math.floor(y/32) + 1
    for i, u in ipairs(units) do
        if x32 == u.x32 and y32 == u.y32 then
            return u
        end
    end
    return nil
end

function get_closer_of_target_old(player)
    --print('Moving', player.in_transition, "p32 = " .. player.x32, player.y32, "p = " .. player.x, player.y, "next = " .. player.next.x32, player.next.y32, "target = " .. player.target.x32, player.target.y32)
    if player.x ~= player.target.x or player.y ~= player.target.y then
        -- Next goal reached
        if player.in_transition then
            if player.next.x == player.x and player.next.y == player.y then
                player.in_transition = false
                print('Next Reached!')
            end
        end
        -- Choosing next goal
        if not player.in_transition then
            player.next.step.x32 = 0
            -- Next step
            if player.x32 > player.target.x32 then
                player.next.step.x32 = -1
            elseif player.x32 < player.target.x32 then
                player.next.step.x32 = 1
            end
            player.next.step.y32 = 0
            if player.y32 > player.target.y32 then
                player.next.step.y32 = -1
            elseif player.y32 < player.target.y32 then
                player.next.step.y32 = 1
            end
            player.next.x32 = player.x32 + player.next.step.x32
            player.next.y32 = player.y32 + player.next.step.y32
            player.next.x = player.next.x32 * 32 + 16
            player.next.y = player.next.y32 * 32 + 16
            player.in_transition = true
        end
        -- Going to next goal
        if player.in_transition then
            if player.x < player.next.x and player.x + player.next.step.x32 * player.move > player.next.x then
                player.x = player.next.x
            else
                player.x = player.x + player.next.step.x32 * player.move
            end
            if player.y < player.next.y and player.y + player.next.step.y32 * player.move > player.next.y then
                player.y = player.next.y
            else
                player.y = player.y + player.next.step.y32 * player.move
            end
            player.x32 = math.floor(player.x / 32) + 1
            player.y32 = math.floor(player.y / 32) + 1
        end
    else
        if player.in_transition then
            player.in_transition = false
            print('Target Reached')
        end
    end
end

--print('La carte : ')
--print_matrix(game.map)

if love ~= nil then
    -- https://love2d.org/wiki/love.update
    function love.update(dt)
        --print(dt)
        for i, u in ipairs(units) do
            update(u)
        end
        --speed = (dt * player.rate)
        --if love.keyboard.isDown("up") then
        --    player.y = player.y - speed
        --end
        --if love.keyboard.isDown("down") then
        --    player.y = player.y + speed
        --end
        --if love.keyboard.isDown("left") then
        --    player.x = player.x - speed
        --end
        --if love.keyboard.isDown("right") then
        --    player.x = player.x + speed
        --end
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
    end

    function love.mousereleased( x, y, button, istouch )
        if button == 1 or button == "l" then -- sur mon windows 8.1, c'est une chaîne l pour left !!! Sur un autre PC, c'est l'integer 1 !!! Fou...
            u = select_simple(x, y)
            if u ~= nil then
                camera.player.selected = {}
                camera.player.selected[#camera.player.selected+1] = u
            end
        elseif button == 2 or button == "r" then
            for i, u in ipairs(camera.player.selected) do
                --print('go!', u)
                set_target(u, x, y)
            end
        else
            print(button)
            print(button == "l")
            print(type(button))
            os.exit(1)
        end
    end
    
    function love.draw()
        local cam = {}
        cam.width = 25
        cam.height = 18
        --for lin=0, cam.height-1 do
        --    for col=0, cam.width-1 do
        for lin=1, cam.height do
            for col=1, cam.width do
                --if (col == player.x32 and lin == player.y32) or (col == player.next.x32 and lin == player.next.y32) then
                --    love.graphics.draw(textures_green[1], (col-1)*32, (lin-1)*32)
                --else
                    local r = game.map.ground[lin][col]
                    love.graphics.draw(textures_colored[r], (col-1)*32, (lin-1)*32)
                    local u = game.map.unit[lin][col]
                    if u ~= 0 then
                        love.graphics.setColor(255, 0, 0)
                        love.graphics.circle("fill", (col-1)*32+16, (lin-1)*32+16, 3)
                        love.graphics.setColor(255, 255, 255)
                    end
                --end
            end -- for
        end  -- for
        for i, u in ipairs(units) do
            love.graphics.draw(textures[1], (u.x32-1)*32, (u.y32-1)*32)
            if has(camera.player.selected, u) then
                love.graphics.setColor(255, 255, 0)
                love.graphics.circle("fill", u.x, u.y, u.size + 3)
            end
            love.graphics.setColor(0, 255, 0)
            love.graphics.circle("fill", u.x, u.y, u.size)
            love.graphics.setColor(255, 255, 255)
        end -- for
    end -- fun
end

print('End')

print('Test')

print('ipairs')
a = {1, 2, 3, 4, ["a"] = 6, 7, 8, 9}
for i, v in ipairs(a) do
    print(i, v) -- affiche 1 1, 2 2, 3 3, 4 4, 5 7, 6 8, 7 9 (et donc pas a 6)
end
print('pairs')
for i, v in pairs(a) do
    print(i, v) -- affiche 1 1, 2 2, 3 3, 4 4, 5 7, 6 8, 7 9, a 6
end

