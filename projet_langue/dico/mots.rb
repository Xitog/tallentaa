#http://stackoverflow.com/questions/1000688/what-is-the-canonical-way-to-trim-a-string-in-ruby-without-creating-a-new-string

f = File.new('base.data', 'r')
lines = f.readlines()
words = []

class Mot
    def initialize(base, kind, cat)
        @base = base
        @kind = kind
        @cat  = cat
    end
    
    def to_s
        return "#{@base},#{@kind},#{@cat}"
    end
end

for l in lines do
    part = l.split(':')
    for p in part do
        p.strip!
    end
    if part.length > 2 then
        words << Mot.new(part[0], part[1], part[2])
    end
end

for w in words do
    puts w
end

puts words.length
