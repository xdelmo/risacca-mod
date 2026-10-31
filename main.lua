local mod = RegisterMod("Risacca", 1)
local L = include("logic")
local json = require("json")
local game = Game()

local ITEM_ROTTO = Isaac.GetItemIdByName("Ho Rotto il Gioco")
local ITEM_DEADGOD = Isaac.GetItemIdByName("-1 al Dead God")
local TRINKET_STREAK = Isaac.GetTrinketIdByName("Win Streak")

local function freshRun() return { streak = 0, hitThisFloor = false, deadGodKills = 0 } end
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
