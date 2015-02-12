map = {
  { 1, 0, 0, 0, 0, 0},
  { 1, 0, 0, 0, 0, 0},
  { 1, 0, 0, 0, 0, 0},
  { 1, 0, 0, 0, 0, 0},
  { 1, 0, 0, 0, 0, 0},
}

function love.load(arg)
    if arg[#arg] == "-debug" then require("mobdebug").start() end
    print("Hello")
    print(type(map))
    print(#map)
end

-- Mettre local pour une variable locale ! Global scope by default!
-- Les index en Lua commencent à 1 !!!
-- Pas de paramètres réels/effectifs par défaut : il faut faire un x = x or val
-- => http://www.lua.org/pil/5.html
-- Pas de vérification du nombre de paramètre au lancement
-- L'opérateur ipairs permet d'avoir un index et une value sur une table pour un for
function rect(color, x, y, w, h, border, border_color)
    border = border or false
    border_color = border_color or nil
    love.graphics.setColor(unpack(color))
    love.graphics.rectangle("fill", x, y, w, h)
    if border then
        love.graphics.setColor(unpack(border_color))
        love.graphics.rectangle("line", x, y, w, h)
    end
end

function circle(color, x, y, r)
    love.graphics.setColor(unpack(color))
    love.graphics.circle("fill", x, y, r, 100)
end

mousepressed = false
mx = nil
my = nil

function love.mousepressed(x, y, button)
    if button == "l" then
        mx = x
        my = y
    end
end

function love.mousereleased(x, y, button)
    if button == "l" then
        print("Mouse was pressed at ", mx, ":", my, "and released at ", x, ":", y)
    end
end

function love.draw()
    local a = 5
    for nbline, line in ipairs(map) do
        for nbcol, col in ipairs(line) do
            --print(nbline, nbcol)
            if col == 0 then
                c = { 0, 0, 0, 255 }
            elseif col == 1 then
                c = { 0, 255, 0, 255 }
            end
            if love.mouse.isDown("l") then
                x, y = love.mouse.getPosition()
                x = math.floor(x / 32)
                y = math.floor(y / 32)
                print(x, y, nbcol-1, nbline-1)
                if x == nbcol-1 and y == nbline-1 then
                    c = { 0, 255, 255, 255 }
                end
            end
            rect(c, (nbcol-1)*32, (nbline-1)*32, 32, 32, true, {255, 0, 0, 255})
        end
    end
    circle({0, 255, 0, 255}, 300, 300, 6)
    love.graphics.setColor(20,255,0,255)
    love.graphics.print("Hello", 100, 100)
end
