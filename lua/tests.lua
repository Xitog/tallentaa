-- Sequence
a = 5 b = 6 -- New line doesn't mean anything
c = { 10, 20, 30, 40, 50}
d = { alpha = 55, beta = 66, zeta = null, ["zorba"] = "youpi" }

-- Selection
if a == 5 and b == 6 then
    print("a equals 5 and b equals " .. b) -- concat string with ..
end

-- Itération
while a > 0 do
    print(a)
    a = a - 1 -- no x= operators
end -- no else in while loop

for index, value in ipairs(c) do
    print(index, ' => ', value)
end

for key, value in pairs(d) do
    print(key, ' => ', value) -- zeta is not treated
end

if d.zeta then
    print("never will be")
else
    print("zeta key value is null")
end

if d.nokey then
    print("never will be")
else
    print("nokey doesn't exist")
end

repeat
    print(a)
    a = a + 1
until a >= 5

-- Type
print(type(4))
print(type("abc"))
print(type({}))

-- Matrix
matrix = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0},
    {0, 0, 0, 0, 1, 0},
    {0, 0, 2, 1, 1, 0},
    {0, 0, 1, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
}
matrix.size = 6
for line, vline in ipairs(matrix) do
    for col, value in ipairs(vline) do
        io.stdout:write(value .. ' ')
    end
    print()
end
print("Line 4 Column 3 =" .. matrix[4][3]) -- y puis x
print(matrix.size)

-- Table & metatable (10h38 : that's ok :-)
people_class_methods = {
    new = function(default_name)
        i = {}
        setmetatable(i, {__index = people_instance_methods})
        i:init(default_name)
        return i
    end
}
people_instance_methods = {
    init = function(self, default_name)
        self.name = default_name
    end,
    hello = function(self)
        print("Hello! I'm " .. self.name)
    end,
    setname = function(self, new_name)
        self.name = new_name
    end,
}

p1 = people_class_methods.new("Bob")
p1:hello()
p1:setname("Zorba")
p1:hello()

-- Open / Write files
f = io.open("pipo.txt", "w")
if f == nil then
    print("Pb to open in w mode")
end
f:write("hello pipo!\n")
f:write("another line to the pipo!\n")
f:close()

f = io.open("pipo.txt", "r")
s = f:read("*line") -- read only one line by default, () equivalent to ("*line")
print("read one (text, line): " .. s)
f:close()

f = io.open("pipo.txt", "r") -- in C, when you read in text mode, end of line are converted to standard "\n"
s = f:read("*all")
print("read two (text, all): " .. s)
f:close()

f = io.open("pipo.txt", "rb")
s = f:read("*all")
print("read three (binary, all): " .. s)
f:close()

lines = 0
for line in io.lines("pipo.txt") do
    print(lines .. " : " .. line)
    lines = lines + 1
end

-- Read / write on stdin
io.stdout:write("Enter a line:\n")
s = io.stdin:read()
print(s)
