-- Smoke test: carica main.lua con un'API Isaac finta e simula scenari di gioco.
-- Uso (dalla cartella della mod): lua tests/smoke.lua

local cbs, called, shown, saved = {}, {}, {}, nil

-- enum finti: ogni chiave nuova riceve un numero distinto
local nextId = 10000
local function enum()
  return setmetatable({}, { __index = function(t, k) nextId = nextId + 1; rawset(t, k, nextId); return nextId end })
end
ModCallbacks, EntityType, PickupVariant, CacheFlag, LevelCurse, CollectibleType = enum(), enum(), enum(), enum(), enum(), enum()
RoomType, HeartSubType = enum(), enum()
function EntityRef(e) return { Entity = e } end

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

local items, trinkets = {}, {}
local player = {
  hash = 1, Position = Vector(0, 0), Damage = 3.5, MoveSpeed = 1, TearRange = 260, MaxFireDelay = 10,
  hearts = 6, soul = 0, dead = false, QueuedItem = { Item = nil }, bombs = 0,
}
function player:HasCollectible(id) return items[id] == true end
function player:GetCollectibleNum(id) return items[id] and 1 or 0 end
function player:HasTrinket(id) return trinkets[id] == true end
function player:GetTrinketMultiplier(id) return trinkets[id] and 1 or 0 end
function player:AddBombs(n) self.bombs = self.bombs + n end
function player:AddCollectible(id) items[id] = true end
function player:RemoveCollectible(id) items[id] = nil end
function player:AddCacheFlags() end
local evaluations = 0
function player:EvaluateItems() evaluations = evaluations + 1 end
function player:GetHearts() return self.hearts end
function player:GetSoulHearts() return self.soul end
function player:IsDead() return self.dead end
function player:ToPlayer() return self end

local ids = {
  ["Ho Rotto il Gioco"] = 733, ["-1 al Dead God"] = 734, ["Win Streak"] = 190,
  ["Non Vi Rubo Altro Tempo"] = 735, ["Potrebbe Stare Qua"] = 736, ["Il Miracolo di San Gennaruzzo"] = 737,
  ["Che Fai, Te Ne Privi?"] = 191,
}
local spawned, lastSpawn = 0, nil
local roomEntities = {}
Isaac = {
  GetItemIdByName = function(n) return ids[n] end,
  GetTrinketIdByName = function(n) return ids[n] end,
  GetPlayer = function() return player end,
  Spawn = function(t, v, s) spawned = spawned + 1; lastSpawn = { t = t, v = v, s = s } end,
  GetFreeNearPosition = function(p) return p end,
  GetRoomEntities = function() return roomEntities end,
}
local hud = { ShowItemText = function(_, t, s) shown[#shown + 1] = s ~= "" and (t .. " / " .. s) or t end }
local level = { blueMap = 0, visibility = 0, angelChance = 0 }
function level.GetCurses() return 0 end
function level:ApplyBlueMapEffect() self.blueMap = self.blueMap + 1 end
function level:UpdateVisibility() self.visibility = self.visibility + 1 end
function level:AddAngelRoomChance(c) self.angelChance = self.angelChance + c end
local room = { kind = RoomType.ROOM_DEFAULT, first = true }
function room:GetType() return self.kind end
function room:IsFirstVisit() return self.first end
function room:GetCenterPos() return Vector(0, 0) end
function Game()
  return { GetNumPlayers = function() return 1 end, GetHUD = function() return hud end,
           GetLevel = function() return level end, GetRoom = function() return room end }
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
for _, id in pairs(ids) do assert(eid[id], "descrizione EID mancante: " .. id) end

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
expect({ "Beduins" })

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

-- Non Vi Rubo Altro Tempo: congela solo i nemici vulnerabili, poi il falso via
local function entity(vulnerable)
  return { IsVulnerableEnemy = function() return vulnerable end,
           AddFreeze = function(self, ref, d) assert(ref.Entity == player); self.frozen = d end }
end
local enemy, rock = entity(true), entity(false)
roomEntities = { enemy, rock }
assert(fire(ModCallbacks.MC_USE_ITEM, 735, 735, nil, player) == true, "USE_ITEM deve ritornare true")
assert(enemy.frozen == 90 and rock.frozen == nil, "congelamento errato")
frames(60)
expect({ "Non vi rubo altro tempo", "3, 2, 1... Ah no, aspetta" })

-- Potrebbe Stare Qua: mappa e bombe a ogni piano
fire(ModCallbacks.MC_POST_NEW_LEVEL)
assert(level.blueMap == 0 and player.bombs == 0, "effetto senza l'oggetto")
frames(100); shown = {}
items[736] = true
fire(ModCallbacks.MC_POST_NEW_LEVEL)
assert(level.blueMap == 1 and level.visibility == 1 and player.bombs == 2, "Potrebbe Stare Qua errato")
frames(100); shown = {}

-- scritta solo alla prima visita di una secret
room.kind = RoomType.ROOM_SUPERSECRET
fire(ModCallbacks.MC_POST_NEW_ROOM); frames(5)
expect({ "Potrebbe stare qua!" })
room.first = false
fire(ModCallbacks.MC_POST_NEW_ROOM); frames(20)
expect({})

-- Il Miracolo di San Gennaruzzo: stanza dell'angelo più probabile, cuore eterno alla prima visita
assert(level.angelChance == 0, "effetto senza l'oggetto")
items[737] = true
fire(ModCallbacks.MC_POST_NEW_LEVEL)
assert(level.angelChance == 0.25, "probabilità angelo errata: " .. level.angelChance)
frames(100); shown = {}
local spawnedBefore = spawned
room.kind = RoomType.ROOM_ANGEL
fire(ModCallbacks.MC_POST_NEW_ROOM); frames(20)
assert(spawned == spawnedBefore, "cuore eterno anche fuori dalla prima visita")
expect({})
room.first = true
fire(ModCallbacks.MC_POST_NEW_ROOM); frames(5)
assert(spawned == spawnedBefore + 1 and lastSpawn.s == HeartSubType.HEART_ETERNAL, "cuore eterno mancante")
expect({ "Il miracolo / di San Gennaruzzo!" })

-- Che Fai, Te Ne Privi?: un pickup in più solo se il tiro riesce e il trinket c'è
room.kind = RoomType.ROOM_DEFAULT
local function rng(roll)
  return { RandomFloat = function() return roll end, RandomInt = function() return 1 end }
end
spawnedBefore = spawned
fire(ModCallbacks.MC_PRE_SPAWN_CLEAN_AWARD, nil, rng(0.1), Vector(0, 0)); frames(20)
assert(spawned == spawnedBefore, "pickup senza il trinket")
trinkets[191] = true
fire(ModCallbacks.MC_PRE_SPAWN_CLEAN_AWARD, nil, rng(0.9), Vector(0, 0)); frames(20)
assert(spawned == spawnedBefore, "pickup con tiro fallito")
expect({})
fire(ModCallbacks.MC_PRE_SPAWN_CLEAN_AWARD, nil, rng(0.1), Vector(0, 0)); frames(5)
assert(spawned == spawnedBefore + 1 and lastSpawn.v == PickupVariant.PICKUP_BOMB, "pickup errato")
expect({ "Che fai? Te ne privi?" })

-- ogni callback registrata deve essere stata chiamata almeno una volta
for i, c in ipairs(cbs) do assert(called[c], "callback #" .. i .. " mai chiamata") end
expect({})
print("SMOKE OK")
