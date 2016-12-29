-- Docs :
-- https://www.lua.org/manual/5.3/
-- https://love2d.org/wiki/Main_Page
-- 12h52 ça marche. ZeroBrane configuré (tabs, love en relatif)
-- 13h17 yeahhhh ! Translate OK
-- 15h27 rotation centrée OK (il faut faire un translate avant et après car rotate only sur origine)

-- https://love2d.org/wiki/love.graphics.rotate
-- https://love2d.org/wiki/love.graphics.newScreenshot

cam_x = 0
cam_y = 0
cam_a = 0

width, height, flags = love.window.getMode( )
print("Res :", width, height)
print(love.graphics.getLineStyle())
print(love.graphics.getLineWidth())

player_x = width / 2
player_y = height / 2

function love.load(arg)
    if arg[#arg] == "-debug" then require("mobdebug").start() end
    love.window.setTitle("Test")
end

walls = {
    { x1 = 100, y1 = 100, x2 = 150, y2 = 100 },
    { x1 = 100, y1 = 100, x2 = 100, y2 = 150 },
    { x1 = 100, y1 = 150, x2 = 150, y2 = 150 },
    { x1 = 150, y1 = 100, x2 = 150, y2 = 150 },
    { x1 = 10, y1 = 10, x2 = 600, y2 = 10 },
}

function love.draw()
    love.graphics.setColor(20,255,0,255)
    
    love.graphics.line(player_x, player_y, player_x, player_y - 10)
    love.graphics.points(player_x, player_y)
    
    love.graphics.translate(player_x, player_y)
	love.graphics.rotate(cam_a)
	love.graphics.translate(-player_x, -player_y)
    
    --love.graphics.line(player_x, player_y, player_x, player_y - 10)
    
    love.graphics.translate(cam_x, cam_y)
    
    love.graphics.print("Hello", 100, 100)
  
    for index, wall in ipairs(walls) do
        love.graphics.line(wall.x1, wall.y1, wall.x2, wall.y2)
    end
end

function love.update(dt)
    if love.keyboard.isDown("up") then
        cam_y = cam_y + 2 * math.cos(cam_a) -- cam_y + 1
        cam_x = cam_x + 2 * math.sin(cam_a)
    end
    if love.keyboard.isDown("down") then
        cam_y = cam_y - 2 * math.cos(cam_a) -- cam_y - 1
        cam_x = cam_x - 2 * math.sin(cam_a)
    end
    if love.keyboard.isDown("right") then
        -- cam_x = cam_x + 1
        cam_a = cam_a - 0.05
    end
    if love.keyboard.isDown("left") then
        -- cam_x = cam_x - 1
        cam_a = cam_a + 0.05
    end
end
