S0,S1,S2,S3,S4 = 0,1,2,3,4
NAMES = {S0:"S0/IDLE",S1:"S1/got-1",S2:"S2/got-10",S3:"S3/got-101",S4:"S4/MATCH"}

def nxt(s,b):
    if s==S0: return S1 if b else S0
    elif s==S1: return S2 if not b else S1
    elif s==S2: return S3 if b else S0
    elif s==S3: return S4 if b else S2
    elif s==S4: return S1 if b else S2
    return S0

def out(s,b): return 1 if s==S3 and b==1 else 0

def run(name, bits):
    print(f"\n{'='*50}\nTEST: {name}\n{'='*50}")
    print(f"  {'Cyc':<5} {'In':<4} {'State':<16} {'Detected'}")
    print(f"  {'-'*40}")
    s=S0; dets=[]
    for i,b in enumerate(bits):
        d=out(s,b); ns=nxt(s,b)
        flag="  <<< DETECTED!" if d else ""
        print(f"  {i+1:<5} {b:<4} {NAMES[s]:<16} {d}{flag}")
        if d: dets.append(i+1)
        s=ns
    print(f"  Final: {NAMES[s]} | Detections at cycles: {dets or 'none'}")

print("1011 Sequence Detector — FSM Simulation")
run("Basic 1011",           [1,0,1,1])
run("Wrong pattern 1010",   [1,0,1,0])
run("Overlapping 10111011", [1,0,1,1,1,0,1,1])
run("Noisy 0001011",        [0,0,0,1,0,1,1])
run("All zeros",            [0,0,0,0,0,0])
run("All ones",             [1,1,1,1,1,1])
print("\nAll tests complete!")
