--
-- Original CPP code is:
--
-- Copyright (c) 2004-2007, Lode Vandevenne
--
-- All rights reserved.
--
--------------------------------------------------------------------------------
--
-- Original CPP code license is:
--
--  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
-- 
-- * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
-- * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
-- 
-- THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
-- "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
-- LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
-- A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
-- CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
-- EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
-- PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
-- PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
-- LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
-- NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
-- SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--
--------------------------------------------------------------------------------
--
-- Translation in Lua was made by Damien Gouteux in 2017 and is licensed under the terms of previous license.
--

textures = {
    love.graphics.newImage("Texture.png")
}

mapWidth = 24
mapHeight = 24
texWidth = 64
texHeight = 64

worldMap = {
            {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1},
            {1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1},
            {1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1},
            {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1},
            {1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
            {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}
    }

-- x and y start position
posX = 22.0
posY = 12.0
-- initial direction vector
dirX = -1.0
dirY = 0.0
-- the 2d raycaster version of camera plane
planeX = 0.0
planeY = 0.66

curTime = 0.0 -- time of current frame
oldTime = 0.0 -- time of previous frame

w = 512
h = 384

up = false
down = false
right = false
left = false
done = false
    
function love.load()
    love.window.setTitle("raycaster")
    success = love.window.setMode( w, h, {} )
    love.graphics.setBackgroundColor(0, 0, 0)
    if not success then
        os.exit(1)
    end
end

function love.draw()
    for x = 0, w-1 do
        -- calculate ray position and direction 
        cameraX = 2 * x / w - 1 -- x-coordinate in camera space
        rayPosX = posX
        rayPosY = posY
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX
        
        -- which box of the map we're in  
        mapX = math.floor(rayPosX)
        mapY = math.floor(rayPosY)
        
        -- length of ray from current position to next x or y-side
        sideDistX = 0.0
        sideDistY = 0.0
        
        -- Added by me
        if rayDirX == 0 then rayDirX = 0.00001 end
        if rayDirY == 0 then rayDirY = 0.00001 end
        
        -- length of ray from one x or y-side to next x or y-side
        deltaDistX = math.sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
        deltaDistY = math.sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
        perpWallDist = 0.0
        
        -- what direction to step in x or y-direction (either +1 or -1)
        stepX = 0
        stepY = 0
        
        -- was there a wall hit?
        hit = false 
        side = 0 -- was a NS or a EW wall hit?
        
        -- calculate step and initial sideDist
        if rayDirX < 0 then
            stepX = -1
            sideDistX = (rayPosX - mapX) * deltaDistX
        else
            stepX = 1
            sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX
        end
        if rayDirY < 0 then
            stepY = -1
            sideDistY = (rayPosY - mapY) * deltaDistY
        else
            stepY = 1
            sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY
        end
        
        -- perform DDA
        while not hit do
            -- jump to next map square, OR in x-direction, OR in y-direction
            if sideDistX < sideDistY then
                sideDistX = sideDistX + deltaDistX
                mapX = mapX + stepX
                side = 0
            else
                sideDistY = sideDistY + deltaDistY
                mapY = mapY + stepY
                side = 1
            end
            
            -- Check if ray has hit a wall
            if worldMap[mapX + 1][mapY + 1] > 0 then -- lua array indexes start at 1
                hit = true
            end
        end
        
        -- Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
        if side == 0 then
            perpWallDist = math.abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX)
        else
            perpWallDist = math.abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY)
        end
        
        -- Calculate height of line to draw on screen
        lineHeight = math.abs(math.floor(h / perpWallDist))
        
        -- calculate lowest and highest pixel to fill in current stripe
        drawStart = -lineHeight / 2 + h / 2
        if drawStart < 0 then
            drawStart = 0
        end
        drawEnd = lineHeight / 2 + h / 2
        if drawEnd >= h then
            drawEnd = h - 1
        end
        
        -- choose wall color
        color = {128, 128, 0}
        --texnum = worldMap[mapX + 1][mapY + 1] -- Lua indexes start at 1
        texNum = 1
        
        -- calculate value of wallX
        if side == 0 then
            wallX = rayPosY + perpWallDist * rayDirY
        else
            wallX = rayPosX + perpWallDist * rayDirX
        end
        wallX = wallX - math.floor(wallX)
        
        -- x coordinate on the texture
        texX = math.floor(wallX * texWidth)
        if side == 0 and rayDirX > 0 then
            texX = texWidth - texX - 1
        end
        if side == 1 and rayDirY < 0 then 
            texX = texWidth - texX - 1
        end
        
        for y = drawStart, drawEnd do
            -- 256 and 128 factors to avoid floats
            d = y * 256 - h * 128 + lineHeight * 128
            texY = ((d * texHeight) / lineHeight) / 256
            r, g, b = textures[texNum]:getData():getPixel(math.floor(texX) % 64, math.floor(texY) % 64) -- texHeight * texY + texX
            -- make color darker for y-sides:
            -- R, G and B byte each divided through two with a "shift" and an "and"
            if side == 1 then
                r, g, b = r / 2, g / 2, b / 2 --(color >> 1) & 8355711
            end
            love.graphics.setColor(r, g, b)
            love.graphics.points(x, y)
        end
        
        -- give x and y sides different brightness
        if side == 1 then
            color = {color[1] / 2, color[2] / 2, color[3] / 2}
        end
        
        -- draw the pixels of the stripe as a vertical line
        love.graphics.setColor(color[1], color[2], color[3])
        love.graphics.line(x, drawStart, x, drawEnd)
        
    end
end

function love.keypressed( key, scancode, isrepeat )
    if key == "right" then
        right = true
    end
    if key == "left" then
        left = true
    end
    if key == "up" then
        up = true
    end
    if key == "down" then
        down = true
    end
end
    
function love.keyreleased( key, scancode, isrepeat )
    if key == "escape" then
        love.event.quit()
    end
    if key == "right" then
        right = false
    end
    if key == "left" then
        left = false
    end
    if key == "up" then
        up = false
    end
    if key == "down" then
        down = false
    end
end
    
function love.update(frameTime)
    -- speed modifiers
    moveSpeed = frameTime * 5.0 -- the constant value is in squares/second
    rotSpeed = frameTime * 3.0 -- the constant value is in radians/second
    
    -- move forward if no wall in front of you (in Lua indexes start at 1)
    if up then
        new = posX + dirX * moveSpeed
        if new >= 0 and worldMap[math.floor(new) + 1][math.floor(posY) + 1] == 0 then
            posX = new
        end
        new = posY + dirY * moveSpeed
        if new >= 0 and worldMap[math.floor(posX) + 1][math.floor(new) + 1] == 0 then
            posY = new
        end
    end
    -- move backwards if no wall behind you (in Lua indexes start at 1)
    if down then
        new = posX - dirX * moveSpeed
        if new >= 0 and worldMap[math.floor(new) + 1][math.floor(posY) + 1] == 0 then
            posX = new
        end
        new = posY - dirY * moveSpeed
        if new >= 0 and worldMap[math.floor(posX) + 1][math.floor(new) + 1] == 0 then
            posY = new
        end
    end
    -- rotate to the right
    if right then
        -- both camera direction and camera plane must be rotated
        oldDirX = dirX
        dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
        dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
        planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)
    end
    -- rotate to the left
    if left then
        -- both camera direction and camera plane must be rotated
        oldDirX = dirX
        dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
        dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
        planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)
    end
end
