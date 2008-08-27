

# type nomVar;

# int a;
# int * b = NULL;
# int * * c;

# *(&a) = a

# float d = (float) 5;

# int * a = (int *) malloc(sizeof(int));
# *a = 5

# Thread::new
x = Thread.new { sleep 0.1; print "x"; print "y"; print "z" }
a = Thread.new { print "a"; print "b"; sleep 0.2; print "c" }
x.join # Let the threads finish before
a.join # main thread exits...

#abxyzc

puts ""

# Thread::pass
a = Thread.new { print "a"; Thread.pass;
                 print "b"; Thread.pass;
                 print "c" }
b = Thread.new { print "x"; Thread.pass;
                 print "y"; Thread.pass;
                 print "z" }
a.join
b.join

#axbycz

puts ""

t1 = Thread.new { 
		  print "t1 start"; Thread::pass;
		  print "t1 end"
}

t2 = Thread.new {
		  print "t2 start"; Thread::pass;
		  print "t1 end"
}

# t1 startt2 startt1 end
