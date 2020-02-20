    'Inkey$ example
    print "Keys pressed:"
    open "Inkey$ example" for graphics as #graph

    print #graph, "when characterInput [keyPressed]"
    print #graph, "trapclose [quit]"

[loopHere]

    'make sure #graph has input focus
    print #graph, "setfocus"

    'scan for events
    scan

    goto [loopHere]

[keyPressed]

    key$ = Inkey$
    if len(key$) < 2 then
        print "pressed: "; key$
      else
        print "Unhandled special key"

    end if

    goto [loopHere]

[quit]

    print "Quitting"
    close #graph
    end
