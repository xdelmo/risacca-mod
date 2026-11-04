-- Logica pura della mod Risacca: niente riferimenti a Isaac/Game, testabile fuori dal gioco.
local L = {}

L.TEXT = {
  GODOR = "IL GODOR!",
  MAXIMOR = "GODOR MAXIMOR!",
  XL_Q = "È XL?",
  XL_YES = "SÌ, È XL!",
  XL_NO = "No... non è XL",
  BEASTY = "IL BEASTY BOY",
  KUBRICK = "MEGA STANLEY KUBRICK",
  PIPPOLINS = "PIPPOLINS",
  BUMBAZZO = "BUMBAZZO",
  INTRO = "Ciao a tutti, io sono Risacca",
  INTRO_SUB = "Benvenuti sul mio canale",
  ANSIA = "C'ho l'ansia",
  TACCHINO = "Tacchino!",
  FACCIAZZA = "Alla facciazza vostra!",
  BACIONE = "Un bacione grande",
  BACIONE_SUB = "dal vostro Risacca",
  BEDUINS = "Beduins",
  RUBO = "Non vi rubo altro tempo",
  RUBO_DOPO = "3, 2, 1... Ah no, aspetta",
  STARE = "Potrebbe stare qua!",
  PRIVI = "Che fai? Te ne privi?",
  GENNARO = "Il miracolo",
  GENNARO_SUB = "di San Gennaruzzo!",
  PRO = "La mossa del pro player!",
  CRETINO = "Sono un cretino",
  NON_MUORE = "Non muore!",
  SOGNARE = "Fammi sognare",
  TROLLATA = "M'ha trollato!",
  MANNAGGIA = "Mannaggia a lui!",
  IDIOTA = "Sono un idiota!",
  FERMI = "Fermi tutti!",
}

-- Descrizioni per External Item Descriptions: "#" va a capo, {{...}} sono le icone di EID.
L.EID = {
  ROTTO = "Fa comparire accanto a te un oggetto glitchato",
  DEADGOD = "Ogni boss sconfitto dà, fino a un massimo di 10 boss:#↑ {{Damage}} +0.2 Danni#↑ {{Speed}} +0.03 Velocità#↑ {{Range}} +0.1 Gittata#↑ {{Tears}} -0.1 ritardo di tiro#Conta al massimo un boss per stanza",
  STREAK = "↑ {{Damage}} +0.5 Danni per ogni piano di fila finito senza essere colpito#Se vieni colpito la serie si azzera e il bonus sparisce al piano successivo",
  RUBO = "Congela tutti i nemici della stanza per 3 secondi",
  STARE = "A ogni nuovo piano:#{{SecretRoom}} {{SuperSecretRoom}} mostra le stanze segrete sulla mappa#{{Bomb}} +2 bombe",
  PRIVI = "25% di probabilità di un pickup in più quando finisci una stanza:#{{Coin}} moneta, {{Bomb}} bomba, {{Key}} chiave o {{Heart}} cuore",
  PRO = "↑ {{Damage}} +2 Danni per la stanza#Se ti colpiscono perdi il bonus",
  GENNARO = "{{AngelRoom}} +25% di probabilità di una stanza dell'angelo a ogni nuovo piano#{{EternalHeart}} Un cuore eterno alla prima visita di ogni stanza dell'angelo",
  TROLLATA = "Fa comparire una troll bomb addosso a ogni nemico della stanza#Se ti trovi vicino esplode anche su di te",
  FAICOSI = "Ogni seconda lacrima parte doppia",
  MANNAGGIA = "Quando vieni colpito, il nemico più vicino subisce 10 volte il tuo danno",
  IDIOTA = "Non fa niente",
  FERMI = "Non fa niente",
}

L.PRIO = { XL = 1, INTRO = 1, PICKUP = 2, TACCHINO = 2, ITEM = 2, ANSIA = 3, BOSSNAME = 3, BACIONE = 4, BEDUINS = 5, CRETINO = 3, NON_MUORE = 2, MANNAGGIA = 3 }

L.RUBO_FRAMES = 90 -- 3 secondi a 30 update al secondo
L.STARE_BOMBS = 2
L.GENNARO_ANGEL_CHANCE = 0.25
L.PRO_DAMAGE = 2
L.NON_MUORE_FRAMES = 1800 -- 60 secondi a 30 update al secondo
L.MANNAGGIA_MULT = 10

function L.nonMuore(roomFrames, aliveBosses)
  return aliveBosses > 0 and roomFrames >= L.NON_MUORE_FRAMES
end

-- roll in [0, 1), multiplier = GetTrinketMultiplier sommato sui player
function L.priviProcs(roll, multiplier)
  return roll < 0.25 * multiplier
end

function L.pickupText(quality, devilDeal)
  if devilDeal then return L.TEXT.FACCIAZZA end
  if quality >= 4 then return L.TEXT.MAXIMOR end
  if quality == 3 then return L.TEXT.GODOR end
  return nil
end

function L.xlText(isXL)
  return L.TEXT.XL_Q, isXL and L.TEXT.XL_YES or L.TEXT.XL_NO
end

-- halfHearts = mezzi cuori totali (rossi + soul/black). Ritorna fire, armed.
function L.ansia(armed, halfHearts)
  if halfHearts > 1 then return false, true end
  if armed then return true, false end
  return false, armed
end

function L.isDevilPrice(price)
  return price < 0 and price ~= -1000 -- -1000 = PickupPrice.PRICE_FREE
end

-- [type] = true (qualsiasi variant) oppure { [variant] = true }
local FINAL = {
  [273] = true,              -- The Lamb
  [102] = { [0] = true, [1] = true }, -- Isaac, ???
  [275] = true,              -- Mega Satan 2
  [412] = true,              -- Delirium
  [912] = { [0] = true },    -- Mother
  [951] = { [0] = true },    -- The Beast
  [407] = true,              -- Hush
  [84] = true,               -- Satan
  [406] = { [1] = true },    -- Ultra Greedier
}

function L.isFinalBoss(etype, variant)
  local f = FINAL[etype]
  if f == true then return true end
  return f ~= nil and f[variant] == true
end

function L.streakOnNewLevel(streak, hitThisFloor)
  if hitThisFloor then return 0 end
  return streak + 1
end

function L.deadGodBonus(kills)
  local k = math.min(kills, 10)
  return { damage = 0.2 * k, speed = 0.03 * k, range = 4 * k, fireDelay = -0.1 * k }
end

local SUPPRESS_WINDOW = 15
L.REPEAT_COOLDOWN = 900 -- la stessa scritta non torna prima di 30 secondi (30 update al secondo)

function L.newQueue()
  local q = { items = {}, seq = 0, now = 0, last = {} }

  function q:push(title, sub, delay, prio)
    self.seq = self.seq + 1
    self.items[#self.items + 1] = { title = title, sub = sub, left = delay, prio = prio, seq = self.seq }
  end

  function q:tick()
    self.now = self.now + 1
    local best
    for _, it in ipairs(self.items) do
      local last = self.last[it.title]
      local fresh = not last or self.now - last >= L.REPEAT_COOLDOWN
      if it.left <= 0 and fresh and (not best or it.prio > best.prio or (it.prio == best.prio and it.seq < best.seq)) then
        best = it
      end
    end
    local keep = {}
    for _, it in ipairs(self.items) do
      local drop = it.left <= 0 or (best and it.prio < best.prio and it.left <= SUPPRESS_WINDOW)
      if not drop then
        it.left = it.left - 1
        keep[#keep + 1] = it
      end
    end
    self.items = keep
    if best then
      self.last[best.title] = self.now
      return best.title, best.sub
    end
    return nil
  end

  return q
end

return L
