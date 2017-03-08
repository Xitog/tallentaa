Division = {}
Division.verticale = 1
Division.horizontale = 2

UNSET = -1
-- MIN_DIVISIBLE = 24 -- 8 => 834 salles ! 24 => 88 salles
GLOBAL_ID = 0
MAX_DEEP = 3 -- 2 => 4 salles. 3 => 8 salles. 4 => 16 salles.

function create_node(x, y, w, h, deep)
    node = {}
    node.type = 'node'
    node.id = GLOBAL_ID
    GLOBAL_ID = GLOBAL_ID + 1
    node.x = x
    node.y = y
    node.w = w
    node.h = h
    node.deep = deep
    node.div = UNSET
    node.div_pos = UNSET
    node.wall_thickness = UNSET
    node.left = UNSET
    node.right = UNSET
    return node
end

root = create_node(0, 0, 100, 100, 1)
math.randomseed(os.time())

function clone(target)
    local r = {}
    --for key, value in next, target, nil do
    for key, value in pairs(target) do
        --print("cloning: ", key, value)
        if type(value) == 'table' then
            r[key] = clone(value)
        else
            r[key] = value
        end
    end
    return r
end

function display(target, level)
    for key, value in pairs(target) do
        if value ~= UNSET and type(value) ~= 'table' then
            print(space(level) .. key .. " = " .. value)
        end
    end
end

function d2(s, file)
    print(s)
    file:write(s .. '\n')
end

function display_node(node, level, file)
    local s = space(level) .. '--------'
    d2(s, file)
    s = space(level) .. 'id = ' .. node.id .. ' deep = ' .. node.deep
    d2(s, file)
    s = space(level) .. 'x,y = ' .. node.x .. ',' .. node.y
    d2(s, file)
    s = space(level) .. 'w,h = ' .. node.w .. ',' .. node.h
    d2(s, file)
    if node.div == Division.verticale then
        s = space(level) .. 'div = verticale'
        d2(s, file)
    else
        s = space(level) .. 'div = horizontale'
        d2(s, file)
    end
    s = space(level) .. 'div_pos = ' .. node.div_pos
    d2(s, file)
    s = space(level) .. 'wall_thickness = ' .. node.wall_thickness
    d2(s, file)
    if node.left ~= UNSET then
        display_node(node.left, level+1, file)
    end
    if node.right ~= UNSET then
        display_node(node.right, level+1, file)
    end
end

function space(level)
    local s = ""
    if level <= 0 then return s end
    for i=1, level do
        s = s.. "    "
    end
    return s
end

function choose(node)
    -- verti ou horizon
    local base_coo = 0
    local base_len = 0
    if node.w > node.h then
        node.div = Division.verticale
        base_coo = node.x
        base_len = node.w
    elseif node.w <= node.h then
        node.div = Division.horizontale
        base_coo = node.y
        base_len = node.h
    end
    -- wall thickness and minimum
    --if base_len < MIN_DIVISIBLE then
    --    return nil
    --[[if base_len > 1 and base_len <= 5 then
        if math.random(1, 100) > 90 then
            node.wall_thickness = 0
        else
            node.wall_thickness = 1
        end
    elseif base_len > 5 and base_len <= 10 then
        if math.random(1, 100) > 90 then
            node.wall_thickness = 0
        else
            node.wall_thickness = math.random(1, 3)
        end
    else
        node.wall_thickness = math.random(1, 3)
    end]]
    -- calc div pos and children
    local mid = math.floor(base_len / 2)                      -- ex : 5
    local mid_of_mid = math.floor(mid / 2)                    -- 2
    node.div_pos = mid + math.random(-mid_of_mid, mid_of_mid) -- -2|+2
    if node.div == Division.verticale then
        node.left = create_node(node.x, node.y, node.div_pos, node.h, node.deep+1)
        node.right = create_node(node.x + node.div_pos, node.y, node.w - node.div_pos, node.h, node.deep+1)
    elseif node.div == Division.horizontale then
        node.left = create_node(node.x, node.y, node.w, node.div_pos, node.deep+1)
        node.right = create_node(node.x, node.y + node.div_pos, node.w, node.h - node.div_pos, node.deep+1) 
    end
    -- Maximum
    if node.deep < MAX_DEEP then
        choose(node.left)
        choose(node.right)
    else
        table.insert(leaves, node.left)
        table.insert(leaves, node.right)
    end
end

leaves = {}
choose(root)
local file = io.open ('./output/' .. os.time() .. '.txt', 'w')
display_node(root, 0, file)

function tree_to_matrix(tree)
    -- Create matrix
    local matrix = {}
    for col = tree.x, tree.w do
        matrix[col] = {}
        for lin = tree.y, tree.h do
            matrix[col][lin] = 0
        end
    end
    matrix.w = tree.w
    matrix.h = tree.h
    -- Make wall for leaf
    for i, v in pairs(leaves) do
        v.wall_thickness = 1
    end
    -- Go through the tree (the root has no wall thickness)
    create_rooms(tree.right, matrix)
    create_rooms(tree.left, matrix)
    return matrix
end

function create_rooms(tree, matrix)
    if tree == nil then
        return
    end
    if type(tree) ~= 'table' then
        return
    end
    if tree.type ~= 'node' then
        return
    end
    for col = tree.x, tree.x + tree.w do
        for lin = tree.y, tree.y + tree.h do
            if col - tree.x <= tree.wall_thickness or lin - tree.y <= tree.wall_thickness or (tree.x + tree.w) - col <= tree.wall_thickness or (tree.y + tree.h) - lin <= tree.wall_thickness then
                matrix[col][lin] = 666 -- hard wall
            else
                matrix[col][lin] = tree.id
            end
        end
    end
    create_rooms(tree.right, matrix)
    create_rooms(tree.left, matrix)
end

print("GLOBAL_ID = ", GLOBAL_ID, " LAST CREATED ID = ", GLOBAL_ID - 1)
mx = tree_to_matrix(root)

if love ~= nil then
    
    textures = {}
    font = love.graphics.newFont(30);
    
    function load_textures()
        black = love.graphics.newImage('assets/textures/black.png')
        textures = { 
            love.graphics.newImage('assets/textures/white.png'),
            love.graphics.newImage('assets/textures/red.png'),
            love.graphics.newImage('assets/textures/green.png'),
            love.graphics.newImage('assets/textures/blue.png'),
            love.graphics.newImage('assets/textures/grey.png'),
            love.graphics.newImage('assets/textures/orange.png'),
            love.graphics.newImage('assets/textures/brown.png'),
            love.graphics.newImage('assets/textures/light_blue.png'),
            love.graphics.newImage('assets/textures/light_green.png'),
            love.graphics.newImage('assets/textures/pink.png'),
            --love.graphics.newImage('assets/textures/black.png'),
            love.graphics.newImage('assets/textures/dark_brown.png'),
            love.graphics.newImage('assets/textures/yellow.png'),
            love.graphics.newImage('assets/textures/purple.png'),
            love.graphics.newImage('assets/textures/dark_grey.png'),
        }
    end
    
    function draw_matrix(matrix)
        print("Drawing matrix")
        local canvas = love.graphics.newCanvas(matrix.w * 32, matrix.h * 32)
        love.graphics.setCanvas(canvas)
        love.graphics.setFont(font)
        for col=1, matrix.w do
            for lin=1, matrix.h do
                if matrix[col][lin] ~= 666 then
                    love.graphics.draw(textures[matrix[col][lin]], (lin-1)*32, (col-1)*32)
                else
                    love.graphics.draw(black, (lin-1)*32, (col-1)*32)
                end
                love.graphics.setColor(0, 0, 0)
                love.graphics.print(tostring(matrix[col][lin]), (lin-1)*32, (col-1)*32)
                love.graphics.setColor(255, 255, 255)
            end
        end
        love.graphics.setCanvas()
        love.filesystem.setIdentity("BSPDungeons")
        local data = canvas:newImageData( )
        data:encode('png', os.time() .. '.png')
    end

    function love.load()
        load_textures()
        draw_matrix(mx)
    end
end
