local mod = RegisterMod("Risacca", 1)
local L = include("logic")
local json = require("json")
local game = Game()

local ITEM_ROTTO = Isaac.GetItemIdByName("Ho Rotto il Gioco")
local ITEM_DEADGOD = Isaac.GetItemIdByName("-1 al Dead God")
local TRINKET_STREAK = Isaac.GetTrinketIdByName("Win Streak")

-- Descrizioni per External Item Descriptions, solo se l'altra mod è attiva
if EID then
  EID:setModIndicatorName("Risacca Mod")
  EID:addCollectible(ITEM_ROTTO, L.EID.ROTTO)
  EID:addCollectible(ITEM_DEADGOD, L.EID.DEADGOD)
  EID:addTrinket(TRINKET_STREAK, L.EID.STREAK)
end

local function freshRun() return { streak = 0, hitThisFloor = false, deadGodKills = 0, beastyShown = false, kubrickShown = false } end
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
    local t = L.pickupText(qi.Quality, devilPending[idx] == qi.ID)
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
  end
end)

mod:AddCallback(ModCallbacks.MC_POST_NPC_DEATH, function(_, npc)
  if L.isFinalBoss(npc.Type, npc.Variant) and not roomFlags.bacione then
    roomFlags.bacione = true
    say(T.BACIONE, T.BACIONE_SUB, 30, P.BACIONE)
  end
end)
