a = true
b = true

if a then println("OK 1") end
if a then if b then println("OK 2") end end

if a then
    println("OK 3")
    println("OK 4")
end

if a then
    println("OK 5")
    if b then
        println("OK 6")
    end
end

if a then
    println("OK 7")
end

unless a then println("ERR 1") else println("OK 8") end

unless a then
    println("ERR 2")
else
    println("OK 9")
end

unless a then
    println("ERR 2")
else println("OK 10")
end

c = 22

if c == 1 then
    println("ERR 3")
elsif c == 2 then
    println("ERR 4")
elsif c == 22 then
    println("OK 11")
elsif c == 3 then
    println("ERR 5")
end

if c == 3 then
    println("ERR 6")
elsif c == 4 then
    println("ERR 7")
else
    println("OK 12")
end

2