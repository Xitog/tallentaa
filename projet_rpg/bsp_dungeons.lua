Division = {}
Division.verticale = 1
Division.horizontale = 2

UNSET = -1

root = {}
root.x = 0
root.y = 0
root.w = 100
root.h = 100
root.div = UNSET
root.div_pos = UNSET
root.wall_thickness = UNSET
root.left = UNSET
root.right = UNSET

--https://www.lua.org/pil/19.3.html
--root.ordered = {}
--for k in pairs(root) do table.insert(rootx, k) end
--table.sort(rootx)
--http://lua-users.org/wiki/OrderedTable

-- il n'y a pas de fonction de base pour copier une liste !
-- il n'y a pas de fonction de base pour tester la présence dans une liste !
-- pairs ne retourne rien si la valeur est à nul !!! MAIS QUEL MERDE CE LANGAGE !
-- http://lua-users.org/wiki/CopyTable
-- pas de local par défaut !!!
-- Devrait être automatique
math.randomseed(os.time())
-- Pas de valeur par défaut des paramètres !!!
-- égalité de type par des chaînes !!! == 'table' ?!

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

function display_node(node, level)
    print(space(level) .. '--------')
    print(space(level) .. 'x,y = ' .. node.x .. ',' .. node.y)
    print(space(level) .. 'w,h = ' .. node.w .. ',' .. node.h)
    if node.div == Division.verticale then
        print(space(level) .. 'div = verticale')
    else
        print(space(level) .. 'div = horizontale')
    end
    print(space(level) .. 'div_pos = ' .. node.div_pos)
    print(space(level) .. 'wall_thickness = ' .. node.wall_thickness)
    if node.left ~= UNSET then
        display_node(node.left, level+1)
    end
    if node.right ~= UNSET then
        display_node(node.right, level+1)
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

-- Test
print("Test clone :")
node2 = clone(root)
root.x = 20
print(node2, type(node2))
display(node2, 0)
print("Should be 0 = ", node2.x)
print("Should be 20 = ", root.x)
root.x = 0
print()

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
    -- wall thickness
    if base_len == 1 then
        error("unable to divide type|len", node.div, base_len)
    elseif base_len > 1 and base_len <= 5 then
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
    end
    -- calc div pos and children
    local mid = math.floor(base_len / 2)                      -- ex : 5
    local mid_of_mid = math.floor(mid / 2)                    -- 2
    node.div_pos = mid + math.random(-mid_of_mid, mid_of_mid) -- -2|+2
    if node.div == Division.verticale then
        node.left = {}
        node.left.x = node.x
        node.left.y = node.y
        node.left.w = node.div_pos
        node.left.h = node.h
        node.left.div = UNSET
        node.left.div_pos = UNSET
        node.left.wall_thickness = UNSET
        node.left.left = UNSET
        node.left.right = UNSET
        
        if node.left.w > 5 or node.left.h > 5 then
            choose(node.left)
        end
        
        node.right = {}
        node.right.x = node.x + node.div_pos
        node.right.y = node.y
        node.right.w = node.w - node.div_pos
        node.right.h = node.h
        node.right.div = UNSET
        node.right.div_pos = UNSET
        node.right.wall_thickness = UNSET
        node.right.left = UNSET
        node.right.right = UNSET
        
        if node.right.w > 5 or node.right.h > 5 then
            choose(node.right)
        end
    elseif node.div == Division.horizontale then
        node.left = {}
        node.left.x = node.x
        node.left.y = node.y
        node.left.w = node.w
        node.left.h = node.div_pos
        node.left.div = UNSET
        node.left.div_pos = UNSET
        node.left.wall_thickness = UNSET
        node.left.left = UNSET
        node.left.right = UNSET
        
        if node.left.w > 7 or node.left.h > 7 then
            choose(node.left)
        end
        
        node.right = {}
        node.right.x = node.x
        node.right.y = node.y + node.div_pos
        node.right.w = node.w
        node.right.h = node.h - node.div_pos
        node.right.div = UNSET
        node.right.div_pos = UNSET
        node.right.wall_thickness = UNSET
        node.right.left = UNSET
        node.right.right = UNSET
        
        if node.right.w > 5 or node.right.h > 5 then
            choose(node.right)
        end
    end
end

choose(root)
display_node(root, 0)

