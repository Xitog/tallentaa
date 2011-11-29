require 'gosu'
class Test < Gosu::Window
  def initialize
    super 800, 600, false, 20
  end
  def update
    self.caption = "#{self.mouse_x} / #{self.mouse_y}"
  end
end
Test.new.show

