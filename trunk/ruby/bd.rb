require_gem 'activerecord'

ActiveRecord::Base.establish_connection(
    :adapter => 'mysql',
    :database => 'testrb',
    :host => 'localhost',
    :username => 'root',
    :password => 'asydug5'
  )

class Movie < ActiveRecord::Base
	def title=(v)
		self[:title]=v
	end
end

m = Movie.new(:id=>20920, :title => 'A simple plan')
m.title = 'Pipo'
m.save

