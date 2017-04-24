import csvtodb as db
import sys
import time

class posGain:
    def analyzeScript(self, script, df, args):
        self.sl = int(args[0])
        self.ll = int(args[1])
        ret = ""
        tail = df.tail(self.ll)
        if len(tail.index) == self.ll:
            incrSL = (tail['Close'][-1] - tail['Close'][-self.sl])/tail['Close'][-self.sl]
            incrLL = (tail['Close'][-1] - tail['Close'][-self.ll])/tail['Close'][-self.ll]
            posRet = (script, str("%.2f" % (incrSL*100)), str("%.2f" % (incrLL*100)))
            ret = ("", posRet)[incrSL > 0]
        return ret

    def report(self, rep):
        report = sorted(rep, reverse=True, key=lambda x:x[1])
        slHeader = str(self.sl) + "_DAY_MOVE"
        llHeader = str(self.ll) + "_DAY_MOVE"
        F = open("posGain" + time.strftime("%Y%m%d-%H%M%S") + ".csv", "w")
        F.write("%20s,%12s,%12s" % ("SYMBOL", slHeader, llHeader))
        F.write("\n".join(map(lambda x:("%20s,%12s,%12s" % (x[0], x[1], x[2])), report)))
        F.close()

def report(c, args):
    com = c()
    rep = []
    s = db.getLastDayScripts()
    if s != -1:
        sc = [str(r[0]) for r in s]
        for scr in sc:
            df = db.obtainQuotes(scr)
            r = com.analyzeScript(scr, df, args)
            if r:
                rep.append(r)
        com.report(rep)

def _printUsage():
    pass

def main(args):
    commands = { 'posGain' : posGain,
            }
    if args:
        c = args[0]
        c = c[1:]
        try:
            f = commands[c]
        except KeyError:
            raise ValueError('Unsupported function')
        report(f, args[1:])
    else:
        _printUsage()

if __name__ == "__main__":
    main(sys.argv[1:])
