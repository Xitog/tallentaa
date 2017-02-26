-- Commun stuff between RPG & STR

function create_map(size)
    local map = {}
    map.ground = {}
    map.unit = {}
    map.width = 32
    map.height = 32
    for i=1, map.width do
        map.ground[i] = {}
        map.unit[i] = {}
    end
    return map
end

function populate(map)
    for i=1, map.width do
        for j=1, map.height do
            map.ground[i][j] = math.random(1, 4)
            map.unit[i][j] = 0
        end
    end
end

    