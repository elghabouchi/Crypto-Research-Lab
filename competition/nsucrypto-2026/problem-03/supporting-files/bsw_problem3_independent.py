from time import perf_counter

def independent(p):
    S=sorted({x*x%p for x in range(1,p)})
    T=sorted(set(range(1,p))-set(S))
    nonsquares=set(T)
    count=bad=nodes=0
    def visit(i,chosen,unused):
        nonlocal count,bad,nodes
        nodes+=1
        if i==len(S):
            count+=1
            if len({s*t%p for s,t in chosen})!=1:bad+=1
            return
        s=S[i]
        for t in sorted(unused):
            if all(((s-u)*(s-v)*(t-u)*(t-v))%p in nonsquares for u,v in chosen):
                visit(i+1,chosen+[(s,t)],unused-{t})
    visit(0,[],set(T))
    print(dict(q=p, independent_solutions=count,
               nonstandard=bad, nodes=nodes), flush=True)
    assert count==len(S) and bad==0
for p in (43,47):independent(p)
