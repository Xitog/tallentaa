-- https://love2d.org/
-- 18/04 11h15 : collision OK

-- local f = io.open("data.txt", "rb")
local f = love.filesystem.newFile("data.txt")
if f == nil then
    print("Impossible to open data.txt")
else
    f:open("r")
    local content, size = f:read(1)
    local MAX = 100
    print(type(content) .. " : |" .. content .. "|")
    print(type(size), size)
    while content ~= nil and content ~= "" and MAX > 0 do
        local n = string.byte(content)
        if n ~= nil and n >= 0 and n < 255 then
            if n < 128 then
                if content == '\r' then content = '\\r' end
                if content == '\n' then content = '\\n' end
                print("|" .. content .. "| (" .. string.format("%02x", n) .. ") #" .. size)
            elseif n < 224 then
                f:read(1)
            elseif n < 240 then
                f:read(2)
            else
                f:read(3) -- 4 byte wide chars
            end
        end
        content, size = f:read(1)
        MAX = MAX - 1
    end
    f:close()
end

os.exit()

local player_x = 2
local player_y = 2
local player_a = 90 * 0.01745 -- conversion en radian
local dir_x = math.cos(player_a)
local dir_y = math.sin(player_a)
local rot_speed = 0.01
local move_speed = 0.01
local ZOOM = 32
local armed = false

local function storeAsFloat(rgb)
    local r, g, b, a = love.math.colorFromBytes(rgb)
    return {r, g, b, a}
end

local RED = storeAsFloat({255, 0, 0})
local PURPLE = storeAsFloat({160, 32, 240})
local YELLOW =  storeAsFloat({255, 255, 0})
local GREEN = storeAsFloat({0, 255, 0})

local BLACK = storeAsFloat({0, 0, 0})
local GREY = storeAsFloat({128, 128, 128})
local WHITE = storeAsFloat({255, 255, 255})

local COLORS = {RED, PURPLE, YELLOW, GREEN}

local map = {
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 1},
        {1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 1},
        {1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1},
        {1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
}

function love.load()
    love.window.setTitle("FPS")
    love.window.setMode(640, 480, {resizable=false, vsync=0})
    love.graphics.setLineWidth(1)
end

function love.update(dt)
    --print(dt)
    local moved = false
    local next_x = player_x
    local next_y = player_y
    if love.keyboard.isDown("up") then
        next_x = math.min(player_x + dir_x * move_speed, 639)
        next_y = math.min(player_y + dir_y * move_speed, 479)
        moved = true
    end
    if love.keyboard.isDown("down") then
        next_x = math.max(player_x - dir_x * move_speed, 0)
        next_y = math.max(player_y - dir_y * move_speed, 0)
        moved = true
    end
    if love.keyboard.isDown("right") then
        player_a = player_a + rot_speed
        dir_x = math.cos(player_a);
        dir_y = math.sin(player_a);
    end
    if love.keyboard.isDown("left") then
        player_a = player_a - rot_speed
        dir_x = math.cos(player_a);
        dir_y = math.sin(player_a);
    end
    if moved then
        local map_x = math.floor(player_x) + 1
        local map_y = math.floor(player_y) + 1
        local map_next_x = math.floor(next_x) + 1
        local map_next_y = math.floor(next_y) + 1
        if map[map_next_y][map_next_x] == 0 then
            player_x = next_x
            player_y = next_y
        elseif map[map_y][map_next_x] == 0 then
            player_x = next_x
        elseif map[map_next_y][map_x] == 0 then
            player_y = next_y
        end
    end
    if love.keyboard.isDown("space") then
        armed = true
    elseif armed then
        print("armed")
        armed = false
    end
end

function love.draw()
    love.graphics.setColor(WHITE)
    love.graphics.rectangle("fill", 0, 0, 640, 480)
    love.graphics.setColor(GREY)
    for col = 1, 20 do
        local scol = col - 1
        for row = 1, 15 do
            local srow = row - 1
            local c = map[row][col]
            love.graphics.setColor(GREY)
            love.graphics.rectangle("line", scol * ZOOM, srow * ZOOM, ZOOM, ZOOM)
            if c > 0 then
                love.graphics.setColor(COLORS[c])
                love.graphics.rectangle("fill", scol * ZOOM, srow * ZOOM, ZOOM, ZOOM)
            else
                love.graphics.setColor(WHITE)
                love.graphics.rectangle("fill", scol * ZOOM, srow * ZOOM, ZOOM, ZOOM)
            end
        end
    end
    love.graphics.setColor(BLACK)
    love.graphics.line(player_x * ZOOM, player_y * ZOOM, player_x * ZOOM + dir_x * ZOOM * 1.05, player_y * ZOOM + dir_y * ZOOM * 1.05)
    love.graphics.circle("fill", player_x * ZOOM, player_y * ZOOM, 5)
    love.graphics.setColor(GREEN)
    love.graphics.print("Hello World!", 400, 300)
    love.graphics.print(player_x, 400, 312)
    love.graphics.print(player_y, 400, 324)
    love.graphics.print(player_a, 400, 336)
    love.graphics.print(dir_x, 400, 348)
    love.graphics.print(dir_y, 400, 360)
end
