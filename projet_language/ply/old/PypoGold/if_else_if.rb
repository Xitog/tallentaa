if false then
    println("ERR")
else
    println("OK")
end


if false then
    println("ERR 2")
else
    if true then
      println("OK 2")
    end
end


a = 2

if a == 1 then
    println("a = 1 ERR")
else
    if a == 2 then
        println("a = 2 OK")
    else
        if a == 3 then
            println("a = 3 ERR")
        else
            println("ERR")
        end
    end
end

#5h03 : j'ai compris !!! Il faut bien une boucle pour les champs ELSIF/ELIF !!!

2
