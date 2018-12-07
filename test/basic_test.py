if __name__=="__main__":
    msg="1.0"
    print "index=",msg
    if type(msg)==type("1.0"):
        print "msg is a float number"
    print float(msg)
    print int(float(msg))
    print type(str(int(float(msg))))==type("aaa")
