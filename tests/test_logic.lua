local L = dofile("logic.lua")

local function near(a, b) return math.abs(a - b) < 1e-9 end

-- pickupText
assert(L.pickupText(4, false) == "GODOR MAXIMOR!")
assert(L.pickupText(3, false) == "IL GODOR!")
assert(L.pickupText(2, false) == nil)
assert(L.pickupText(1, true) == "Alla facciazza vostra!")
assert(L.pickupText(4, true) == "Alla facciazza vostra!")

-- priviProcs
assert(L.priviProcs(0.24, 1) and not L.priviProcs(0.25, 1))
assert(L.priviProcs(0.49, 2) and not L.priviProcs(0.5, 2))
assert(not L.priviProcs(0, 0))

-- xlText
local t, s = L.xlText(true)
assert(t == "È XL?" and s == "SÌ, È XL!")
t, s = L.xlText(false)
assert(t == "È XL?" and s == "No... non è XL")

-- ansia_lost: mai armato (The Lost, 0-1 mezzi cuori fissi) → non scatta mai
local armed, fire = false
for _, hh in ipairs({0, 1, 0, 1, 1}) do
  fire, armed = L.ansia(armed, hh)
  assert(fire == false)
end

-- ansia: scatta una volta, si riarma sopra mezzo cuore
armed = true
fire, armed = L.ansia(armed, 1); assert(fire == true and armed == false)
fire, armed = L.ansia(armed, 1); assert(fire == false)
fire, armed = L.ansia(armed, 4); assert(fire == false and armed == true)
fire, armed = L.ansia(armed, 1); assert(fire == true)

-- isDevilPrice
assert(L.isDevilPrice(-1) and L.isDevilPrice(-3))
assert(not L.isDevilPrice(-1000) and not L.isDevilPrice(0) and not L.isDevilPrice(15))

-- isFinalBoss
assert(L.isFinalBoss(273, 0) and L.isFinalBoss(102, 1) and L.isFinalBoss(951, 0))
assert(not L.isFinalBoss(951, 10) and not L.isFinalBoss(45, 0))

-- streak
assert(L.streakOnNewLevel(2, false) == 3)
assert(L.streakOnNewLevel(5, true) == 0)

-- deadGodBonus
local b = L.deadGodBonus(3)
assert(near(b.damage, 0.6) and near(b.speed, 0.09) and near(b.range, 12) and near(b.fireDelay, -0.3))
assert(near(L.deadGodBonus(15).damage, 2.0))

-- queue_suppresses_lower
local q = L.newQueue()
q:push(L.TEXT.TACCHINO, nil, 2, L.PRIO.TACCHINO)
q:push(L.TEXT.ANSIA, nil, 0, L.PRIO.ANSIA)
assert(q:tick() == L.TEXT.ANSIA)
for _ = 1, 30 do assert(q:tick() == nil) end

-- queue delay
q = L.newQueue()
q:push("A", nil, 3, 1)
for _ = 1, 3 do assert(q:tick() == nil) end
assert(q:tick() == "A")
assert(q:tick() == nil)

-- queue: priorità più bassa lontana (>15 frame) sopravvive
q = L.newQueue()
q:push("FAR", nil, 40, 1)
q:push("NOW", nil, 0, 5)
assert(q:tick() == "NOW")
local got
for _ = 1, 45 do got = q:tick() or got end
assert(got == "FAR")

print("OK")
