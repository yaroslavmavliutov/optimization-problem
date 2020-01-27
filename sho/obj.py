def save(sol, func, nrun, fname):
    val = func(sol)
    with open(fname+str(nrun)+".csv", 'a') as fd:
        fd.write("{val};{sol}\n".format(val=val, sol=sol))
    return val