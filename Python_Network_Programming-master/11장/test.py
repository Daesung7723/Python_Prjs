from twisted.internet import reactor

def test(x):
    import time
    while 1:
        time.sleep(2)
        print(x)
        
def test1(x):
    import time
    while 1:
        time.sleep(3)
        print(x)
 
reactor.callInThread(test, "2 seconds have passed")
reactor.callInThread(test1, "Hello")
reactor.run()   

    