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
