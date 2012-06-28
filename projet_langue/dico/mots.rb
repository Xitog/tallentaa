#!/usr/bin/ruby

class Mot
    attr_reader :base, :kind, :cat
    
    def initialize(base, kind, cat)
        @base = base
        @kind = kind
        @cat  = cat
    end
    
    def to_s
        return "#{@base},#{@kind},#{@cat}"
    end
end

class Base
    attr_reader :words
    
    def initialize()
        f = File.new('base.data', 'r')
        lines = f.readlines()
        words = []
        for l in lines do
            part = l.split(':')
            for p in part do
                p.strip!
            end
            if part.length > 2 then
                words << Mot.new(part[0], part[1], part[2])
            end
        end
        @words = words
    end
end

#for w in words do
#    puts w
#end
#puts words.length
