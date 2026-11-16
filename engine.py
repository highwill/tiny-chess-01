import json, os, sys, urllib.request, urllib.error

U = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
ON = [r * 16 + f for r in range(8) for f in range(8)]
KN = (31, 33, 14, 18, -31, -33, -14, -18)
KI = (1, -1, 16, -16, 15, 17, -15, -17)
BD = (15, 17, -15, -17)
RD = (1, -1, 16, -16)
V = (0, 100, 320, 330, 500, 900, 0, 100, 320, 330, 500, 900, 0)
PH = (0, 0, 1, 1, 2, 4, 0, 0, 1, 1, 2, 4, 0)
PR = ((5, 4, 3, 2), (11, 10, 9, 8))
PC = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6,
      "p": 7, "n": 8, "b": 9, "r": 10, "q": 11, "k": 12}
P = (
 (0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5, 5, 0, 0, 0, 20, 20, 0, 0, 0, 5, -5, -10, 0, 0, -10, -5, 5, 5, 10, 10, -20, -20, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0),
 (-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 0, 0, 0, -20, -40, -30, 0, 10, 15, 15, 10, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 10, 15, 15, 10, 5, -30, -40, -20, 0, 5, 5, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50),
 (-20, -10, -10, -10, -10, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 5, 0, 0, 0, 0, 5, -10, -20, -10, -10, -10, -10, -10, -10, -20),
 (0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 5, 5, 0, 0, 0),
 (-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 5, 5, 5, 0, -10, -5, 0, 5, 5, 5, 5, 0, -5, 0, 0, 5, 5, 5, 5, 0, -5, -10, 5, 5, 5, 5, 5, 0, -10, -10, 0, 5, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20),
 (-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20),
)
KE = (-50, -40, -30, -20, -20, -30, -40, -50, -30, -20, -10, 0, 0, -10, -20, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -30, 0, 0, 0, 0, -30, -30, -50, -30, -30, -30, -30, -30, -30, -50)
MA = 100000
INF = 999999

B = [0] * 128
t = 0
ca = 0
ep = -1
K = [0, 0]
ST = []
TT = {}
KILL = [[0, 0] for _ in range(256)]
HIST = [[0] * 128 for _ in range(13)]
ND = 0
BG = 100000
REP = []
R2 = set()


class Stop(Exception):
    pass


def k():
    return bytes(B) + bytes((t, ca, ep + 1))


def post(path, body):
    req = urllib.request.Request(U + path, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")


def setup(fen):
    global B, t, ca, ep, K
    B = [0] * 128
    w = fen.split()
    for i, row in enumerate(w[0].split("/")):
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            else:
                B[(7 - i) * 16 + f] = PC[c]
                f += 1
    t = 0 if w[1] == "w" else 1
    ca = 0
    for c in w[2]:
        if c == "K":
            ca |= 1
        elif c == "Q":
            ca |= 2
        elif c == "k":
            ca |= 4
        elif c == "q":
            ca |= 8
    ep = -1
    if w[3] != "-":
        ep = (int(w[3][1]) - 1) * 16 + ord(w[3][0]) - 97
    K = [0, 0]
    for q in ON:
        if B[q] == 6:
            K[0] = q
        elif B[q] == 12:
            K[1] = q


def uci(m):
    f = m & 127
    o = (m >> 7) & 127
    s = "abcdefgh"[f & 7] + str((f >> 4) + 1) + "abcdefgh"[o & 7] + str((o >> 4) + 1)
    pr = (m >> 14) & 15
    if pr:
        s += "nbrq"[pr - 2 if pr < 7 else pr - 8]
    return s


def parse_uci(u):
    f = (ord(u[0]) - 97) + (int(u[1]) - 1) * 16
    o = (ord(u[2]) - 97) + (int(u[3]) - 1) * 16
    pr = 0
    if len(u) == 5:
        pr = {"n": 2, "b": 3, "r": 4, "q": 5, "N": 2, "B": 3, "R": 4, "Q": 5}[u[4]]
        if t == 1:
            pr += 6
    return f | o << 7 | pr << 14


def att(s, w):
    if w:
        for x in (s - 15, s - 17):
            if not x & 0x88 and B[x] == 1:
                return 1
    else:
        for x in (s + 15, s + 17):
            if not x & 0x88 and B[x] == 7:
                return 1
    for d in KN:
        x = s + d
        if not x & 0x88 and B[x] == (2 if w else 8):
            return 1
    for d in KI:
        x = s + d
        if not x & 0x88 and B[x] == (6 if w else 12):
            return 1
    for d in BD:
        x = s + d
        while not x & 0x88:
            q = B[x]
            if q:
                if q == (3 if w else 9) or q == (5 if w else 11):
                    return 1
                break
            x += d
    for d in RD:
        x = s + d
        while not x & 0x88:
            q = B[x]
            if q:
                if q == (4 if w else 10) or q == (5 if w else 11):
                    return 1
                break
            x += d
    return 0


def gen(cp=0):
    ms = []
    A = ms.append
    for f in ON:
        p = B[f]
        if not p or (p < 7) != (t == 0):
            continue
        if p == 1 or p == 7:
            d = 16 if p == 1 else -16
            r7 = 7 if p == 1 else 0
            to = f + d
            if not B[to]:
                if (to >> 4) == r7:
                    for pr in PR[t]:
                        A(f | to << 7 | pr << 14)
                elif not cp:
                    A(f | to << 7)
                    if ((f >> 4) == 1 and p == 1 or (f >> 4) == 6 and p == 7) and not B[f + 2 * d]:
                        A(f | (f + 2 * d) << 7)
            for dd in (d - 1, d + 1):
                to = f + dd
                if to & 0x88:
                    continue
                q = B[to]
                if q and (q < 7) != (p < 7):
                    if (to >> 4) == r7:
                        for pr in PR[t]:
                            A(f | to << 7 | pr << 14)
                    else:
                        A(f | to << 7)
                elif to == ep:
                    A(f | to << 7)
        elif p == 2 or p == 8:
            for dd in KN:
                to = f + dd
                if to & 0x88:
                    continue
                q = B[to]
                if not q:
                    if not cp:
                        A(f | to << 7)
                elif (q < 7) != (p < 7):
                    A(f | to << 7)
        elif p == 6 or p == 12:
            for dd in KI:
                to = f + dd
                if to & 0x88:
                    continue
                q = B[to]
                if not q:
                    if not cp:
                        A(f | to << 7)
                elif (q < 7) != (p < 7):
                    A(f | to << 7)
            if not cp:
                if p == 6 and f == 4:
                    if ca & 1 and not B[5] and not B[6] and B[7] == 4 and not att(4, 0) and not att(5, 0) and not att(6, 0):
                        A(4 | 6 << 7)
                    if ca & 2 and not B[3] and not B[2] and not B[1] and B[0] == 4 and not att(4, 0) and not att(3, 0) and not att(2, 0):
                        A(4 | 2 << 7)
                elif p == 12 and f == 116:
                    if ca & 4 and not B[117] and not B[118] and B[119] == 10 and not att(116, 1) and not att(117, 1) and not att(118, 1):
                        A(116 | 118 << 7)
                    if ca & 8 and not B[115] and not B[114] and not B[113] and B[112] == 10 and not att(116, 1) and not att(115, 1) and not att(114, 1):
                        A(116 | 114 << 7)
        else:
            ds = BD if p in (3, 9) else RD if p in (4, 10) else BD + RD
            for dd in ds:
                to = f + dd
                while not to & 0x88:
                    q = B[to]
                    if not q:
                        if not cp:
                            A(f | to << 7)
                    else:
                        if (q < 7) != (p < 7):
                            A(f | to << 7)
                        break
                    to += dd
    return ms


def make(m):
    global ca, ep, t
    f = m & 127
    to = (m >> 7) & 127
    pr = (m >> 14) & 15
    p = B[f]
    c = B[to]
    ST.append((p, c, ca, ep, K[0], K[1]))
    B[to] = pr or p
    B[f] = 0
    e = -1
    if p == 1 and to == ep and not c:
        B[to - 16] = 0
    if p == 7 and to == ep and not c:
        B[to + 16] = 0
    if p == 1 and to - f == 32:
        e = f + 16
    if p == 7 and f - to == 32:
        e = f - 16
    if p == 6:
        ca &= ~3
        K[0] = to
        if to - f == 2:
            B[5] = 4
            B[7] = 0
        elif f - to == 2:
            B[3] = 4
            B[0] = 0
    if p == 12:
        ca &= ~12
        K[1] = to
        if to - f == 2:
            B[117] = 10
            B[119] = 0
        elif f - to == 2:
            B[115] = 10
            B[112] = 0
    if f == 7 or to == 7:
        ca &= ~1
    if f == 0 or to == 0:
        ca &= ~2
    if f == 119 or to == 119:
        ca &= ~4
    if f == 112 or to == 112:
        ca &= ~8
    ep = e
    t ^= 1


def unmake(m):
    global ca, ep, t
    p, c, ca0, ep0, wk, bk = ST.pop()
    f = m & 127
    to = (m >> 7) & 127
    if p == 6 and to - f == 2:
        B[7] = 4
        B[5] = 0
    elif p == 6 and f - to == 2:
        B[0] = 4
        B[3] = 0
    elif p == 12 and to - f == 2:
        B[119] = 10
        B[117] = 0
    elif p == 12 and f - to == 2:
        B[112] = 10
        B[115] = 0
    if (p == 1 or p == 7) and to == ep0 and not c:
        B[to - 16 if p == 1 else to + 16] = 7 if p == 1 else 1
    B[f] = p
    B[to] = c
    ca = ca0
    ep = ep0
    K[0] = wk
    K[1] = bk
    t ^= 1


def ev():
    s = 0
    ph = 0
    wn = 0
    bn = 0
    for q in ON:
        p = B[q]
        if p:
            w = p < 7
            i = (7 - (q >> 4)) * 8 + (q & 7) if w else (q >> 4) * 8 + (q & 7)
            v = V[p] + P[p - 1 if w else p - 7][i]
            s += v if w else -v
            ph += PH[p]
            if p == 3:
                wn += 1
            elif p == 9:
                bn += 1
    if wn > 1:
        s += 30
    if bn > 1:
        s -= 30
    f = 24 - ph
    if f > 0:
        q = K[0]
        i = (7 - (q >> 4)) * 8 + (q & 7)
        s += (KE[i] - P[5][i]) * f // 24
        q = K[1]
        i = (q >> 4) * 8 + (q & 7)
        s -= (KE[i] - P[5][i]) * f // 24
    s += 10 if t == 0 else -10
    return s if t == 0 else -s


def osc(m, pl, tm):
    if m == tm:
        return 1000000
    f = m & 127
    o = (m >> 7) & 127
    p = B[f]
    q = B[o]
    if q:
        return 10000 + V[q] * 10 - V[p] // 10
    if o == ep and (p == 1 or p == 7):
        return 10000 + 1000 - V[p] // 10
    if m == KILL[pl][0]:
        return 9000
    if m == KILL[pl][1]:
        return 8000
    return HIST[p][o]


def qs(a, be, pl):
    global ND
    ND += 1
    if ND > BG:
        raise Stop
    if att(K[t], (1 - t) == 0):
        for m in gen():
            make(m)
            if not att(K[1 - t], t == 0):
                unmake(m)
                break
            unmake(m)
        else:
            return -MA + pl
    s = ev()
    if s >= be:
        return be
    if s > a:
        a = s
    for m in gen(1):
        make(m)
        if att(K[1 - t], t == 0):
            unmake(m)
            continue
        try:
            v = -qs(-be, -a, pl + 1)
        except Stop:
            unmake(m)
            raise
        unmake(m)
        if v >= be:
            return be
        if v > a:
            a = v
    return a


def sr(a, be, d, pl):
    global ND, t, ep
    ND += 1
    if ND > BG:
        raise Stop
    if d <= 0:
        return qs(a, be, pl)
    chk = att(K[t], (1 - t) == 0)
    if chk:
        d += 1
    key = k()
    if key in R2:
        return 0
    e = TT.get(key)
    tm = 0
    if e and e[0] >= d:
        _, fl, v, tm = e
        if fl == 0:
            return v
        if fl == 1 and v > a:
            a = v
        elif fl == 2 and v < be:
            be = v
        if a >= be:
            return v
    if d >= 3 and not chk and ev() >= be and any(B[q] and (B[q] < 7) == (t == 0) and B[q] % 6 > 1 for q in ON):
        e0 = ep
        ep = -1
        t ^= 1
        try:
            v = -sr(-be, -be + 1, d - 3, pl + 1)
        except Stop:
            t ^= 1
            ep = e0
            raise
        t ^= 1
        ep = e0
        if v >= be:
            return be
    ms = []
    for m in gen():
        make(m)
        if att(K[1 - t], t == 0):
            unmake(m)
            continue
        ms.append(m)
        unmake(m)
    if not ms:
        return -MA + pl if chk else 0
    ms.sort(key=lambda m: osc(m, pl, tm), reverse=True)
    a0 = a
    bv = -INF
    bm = 0
    for i, m in enumerate(ms):
        f = m & 127
        o = (m >> 7) & 127
        p = B[f]
        cp = B[o] != 0 or (o == ep and (p == 1 or p == 7))
        make(m)
        try:
            if i >= 4 and d >= 3 and not chk and not cp:
                v = -sr(-be, -a, d - 2, pl + 1)
                if v > a:
                    v = -sr(-be, -a, d - 1, pl + 1)
            else:
                v = -sr(-be, -a, d - 1, pl + 1)
        except Stop:
            unmake(m)
            raise
        unmake(m)
        if v > bv:
            bv = v
            bm = m
        if v > a:
            a = v
        if a >= be:
            if not cp:
                if KILL[pl][0] != m:
                    KILL[pl][1] = KILL[pl][0]
                    KILL[pl][0] = m
                HIST[p][o] += d * d
            break
    TT[key] = (d, 2 if bv <= a0 else 1 if bv >= be else 0, bv, bm)
    return bv


def root(ms, d, first, bad, al=-INF, be=INF):
    a = al
    bv = -INF
    bm = first
    ms.sort(key=lambda m: osc(m, 0, first), reverse=True)
    for m in ms:
        make(m)
        try:
            v = -sr(-be, -a, d - 1, 1)
        except Stop:
            unmake(m)
            raise
        unmake(m)
        if m in bad:
            v = 0
        if v > bv:
            bv = v
            bm = m
        if v > a:
            a = v
    return bm, bv


def choose(ms, plies):
    global ND, BG, R2
    if len(TT) > 200000:
        TT.clear()
    BG = max(8000, 100000 - max(0, plies - 30) * 150)
    R2 = {x for x in REP if REP.count(x) > 1}
    bad = set()
    for m in ms:
        make(m)
        if REP.count(k()) >= 2:
            bad.add(m)
        unmake(m)
    bm = ms[0]
    ND = 0
    val = 0
    for d in range(1, 17):
        try:
            if d == 1:
                bm, val = root(ms, d, bm, bad)
            else:
                lo = val - 50
                hi = val + 50
                bm, val = root(ms, d, bm, bad, lo, hi)
                if val <= lo or val >= hi:
                    bm, val = root(ms, d, bm, bad)
        except Stop:
            break
    return bm


if __name__ == "__main__":
    while True:
        g = post("/game", {})
        if g["status"] == "done":
            break
        setup(g["fen"])
        REP.clear()
        REP.append(k())
        while g["status"] == "your_move":
            ms = [parse_uci(u) for u in g["legal_moves"]]
            mv = ms[0] if len(ms) == 1 else choose(ms, g["plies"])
            make(mv)
            REP.append(k())
            unmake(mv)
            g = post("/move", {"game": g["game"], "move": uci(mv)})
            if g["status"] == "your_move":
                setup(g["fen"])
                REP.append(k())
        print(f"game {g['game']}: {g.get('outcome')} by {g.get('reason')}", file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
