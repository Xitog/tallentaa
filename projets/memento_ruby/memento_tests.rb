class Pipo
    attr_reader :a
    def initialize(a)
        @a = a
    end
    def +(other)
        return Pipo.new(@a.upcase + other.a.upcase)
    end
end

a = Pipo.new("abc")
b = Pipo.new("cde")
puts (a+b).a

for i in 1..3 # lance 3 fois un dé
  de = Random.new.rand(1..6)
  puts i, de
  #retry if de == 1 # recommence tout si on tombe sur 1
  redo if de < 4 # recommence l'itération si on tombe sur 2 ou 3
  puts "un lancer validé"
end

a = 5
begin
    puts "hello"
    puts "world"
end if a != 5
