cmd_list  = (
        #("myscp", ("scp a.txt root@localhost:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
        #       ("remove", ("rm -i cfiles/a.txt"), (u".*rm: remove.*\?", u"yes")),
        #        ("myscp2", ("scp a.txt root@127.0.0.1:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
                ("testshell1", "python testshell.py", (u"operation","add"), \
                    (u"number1","26"),(u"number2","37"),(u"(\d)+",""),(u"(\d)+","")),
                ("testshell2", "python testshell.py", (u"operation","sub"), \
                    (u"number1","56"),(u"number2","14"),(u"(\d)+",""),(u"(\d)+","")),
                ("testshell3", "python testshell.py", \
                    (u"operation","mul"),(u"number1","65"),(u"number2","75"),(u"(\d)+",""),(u"(\d)+","")),
             )

