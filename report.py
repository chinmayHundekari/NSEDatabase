import csvtodb as db
import sys

def posGain(script, df, args):
    sl = int(args[0])
    ll = int(args[1])
    ret = ""
    tail = df.tail(ll)
    if len(tail.index) == ll:
        incrSL = (tail['Close'][-1] - tail['Close'][-sl])/tail['Close'][-sl]
        incrLL = (tail['Close'][-1] - tail['Close'][-ll])/tail['Close'][-ll]
        posRet = (script, str("%.2f" % (incrSL*100)), str("%.2f" % (incrLL*100)))
        ret = ("", posRet)[incrSL > 0]
    return ret

def report(func, args):
    rep = []
    s = db.getLastDayScripts()
    if s != -1:
        sc = [str(r[0]) for r in s]
        for scr in sc:
            df = db.obtainQuotes(scr)
            r = func(scr, df, args)
            if r:
                rep.append(r)
        report = sorted(rep, reverse=True, key=lambda x:x[1])
        sl = args[0] + "_DAY_MOVE"
        ll = args[1] + "_DAY_MOVE"
        print ("%20s,%12s,%12s" % ("SYMBOL", sl, ll))
        print "\n".join(map(lambda x:("%20s,%12s,%12s" % (x[0], x[1], x[2])), report))

def _printUsage():
    pass

def main(args):
    if args:
        if args[0] == "-posGain":
            report(posGain, args[1:])
        else:
            _printUsage()
    else:
        _printUsage()

if __name__ == "__main__":
    main(sys.argv[1:])
