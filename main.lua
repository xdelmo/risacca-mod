local mod = RegisterMod("Risacca", 1)
local L = include("logic")
local json = require("json")
local game = Game()

local ITEM_ROTTO = Isaac.GetItemIdByName("Ho Rotto il Gioco")
local ITEM_DEADGOD = Isaac.GetItemIdByName("-1 al Dead God")
local TRINKET_STREAK = Isaac.GetTrinketIdByName("Win Streak")
local ITEM_RUBO = Isaac.GetItemIdByName("Non Vi Rubo Altro Tempo")
local ITEM_STARE = Isaac.GetItemIdByName("Potrebbe Stare Qua")
local ITEM_GENNARO = Isaac.GetItemIdByName("Il Miracolo di San Gennaruzzo")
local TRINKET_PRIVI = Isaac.GetTrinketIdByName("Che Fai, Te Ne Privi?")
local ITEM_PRO = Isaac.GetItemIdByName("La Mossa del Pro Player")
local ITEM_TROLLATA = Isaac.GetItemIdByName("La Trollata")
local ITEM_FAICOSI = Isaac.GetItemIdByName("Fai Così, Fai Così")
local TRINKET_MANNAGGIA = Isaac.GetTrinketIdByName("Mannaggia a Lui")
local TACCHINO_ITEMS = {
  Isaac.GetItemIdByName("Tacchinardi"),
  Isaac.GetItemIdByName("Tacchinibus"),
  Isaac.GetItemIdByName("Il Tacchino della Domenica"),
}
local ITEM_IDIOTA = Isaac.GetItemIdByName("Sono un Idiota")
local ITEM_FERMI = Isaac.GetItemIdByName("Fermi Tutti")

-- Descrizioni per External Item Descriptions, solo se l'altra mod è attiva
if EID then
  EID:setModIndicatorName("Risacca Mod")
  EID:addCollectible(ITEM_ROTTO, L.EID.ROTTO)
  EID:addCollectible(ITEM_DEADGOD, L.EID.DEADGOD)
  EID:addTrinket(TRINKET_STREAK, L.EID.STREAK)
  EID:addCollectible(ITEM_RUBO, L.EID.RUBO)
  EID:addCollectible(ITEM_STARE, L.EID.STARE)
  EID:addCollectible(ITEM_GENNARO, L.EID.GENNARO)
  EID:addTrinket(TRINKET_PRIVI, L.EID.PRIVI)
  EID:addCollectible(ITEM_PRO, L.EID.PRO)
  EID:addCollectible(ITEM_TROLLATA, L.EID.TROLLATA)
  EID:addCollectible(ITEM_FAICOSI, L.EID.FAICOSI)
  EID:addTrinket(TRINKET_MANNAGGIA, L.EID.MANNAGGIA)
  EID:addCollectible(TACCHINO_ITEMS[1], L.EID.TACCHINARDI)
  EID:addCollectible(TACCHINO_ITEMS[2], L.EID.TACCHINIBUS)
  EID:addCollectible(TACCHINO_ITEMS[3], L.EID.DOMENICA)
  EID:addCollectible(ITEM_IDIOTA, L.EID.IDIOTA)
  EID:addCollectible(ITEM_FERMI, L.EID.FERMI)
end

local function freshRun() return { streak = 0, hitThisFloor = false, deadGodKills = 0, beastyShown = false, kubrickShown = false, pippolinsShown = false, bumbazzoShown = false, tacchinoShown = false } end
local run = freshRun()
local roomFlags = {}

local function save() mod:SaveData(json.encode(run)) end

local function players()
  local t = {}
  for i = 0, game:GetNumPlayers() - 1 do t[#t + 1] = Isaac.GetPlayer(i) end
  return t
end

local function anyHas(check)
  for _, p in ipairs(players()) do if check(p) then return true end end
  return false
end

local function refresh(flags)
  for _, p in ipairs(players()) do
    p:AddCacheFlags(flags)
    p:EvaluateItems()
  end
end

mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, function(_, isContinued)
  run = freshRun()
  if isContinued and mod:HasData() then
    local ok, data = pcall(json.decode, mod:LoadData())
    if ok and type(data) == "table" then
      for k in pairs(run) do if data[k] ~= nil then run[k] = data[k] end end
    end
    -- il gioco calcola le statistiche prima di questa callback, quando i bonus erano ancora a zero
    refresh(CacheFlag.CACHE_ALL)
  end
  save()
end)

mod:AddCallback(ModCallbacks.MC_PRE_GAME_EXIT, function() save() end)
mod:AddCallback(ModCallbacks.MC_POST_NEW_ROOM, function() roomFlags = {} end)

-- Ho Rotto il Gioco: piedistallo glitchato col trucco TMTRAINER
mod:AddCallback(ModCallbacks.MC_USE_ITEM, function(_, _, _, player)
  local TM = CollectibleType.COLLECTIBLE_TMTRAINER
  local hadTM = player:HasCollectible(TM)
  if not hadTM then player:AddCollectible(TM, 0, false) end
  Isaac.Spawn(EntityType.ENTITY_PICKUP, PickupVariant.PICKUP_COLLECTIBLE, 0,
    Isaac.GetFreeNearPosition(player.Position, 40), Vector.Zero, nil)
  if not hadTM then player:RemoveCollectible(TM) end
  return true
end, ITEM_ROTTO)

-- Win Streak
mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, function()
  run.streak = 0
  run.hitThisFloor = true
end, EntityType.ENTITY_PLAYER)

mod:AddCallback(ModCallbacks.MC_POST_NEW_LEVEL, function()
  if anyHas(function(p) return p:HasTrinket(TRINKET_STREAK) end) then
    run.streak = L.streakOnNewLevel(run.streak, run.hitThisFloor)
  end
  run.hitThisFloor = false
  refresh(CacheFlag.CACHE_DAMAGE)
  save()
end)

-- -1 al Dead God
mod:AddCallback(ModCallbacks.MC_POST_NPC_DEATH, function(_, npc)
  if not npc:IsBoss() or roomFlags.deadGod then return end
  if not anyHas(function(p) return p:HasCollectible(ITEM_DEADGOD) end) then return end
  roomFlags.deadGod = true
  run.deadGodKills = run.deadGodKills + 1
  refresh(CacheFlag.CACHE_ALL)
  save()
end)

mod:AddCallback(ModCallbacks.MC_EVALUATE_CACHE, function(_, player, flag)
  if flag == CacheFlag.CACHE_DAMAGE and player:HasTrinket(TRINKET_STREAK) then
    player.Damage = player.Damage + 0.5 * run.streak * player:GetTrinketMultiplier(TRINKET_STREAK)
  end
  local n = player:GetCollectibleNum(ITEM_DEADGOD)
  if n == 0 then return end
  local b = L.deadGodBonus(run.deadGodKills)
  if flag == CacheFlag.CACHE_DAMAGE then player.Damage = player.Damage + b.damage * n
  elseif flag == CacheFlag.CACHE_SPEED then player.MoveSpeed = player.MoveSpeed + b.speed * n
  elseif flag == CacheFlag.CACHE_RANGE then player.TearRange = player.TearRange + b.range * n
  elseif flag == CacheFlag.CACHE_FIREDELAY then player.MaxFireDelay = player.MaxFireDelay + b.fireDelay * n
  end
end)

-- ===== Scritte a schermo =====
local T, P = L.TEXT, L.PRIO
local q = L.newQueue()
local function say(t, s, delay, prio) q:push(t, s, delay, prio) end

mod:AddCallback(ModCallbacks.MC_POST_UPDATE, function()
  local t, s = q:tick()
  if t then game:GetHUD():ShowItemText(t, s or "") end
end)

mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, function(_, isContinued)
  if not isContinued then say(T.INTRO, T.INTRO_SUB, 30, P.INTRO) end
end)

mod:AddCallback(ModCallbacks.MC_POST_NEW_LEVEL, function()
  local isXL = (game:GetLevel():GetCurses() & LevelCurse.CURSE_OF_LABYRINTH) ~= 0
  local t, s = L.xlText(isXL)
  say(t, s, 90, P.XL)
end)

-- stato per player, chiave GetPtrHash(player)
local devilPending, prevQueued, armed, wasDead = {}, {}, {}, {}

mod:AddCallback(ModCallbacks.MC_PRE_PICKUP_COLLISION, function(_, pickup, collider)
  local player = collider:ToPlayer()
  if player and L.isDevilPrice(pickup.Price) then
    devilPending[GetPtrHash(player)] = pickup.SubType
  end
end, PickupVariant.PICKUP_COLLECTIBLE)

mod:AddCallback(ModCallbacks.MC_POST_PLAYER_UPDATE, function(_, player)
  local idx = GetPtrHash(player)

  local qi = player.QueuedItem.Item
  if qi and not prevQueued[idx] and qi:IsCollectible() then
    -- gli oggetti inutili non fanno niente: solo la scritta quando li raccogli
    local useless = { [ITEM_IDIOTA] = L.TEXT.IDIOTA, [ITEM_FERMI] = L.TEXT.FERMI }
    local t = useless[qi.ID] or L.pickupText(qi.Quality, devilPending[idx] == qi.ID)
    devilPending[idx] = nil
    if t then say(t, nil, 45, P.PICKUP) end
  end
  prevQueued[idx] = qi ~= nil

  local half = player:GetHearts() + player:GetSoulHearts()
  if armed[idx] == nil then armed[idx] = half > 1 end
  local fire
  fire, armed[idx] = L.ansia(armed[idx], half)
  if fire then say(T.ANSIA, nil, 0, P.ANSIA) end

  local dead = player:IsDead()
  if dead and not wasDead[idx] then say(T.BEDUINS, nil, 0, P.BEDUINS) end
  wasDead[idx] = dead
end)

mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, function(_, _, amount)
  if amount >= 2 and not roomFlags.tacchino then
    roomFlags.tacchino = true
    say(T.TACCHINO, nil, 2, P.TACCHINO)
  end
end, EntityType.ENTITY_PLAYER)

mod:AddCallback(ModCallbacks.MC_POST_NPC_INIT, function(_, npc)
  if npc.Variant ~= 0 then return end
  if npc.Type == EntityType.ENTITY_BEAST and not run.beastyShown then
    run.beastyShown = true
    say(T.BEASTY, nil, 30, P.BOSSNAME)
    save()
  elseif npc.Type == EntityType.ENTITY_MEGA_SATAN and not run.kubrickShown then
    run.kubrickShown = true
    say(T.KUBRICK, nil, 30, P.BOSSNAME)
    save()
  elseif npc.Type == EntityType.ENTITY_PEEP and not run.pippolinsShown then -- variant 1 è The Bloat
    run.pippolinsShown = true
    say(T.PIPPOLINS, nil, 30, P.BOSSNAME)
    save()
  elseif npc.Type == EntityType.ENTITY_BUMBINO and not run.bumbazzoShown then
    run.bumbazzoShown = true
    say(T.BUMBAZZO, nil, 30, P.BOSSNAME)
    save()
  end
end)

mod:AddCallback(ModCallbacks.MC_POST_NPC_DEATH, function(_, npc)
  if L.isFinalBoss(npc.Type, npc.Variant) and not roomFlags.bacione then
    roomFlags.bacione = true
    say(T.BACIONE, T.BACIONE_SUB, 30, P.BACIONE)
  end
end)

mod:AddCallback(ModCallbacks.MC_POST_UPDATE, function()
  if roomFlags.nonMuore then return end
  local room = game:GetRoom()
  if L.nonMuore(room:GetFrameCount(), room:GetAliveBossesCount()) then
    roomFlags.nonMuore = true
    say(T.NON_MUORE, nil, 0, P.NON_MUORE)
  end
end)

-- Fammi sognare: niente return, altrimenti si altera l'uso del D6
mod:AddCallback(ModCallbacks.MC_USE_ITEM, function()
  say(T.SOGNARE, nil, 0, P.ITEM)
end, CollectibleType.COLLECTIBLE_D6)

-- ===== Oggetti dei tormentoni: effetto più scritta =====

-- Non Vi Rubo Altro Tempo
mod:AddCallback(ModCallbacks.MC_USE_ITEM, function(_, _, _, player)
  for _, e in ipairs(Isaac.GetRoomEntities()) do
    if e:IsVulnerableEnemy() then e:AddFreeze(EntityRef(player), L.RUBO_FRAMES) end
  end
  say(T.RUBO, nil, 0, P.ITEM)
  say(T.RUBO_DOPO, nil, 45, P.ITEM)
  return true
end, ITEM_RUBO)

mod:AddCallback(ModCallbacks.MC_POST_NEW_LEVEL, function()
  local level = game:GetLevel()
  -- Potrebbe Stare Qua: lo stesso effetto di Blue Map, più le bombe
  if anyHas(function(p) return p:HasCollectible(ITEM_STARE) end) then
    level:ApplyBlueMapEffect()
    level:UpdateVisibility()
    for _, p in ipairs(players()) do
      if p:HasCollectible(ITEM_STARE) then p:AddBombs(L.STARE_BOMBS) end
    end
  end
  -- Il Miracolo di San Gennaruzzo: se l'oggetto arriva a metà piano, vale dal piano dopo
  if anyHas(function(p) return p:HasCollectible(ITEM_GENNARO) end) then
    level:AddAngelRoomChance(L.GENNARO_ANGEL_CHANCE)
  end
end)

mod:AddCallback(ModCallbacks.MC_POST_NEW_ROOM, function()
  local room = game:GetRoom()
  if not room:IsFirstVisit() then return end
  local rt = room:GetType()
  if (rt == RoomType.ROOM_SECRET or rt == RoomType.ROOM_SUPERSECRET)
    and anyHas(function(p) return p:HasCollectible(ITEM_STARE) end) then
    say(T.STARE, nil, 0, P.ITEM)
  elseif rt == RoomType.ROOM_ANGEL and anyHas(function(p) return p:HasCollectible(ITEM_GENNARO) end) then
    Isaac.Spawn(EntityType.ENTITY_PICKUP, PickupVariant.PICKUP_HEART, HeartSubType.HEART_ETERNAL,
      Isaac.GetFreeNearPosition(room:GetCenterPos(), 40), Vector.Zero, nil)
    say(T.GENNARO, T.GENNARO_SUB, 0, P.ITEM)
  end
end)

-- Che Fai, Te Ne Privi?
mod:AddCallback(ModCallbacks.MC_PRE_SPAWN_CLEAN_AWARD, function(_, rng, pos)
  local mult = 0
  for _, p in ipairs(players()) do mult = mult + p:GetTrinketMultiplier(TRINKET_PRIVI) end
  if not L.priviProcs(rng:RandomFloat(), mult) then return end
  local kinds = { PickupVariant.PICKUP_COIN, PickupVariant.PICKUP_BOMB, PickupVariant.PICKUP_KEY, PickupVariant.PICKUP_HEART }
  Isaac.Spawn(EntityType.ENTITY_PICKUP, kinds[rng:RandomInt(#kinds) + 1], 0,
    Isaac.GetFreeNearPosition(pos, 40), Vector.Zero, nil)
  say(T.PRIVI, nil, 0, P.ITEM)
end)

-- La Mossa del Pro Player: il bonus è per player e finisce col primo colpo o con la stanza
local proBonus = {}

mod:AddCallback(ModCallbacks.MC_USE_ITEM, function(_, _, _, player)
  proBonus[GetPtrHash(player)] = true
  refresh(CacheFlag.CACHE_DAMAGE)
  say(T.PRO, nil, 0, P.ITEM)
  return true
end, ITEM_PRO)

mod:AddCallback(ModCallbacks.MC_EVALUATE_CACHE, function(_, player, flag)
  if flag == CacheFlag.CACHE_DAMAGE and proBonus[GetPtrHash(player)] then
    player.Damage = player.Damage + L.PRO_DAMAGE
  end
end)

mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, function(_, entity)
  local h = GetPtrHash(entity)
  if not proBonus[h] then return end
  proBonus[h] = nil
  refresh(CacheFlag.CACHE_DAMAGE)
  say(T.CRETINO, nil, 0, P.CRETINO)
end, EntityType.ENTITY_PLAYER)

mod:AddCallback(ModCallbacks.MC_POST_NEW_ROOM, function()
  if next(proBonus) then
    proBonus = {}
    refresh(CacheFlag.CACHE_DAMAGE)
  end
end)

-- La Trollata
mod:AddCallback(ModCallbacks.MC_USE_ITEM, function()
  for _, e in ipairs(Isaac.GetRoomEntities()) do
    if e:IsVulnerableEnemy() then
      Isaac.Spawn(EntityType.ENTITY_BOMB, BombVariant.BOMB_TROLL, 0, e.Position, Vector.Zero, nil)
    end
  end
  say(T.TROLLATA, nil, 0, P.ITEM)
  return true
end, ITEM_TROLLATA)

-- Fai Così, Fai Così: doubling evita che la lacrima gemella conti come un nuovo tiro
local tearCount, doubling = {}, false

mod:AddCallback(ModCallbacks.MC_POST_FIRE_TEAR, function(_, tear)
  if doubling or not tear.SpawnerEntity then return end
  local player = tear.SpawnerEntity:ToPlayer()
  if not player or not player:HasCollectible(ITEM_FAICOSI) then return end
  local h = GetPtrHash(player)
  tearCount[h] = (tearCount[h] or 0) + 1
  if tearCount[h] % 2 == 0 then
    doubling = true
    player:FireTear(tear.Position, tear.Velocity:Rotated(8))
    doubling = false
  end
end)

-- Mannaggia a Lui
mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, function(_, entity)
  local player = entity:ToPlayer()
  local mult = player and player:GetTrinketMultiplier(TRINKET_MANNAGGIA) or 0
  if mult == 0 then return end
  local target, best
  for _, e in ipairs(Isaac.GetRoomEntities()) do
    if e:IsVulnerableEnemy() then
      local d = e.Position:Distance(player.Position)
      if not best or d < best then target, best = e, d end
    end
  end
  if target then
    target:TakeDamage(player.Damage * L.MANNAGGIA_MULT * mult, 0, EntityRef(player), 0)
    say(T.MANNAGGIA, nil, 0, P.MANNAGGIA)
  end
end, EntityType.ENTITY_PLAYER)

-- Trasformazione Tacchino: con tutti e 3 gli oggetti del tacchino, più danno e meno velocità
local function isTacchino(player)
  local n = 0
  for _, id in ipairs(TACCHINO_ITEMS) do
    if player:HasCollectible(id) then n = n + 1 end
  end
  return L.isTacchino(n)
end

local wasTacchino = {}

mod:AddCallback(ModCallbacks.MC_POST_PLAYER_UPDATE, function(_, player)
  local idx = GetPtrHash(player)
  local now = isTacchino(player)
  if now ~= (wasTacchino[idx] or false) then
    player:AddCacheFlags(CacheFlag.CACHE_DAMAGE)
    player:AddCacheFlags(CacheFlag.CACHE_SPEED)
    player:EvaluateItems()
    if now and not run.tacchinoShown then
      run.tacchinoShown = true
      say(T.TACCHINO_TRASF, T.TACCHINO_TRASF_SUB, 0, P.BACIONE)
      save()
    end
  end
  wasTacchino[idx] = now
end)

mod:AddCallback(ModCallbacks.MC_EVALUATE_CACHE, function(_, player, flag)
  if not isTacchino(player) then return end
  if flag == CacheFlag.CACHE_DAMAGE then
    player.Damage = player.Damage + L.TACCHINO_DAMAGE
  elseif flag == CacheFlag.CACHE_SPEED then
    player.MoveSpeed = player.MoveSpeed + L.TACCHINO_SPEED
  end
end)
