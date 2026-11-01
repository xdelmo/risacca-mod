-- Smoke test: carica main.lua con un'API Isaac finta e simula scenari di gioco.
-- Uso (dalla cartella della mod): lua tests/smoke.lua

local cbs, called, shown, saved = {}, {}, {}, nil

-- enum finti: ogni chiave nuova riceve un numero distinto
local nextId = 10000
local function enum()
  return setmetatable({}, { __index = function(t, k) nextId = nextId + 1; rawset(t, k, nextId); return nextId end })
end
ModCallbacks, EntityType, PickupVariant, CacheFlag, LevelCurse, CollectibleType = enum(), enum(), enum(), enum(), enum(), enum()

Vector = setmetatable({ Zero = { X = 0, Y = 0 } }, { __call = function(_, x, y) return { X = x, Y = y } end })
function GetPtrHash(e) return e.hash end
function include(name) return dofile(name .. ".lua") end
package.preload["json"] = function()
  return { encode = function(t) local s = {} for k, v in pairs(t) do s[#s + 1] = k .. "=" .. tostring(v) end return table.concat(s, ";") end,
           decode = function() return { deadGodKills = 1 } end }
end

function RegisterMod(name)
  local m = { Name = name }
  function m:AddCallback(id, fn, filter) cbs[#cbs + 1] = { id = id, fn = fn, filter = filter } end
  function m:SaveData(s) saved = s end
  function m:HasData() return saved ~= nil end
  function m:LoadData() return saved end
  return m
end

local items = {}
local player = {
  hash = 1, Position = Vector(0, 0), Damage = 3.5, MoveSpeed = 1, TearRange = 260, MaxFireDelay = 10,
  hearts = 6, soul = 0, dead = false, QueuedItem = { Item = nil },
}
function player:HasCollectible(id) return items[id] == true end
function player:GetCollectibleNum(id) return items[id] and 1 or 0 end
function player:HasTrinket() return false end
function player:GetTrinketMultiplier() return 1 end
function player:AddCollectible(id) items[id] = true end
function player:RemoveCollectible(id) items[id] = nil end
function player:AddCacheFlags() end
local evaluations = 0
function player:EvaluateItems() evaluations = evaluations + 1 end
function player:GetHearts() return self.hearts end
function player:GetSoulHearts() return self.soul end
function player:IsDead() return self.dead end
function player:ToPlayer() return self end

local ids = { ["Ho Rotto il Gioco"] = 733, ["-1 al Dead God"] = 734, ["Win Streak"] = 190 }
local spawned = 0
Isaac = {
  GetItemIdByName = function(n) return ids[n] end,
  GetTrinketIdByName = function(n) return ids[n] end,
  GetPlayer = function() return player end,
  Spawn = function() spawned = spawned + 1 end,
  GetFreeNearPosition = function(p) return p end,
}
local hud = { ShowItemText = function(_, t, s) shown[#shown + 1] = s ~= "" and (t .. " / " .. s) or t end }
local level = { GetCurses = function() return 0 end }
function Game()
  return { GetNumPlayers = function() return 1 end, GetHUD = function() return hud end, GetLevel = function() return level end }
end

local mod_ = nil
local function fire(id, key, ...)
  local ret
  for _, c in ipairs(cbs) do
    if c.id == id and (c.filter == nil or c.filter == key) then
      called[c] = true
      local r = c.fn(mod_, ...)
      if r ~= nil then ret = r end
    end
  end
  return ret
end

-- External Item Descriptions finto: registra le descrizioni ricevute
local eid = {}
EID = {
  setModIndicatorName = function() end,
  addCollectible = function(_, id, text) eid[id] = text end,
  addTrinket = function(_, id, text) eid[id] = text end,
}

dofile("main.lua")
assert(#cbs > 0, "nessuna callback registrata")
assert(eid[733] and eid[734] and eid[190], "descrizioni EID mancanti")

local function frames(n)
  for _ = 1, n do
    fire(ModCallbacks.MC_POST_PLAYER_UPDATE, nil, player)
    fire(ModCallbacks.MC_POST_UPDATE)
  end
end
local function collectible(id, q) return { ID = id, Quality = q, IsCollectible = function() return true end } end
local function npc(t, v) return { Type = t, Variant = v, IsBoss = function() return true end } end
local function expect(want)
  local got = table.concat(shown, " | ")
  assert(got == table.concat(want, " | "), "\natteso: " .. table.concat(want, " | ") .. "\nottenuto: " .. got)
  shown = {}
end

-- nuova run: intro, poi "È XL?"
fire(ModCallbacks.MC_POST_GAME_STARTED, nil, false)
fire(ModCallbacks.MC_POST_NEW_LEVEL)
fire(ModCallbacks.MC_POST_NEW_ROOM)
frames(100)
expect({ "Ciao a tutti, io sono Risacca / Benvenuti sul mio canale", "È XL? / No... non è XL" })

-- raccolta oggetto Q4 → MAXIMOR
player.QueuedItem.Item = collectible(331, 4); frames(60)
player.QueuedItem.Item = nil; frames(5)
expect({ "GODOR MAXIMOR!" })

-- patto col diavolo → Facciazza
fire(ModCallbacks.MC_PRE_PICKUP_COLLISION, PickupVariant.PICKUP_COLLECTIBLE, { Price = -1, SubType = 50 }, player)
player.QueuedItem.Item = collectible(50, 1); frames(60)
player.QueuedItem.Item = nil; frames(5)
expect({ "Alla facciazza vostra!" })

-- colpo da 2 che porta a mezzo cuore → solo l'ansia
fire(ModCallbacks.MC_ENTITY_TAKE_DMG, EntityType.ENTITY_PLAYER, player, 2)
player.hearts = 1; frames(60)
expect({ "C'ho l'ansia" })

-- Beast: scritta una volta sola per run
fire(ModCallbacks.MC_POST_NPC_INIT, nil, npc(EntityType.ENTITY_BEAST, 0))
fire(ModCallbacks.MC_POST_NPC_INIT, nil, npc(EntityType.ENTITY_BEAST, 0))
frames(40)
expect({ "IL BEASTY BOY" })

-- Satan ucciso due volte nella stessa stanza → un solo bacione
fire(ModCallbacks.MC_POST_NEW_ROOM)
fire(ModCallbacks.MC_POST_NPC_DEATH, nil, npc(84, 0))
frames(40)
fire(ModCallbacks.MC_POST_NPC_DEATH, nil, npc(84, 0)) -- seconda fase, più tardi
frames(40)
expect({ "Un bacione grande / dal vostro Risacca" })

-- morte → tacchinardo
player.hearts = 0; player.dead = true; frames(30)
expect({ "Calmati tacchinardo" })

-- oggetti: Ho Rotto il Gioco e -1 al Dead God
assert(fire(ModCallbacks.MC_USE_ITEM, 733, 733, nil, player) == true, "USE_ITEM deve ritornare true")
assert(spawned == 1 and not items[CollectibleType.COLLECTIBLE_TMTRAINER], "TMTRAINER non rimosso")
items[734] = true
fire(ModCallbacks.MC_POST_NEW_ROOM)
fire(ModCallbacks.MC_POST_NPC_DEATH, nil, npc(20, 0))
local before = player.Damage
fire(ModCallbacks.MC_EVALUATE_CACHE, nil, player, CacheFlag.CACHE_DAMAGE)
assert(math.abs(player.Damage - before - 0.2) < 1e-9, "bonus Dead God errato: " .. (player.Damage - before))
fire(ModCallbacks.MC_PRE_GAME_EXIT)
assert(saved and saved:find("deadGodKills=1"), "salvataggio mancante: " .. tostring(saved))

-- Continua: dopo aver caricato il salvataggio le statistiche vanno ricalcolate
evaluations = 0
fire(ModCallbacks.MC_POST_GAME_STARTED, nil, true)
assert(evaluations > 0, "statistiche non ricalcolate dopo il Continua")

-- ogni callback registrata deve essere stata chiamata almeno una volta
for i, c in ipairs(cbs) do assert(called[c], "callback #" .. i .. " mai chiamata") end
expect({})
print("SMOKE OK")
