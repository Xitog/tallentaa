#!/usr/bin/ruby

#pron.:168684:se:pronom:personnel:réfléchi::mots-outils

class WordList

    attr_reader :words, :cats
    
    def initialize(words=[])
        @words = words
        @cats = []
    end
    
    def add(w)
        @words << w
    end
    
    def add_cat(c)
        @cats << c
    end
    
    def length
        return @words.length
    end

    def include?(search)
        for w in @words do
            if w.val == search then return true end
        end
        return false
    end
    
    def select(what, value)
        selection = []
        for w in @words do
            if what == 'cat' and w.cat == value then selection << w end
        end
        return WordList.new(selection)
    end
    
    def WordList.load(file)
        f = File.open(file)
        lines = f.readlines()
        words = WordList.new
        for row in lines do
            columns = row.split(':')
            w = Word.new(columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7].chomp)
            if !words.cats.include?(columns[7]) then
                words.add_cat(columns[7])
            end
            words.add(w)
        end
        return words
    end

    def save(file)
        f = File.open(file, 'w')
        for w in @words do
            f.write(w.to_format+"\n")
        end
    end
    
    def to_a
        return @words
    end

end

class Word

    attr_reader :typ, :freq, :val, :kind, :subkind, :subsubkind, :x, :cat
    
    def initialize(typ, freq, val, kind, subkind, subsubkind, x, cat)
        @typ = typ
        @freq= freq
        @val = val
        @kind = kind
        @subkind = subkind
        @subsubkind = subsubkind
        @x = x
        @cat = cat
    end

    def to_s
        return "#{@base},#{@kind},#{@subkind},#{@cat}"
    end
    
    def to_format
        return [@typ, @freq, @val, @kind, @subkind, @subsubkind, @x, @cat].join(':')
    end
    
end

#words = WordList.load('base.data')
#for w in words.to_a do
#    puts w.to_format
#end
#puts words.length
#puts words.include?('confondre')
#words.save('pipo.data')

#wl = words.select('cat', 'la maison')
#for w in wl.to_a do
#    puts w
#end
