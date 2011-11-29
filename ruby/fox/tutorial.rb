require 'fox14'

include Fox

theApp = FXApp.new

# File rdoc-sources/FXMainWindow.rb, line 23
#def initialize(app, title, icon=nil, miniIcon=nil, opts=DECOR_ALL, x=0, y=0, width=0, height=0, padLeft=0, padRight=0, padTop=0, padBottom=0, hSpacing=4, vSpacing=4) # :yields: theMainWindow
#end
    
theMainWindow = FXMainWindow.new(theApp, "Hello",nil,nil,DECOR_ALL,20,40,200,400)
theApp.create

theMainWindow.show

theApp.run
