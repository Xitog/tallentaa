-------------------------------------------------------------------------------
-- Players
-------------------------------------------------------------------------------

function create_player(game, name, color)
    local player = {}
    player.name = name
    player.color = color
    player.units = {}
    player.selected = {}
    player.game = game
    game.players[#game.players+1] = player
    return player
end

-------------------------------------------------------------------------------
-- Units
-------------------------------------------------------------------------------

global_id = 1

function create_unit(player, x, y, size, move)
    if player == nil then
        error("Player is nil")
    end
    local u = {}
    u.player = player
    player.units[#player.units+1] = u
    u.x = math.floor(x/32)*32+16
    u.y = math.floor(y/32)*32+16
    u.x32 = math.floor(x/32)+1
    u.y32 = math.floor(y/32)+1
    u.rate = 100
    u.size = size
    u.move = move
    -- Faire une fonction baptiser ?
    u.id = global_id
    global_id = global_id + 1
    u.type = 'unit'
    
    u.next = {}
    u.next.x32 = 0
    u.next.y32 = 0
    u.next.x = 0
    u.next.y = 0
    
    u.next.step = {}
    u.next.step.x = 0
    u.next.step.y = 0
    
    u.target = {}
    u.target.x32 = 0
    u.target.y32 = 0
    u.target.x = 0
    u.target.y = 0
    
    u.in_transition = false
    return u
end

function set_target(unit, x, y)
    x = math.floor(x/32)*32 + 16
    y = math.floor(y/32)*32 + 16
    unit.target.x = x
    unit.target.y = y
    unit.in_transition = true
end

function update(unit)
    unit.player.game.map.unit[unit.y32][unit.x32] = 0
    if unit.in_transition then
        get_closer_of_target(unit)
    end
    unit.player.game.map.unit[unit.y32][unit.x32] = unit
end

function get_closer_of_target(u)
    --print('Moving', player.in_transition, "p32 = " .. player.x32, player.y32, "p = " .. player.x, player.y, "next = " .. player.next.x32, player.next.y32, "target = " .. player.target.x32, player.target.y32)
    if u.x ~= u.target.x or u.y ~= u.target.y then
        if u.in_transition then
            -- On calcule la direction vers laquelle on va
            if u.x > u.target.x then
                u.next.step.x = -1
            elseif u.x < u.target.x then
                u.next.step.x = 1
            else
                u.next.step.x = 0
            end
            if u.y > u.target.y then
                u.next.step.y = -1
            elseif u.y32 < u.target.y then
                u.next.step.y = 1
            else
                u.next.step.y = 0
            end
            -- Il ne faut pas dépasser la cible !
            if math.abs(u.x - u.target.x) < u.next.step.x * u.move then
                u.next.x = u.target.x
            else
                u.next.x = u.x + u.next.step.x * u.move
            end
            if math.abs(u.y - u.target.y) < u.next.step.y * u.move then
                u.next.y = u.target.y
            else
                u.next.y = u.y + u.next.step.y * u.move
            end
            u.next.x32 = math.floor(u.next.x / 32) + 1
            u.next.y32 = math.floor(u.next.y / 32) + 1
            -- Next position check
            if u.player.game.map.unit[u.next.y32][u.next.x32] == 0 then
                u.x = u.next.x
                u.y = u.next.y
                u.x32 = u.next.x32
                u.y32 = u.next.y32
            end
        end
    else
        u.in_transition = false
        --print('Target Reached')
    end
 end
 