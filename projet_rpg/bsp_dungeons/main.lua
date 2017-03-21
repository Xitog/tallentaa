--=============================================================================
-- BSP Dungeons
-- Produce simple BSP dungeons by:
--  1) producing a tree of rooms
--      (by dividing the space Horizontally or vertically)
--  2) projecting the tree of rooms to a 2D matrix
-------------------------------------------------------------------------------
-- Author : Damien Gouteux
-- Creation : février / mars 2017
-- Last modified : 21 mars 2017
-- Language : Lua
-- Frameworks : Löve
--=============================================================================

-- Must be called only once!
math.randomseed(os.time())
    
--=============================================================================
-- MODEL
--=============================================================================

Division = {}
Division.verticale = 1
Division.horizontale = 2

UNSET = -1
GLOBAL_ID = 0
LEAF_ID = 1

function create_node(x, y, w, h, wall, deep, parent)
    node = {}
    node.type = 'node'
    node.id = GLOBAL_ID
    GLOBAL_ID = GLOBAL_ID + 1
    node.x = x
    node.y = y
    node.w = w
    node.h = h
    node.deep = deep -- level of deepness into the tree of rooms
    node.div = UNSET -- if div is vertical or horizontal
    node.div_pos = UNSET -- where is the div
    node.link = UNSET -- where is the link between the two room 
    node.left = UNSET -- child 1
    node.right = UNSET -- child 2
    node.leaf = false -- is a leaf? (left & right = UNSET)
    node.lid = UNSET -- leaf id
    node.wall_thickness = wall -- thickness of the wall
    if parent ~= nil then
        node.parent = parent -- parent
    else
        node.parent = UNSET -- parent
    end
    return node
end

-------------------------------------------------------------------------------
-- Build the tree of rooms
-- For a given @node, choose its separation and size.
-- If its deepness is < to @max_deepness, continue to choose for its children.
-- If @max_deepness :
--      2 =>  4 salles
--      3 =>  8 salles
--      4 => 16 salles
-- Store the leaves of the tree into @leaves
-------------------------------------------------------------------------------
function choose(node, max_deepness, leaves)
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
    wall_thickness = math.random(1, 3)
    print('Thickness = ' .. node.wall_thickness)
    -- calc div pos and children
    local mid = math.floor(base_len / 2)                      -- ex : 5
    local mid_of_mid = math.floor(mid / 2)                    -- 2
    node.div_pos = mid + math.random(-mid_of_mid, mid_of_mid) -- -2|+2
    if node.div == Division.verticale then
        node.left = create_node(node.x, node.y, node.div_pos, node.h, wall_thickness, node.deep+1, node)
        node.right = create_node(node.x + node.div_pos, node.y, node.w - node.div_pos, node.h, wall_thickness, node.deep+1, node)
    elseif node.div == Division.horizontale then
        node.left = create_node(node.x, node.y, node.w, node.div_pos, wall_thickness, node.deep+1, node)
        node.right = create_node(node.x, node.y + node.div_pos, node.w, node.h - node.div_pos, wall_thickness, node.deep+1, node)
    end
    -- Link between left & right (set at the level of root)
    if node.div == Division.verticale then
        node.link = math.random(node.y + node.wall_thickness, node.y + node.h - node.wall_thickness)
    elseif node.div == Division.horizontale then   
        node.link = math.random(node.x + node.wall_thickness, node.x + node.w - node.wall_thickness)
    end
    -- Maximum
    if node.deep < max_deepness then
        choose(node.left, max_deepness, leaves)
        choose(node.right, max_deepness, leaves)
    else
        table.insert(leaves, node.left)
        node.left.leaf = true
        node.left.lid = LEAF_ID
        LEAF_ID = LEAF_ID + 1
        table.insert(leaves, node.right)
        node.right.leaf = true
        node.right.lid = LEAF_ID
        LEAF_ID = LEAF_ID + 1
    end
end

-------------------------------------------------------------------------------
-- Translate the tree of rooms to a matrix
-- Take the @tree of rooms and apply it to a 2D matrix
-- Initialize the matrix
-------------------------------------------------------------------------------
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
    -- Go through the tree (the root has no wall thickness)
    create_rooms(tree.right, matrix)
    create_rooms(tree.left, matrix)
    return matrix
end

-------------------------------------------------------------------------------
-- Translate the tree of rooms to a matrix, node by node
-- Take the @tree of rooms and apply it to a 2D matrix, node by node
-------------------------------------------------------------------------------
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
    if tree.leaf then
        wall = (tree.lid + 1) * 2
        base =  tree.lid * 2 + 1
        -- make the room
        for col = tree.x, tree.x + tree.w do
            for lin = tree.y, tree.y + tree.h do
                if col - tree.x <= tree.wall_thickness or 
                    lin - tree.y <= tree.wall_thickness or 
                    (tree.x + tree.w) - col < tree.wall_thickness or 
                    (tree.y + tree.h) - lin < tree.wall_thickness then
                    -- link
                    if tree.parent.div == Division.verticale then
                        if col == tree.parent.link then
                            if tree.parent.left == tree and (tree.x + tree.w) - col < tree.wall_thickness then
                                matrix[col][lin] = tree.id
                            elseif tree.parent.right == tree and col - tree.x < tree.wall_thickness then
                                matrix[col][lin] = tree.id
                            else
                                matrix[col][lin] = wall -- hard wall
                            end
                        else
                            matrix[col][lin] = wall -- hard wall
                        end
                    elseif tree.parent.div == Division.horizontale then   
                        if lin == tree.parent.link then
                            if tree.parent.left == tree and (tree.y + tree.h) - lin <= tree.wall_thickness then
                                matrix[col][lin] = tree.id
                            elseif tree.parent.right == tree and lin - tree.y <= tree.wall_thickness then
                                matrix[col][lin] = tree.id
                            else
                                matrix[col][lin] = wall -- hard wall
                            end
                        else
                            matrix[col][lin] = wall -- hard wall
                        end
                    end
                    --matrix[col][lin] = wall -- hard wall
                else
                    matrix[col][lin] = base
                end
            end
        end
    else
        create_rooms(tree.right, matrix)
        create_rooms(tree.left, matrix)
    end
end

--=============================================================================
-- VIEWS
--=============================================================================

-------------------------------------------------------------------------------
-- Textual view
-------------------------------------------------------------------------------
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
    if node.leaf then
        s = space(level) .. 'LEAF ' .. node.lid
        d2(s, file)
    end
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
    s = space(level) .. 'link = ' .. node.link
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

-------------------------------------------------------------------------------
-- Graphical view
-------------------------------------------------------------------------------
if love ~= nil then
    
    textures = {}
    font = love.graphics.newFont(30);
    
    function load_textures()
        black = love.graphics.newImage('assets/textures/black2.png')
        textures = { 
            love.graphics.newImage('assets/textures/white.png'),
            love.graphics.newImage('assets/textures/white_wall.png'),
            love.graphics.newImage('assets/textures/red.png'),
            love.graphics.newImage('assets/textures/red_wall.png'),
            love.graphics.newImage('assets/textures/green.png'),
            love.graphics.newImage('assets/textures/green_wall.png'),
            love.graphics.newImage('assets/textures/blue.png'),
            love.graphics.newImage('assets/textures/blue_wall.png'),
            love.graphics.newImage('assets/textures/grey.png'),
            love.graphics.newImage('assets/textures/grey_wall.png'),
            love.graphics.newImage('assets/textures/orange.png'),
            love.graphics.newImage('assets/textures/orange_wall.png'),
            love.graphics.newImage('assets/textures/brown.png'),
            love.graphics.newImage('assets/textures/brown_wall.png'),
            love.graphics.newImage('assets/textures/light_blue.png'),
            love.graphics.newImage('assets/textures/light_blue_wall.png'),
            love.graphics.newImage('assets/textures/light_green.png'),
            love.graphics.newImage('assets/textures/light_green_wall.png'),
            love.graphics.newImage('assets/textures/pink.png'),
            love.graphics.newImage('assets/textures/pink_wall.png'),
            love.graphics.newImage('assets/textures/dark_brown.png'),
            love.graphics.newImage('assets/textures/dark_brown_wall.png'),
            love.graphics.newImage('assets/textures/yellow.png'),
            love.graphics.newImage('assets/textures/yellow_wall.png'),
            love.graphics.newImage('assets/textures/purple.png'),
            love.graphics.newImage('assets/textures/purple_wall.png'),
            love.graphics.newImage('assets/textures/dark_grey.png'),
            love.graphics.newImage('assets/textures/dark_grey_wall.png'),
            love.graphics.newImage('assets/textures/dark_blue.png'),
            love.graphics.newImage('assets/textures/dark_blue_wall.png'),
        }
    end
    
    function draw_matrix(matrix)
        print("Drawing matrix")
        local canvas = love.graphics.newCanvas(matrix.w * 32, matrix.h * 32)
        love.graphics.setCanvas(canvas)
        love.graphics.setFont(font)
        for col=1, matrix.w do
            for lin=1, matrix.h do
                love.graphics.draw(textures[matrix[col][lin]], (lin-1)*32, (col-1)*32)
                --if matrix[col][lin] ~= 666 then
                --    love.graphics.draw(textures[matrix[col][lin]], (lin-1)*32, (col-1)*32)
                --else
                --    love.graphics.draw(black, (lin-1)*32, (col-1)*32)
                --end
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

-------------------------------------------------------------------------------
-- Creating an instance of the model
-------------------------------------------------------------------------------
local root = create_node(0, 0, 100, 100, 0, 1) -- x, y, w, h, wall thickness, deepness
local leaves = {}
choose(root, 3, leaves)
local file = io.open (os.time() .. '.txt', 'w')
display_node(root, 0, file)

print("GLOBAL_ID = ", GLOBAL_ID, " LAST CREATED ID = ", GLOBAL_ID - 1)
-- not local, needed for graphical view
mx = tree_to_matrix(root)
