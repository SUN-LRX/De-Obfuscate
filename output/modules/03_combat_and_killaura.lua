-- ==============================================================================
-- MODULE 03: COMBAT, TARGET ACQUISITION, KILLAURA & AUTO STUN
-- Reconstructed Strictly From: Mode_ZO_v1/input/test.lua
-- Architecture: Clean Modular Luau
-- ==============================================================================

local Workspace = game:GetService("Workspace")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local LocalPlayer = Players.LocalPlayer

local Combat = {
    OriginalHitboxSizes = {},
}

function Combat.GetInventoryTool()
    local char = LocalPlayer.Character
    if not char then return nil, nil end
    local tool = char:FindFirstChildOfClass("Tool")
    if tool then return tool, "MeleeWeapon" end
    local bp = LocalPlayer:FindFirstChild("Backpack")
    if bp then
        tool = bp:FindFirstChildOfClass("Tool")
        if tool then return tool, "MeleeWeapon" end
    end
    return nil, nil
end

function Combat.FindNearbyTargets(range, checkIce, checkOre, cratersList)
    local rangeVal = tonumber(range) or 25
    local char = LocalPlayer.Character
    if not (char and char:FindFirstChild("HumanoidRootPart")) then return {} end
    local myPos = char.HumanoidRootPart.Position
    local targets = {}

    local charFolder = Workspace:FindFirstChild("Characters")
    if charFolder then
        for _, entity in ipairs(charFolder:GetChildren()) do
            pcall(function()
                if entity ~= char and not entity:GetAttribute("NotAttackable") then
                    local primary = entity.PrimaryPart or entity:FindFirstChild("HumanoidRootPart")
                    if primary then
                        local dist = (myPos - primary.Position).Magnitude
                        if dist <= rangeVal then
                            table.insert(targets, entity)
                        end
                    end
                end
            end)
        end
    end

    local itemsFolder = Workspace:FindFirstChild("Items")
    if itemsFolder then
        for _, item in ipairs(itemsFolder:GetChildren()) do
            pcall(function()
                if item.Name == "Alien" and item:IsA("Model") and item.PrimaryPart then
                    local dist = (myPos - item.PrimaryPart.Position).Magnitude
                    if dist <= rangeVal then
                        table.insert(targets, item)
                    end
                end
            end)
        end
    end

    if checkIce and charFolder then
        for _, ent in ipairs(charFolder:GetChildren()) do
            local ice = ent:FindFirstChild("IceBlock")
            if ice and ice:IsA("BasePart") then
                local dist = (myPos - ice.Position).Magnitude
                if dist <= rangeVal then
                    table.insert(targets, ice)
                end
            end
        end
    end

    if checkOre and cratersList then
        for _, crater in ipairs(cratersList) do
            if crater and crater.Parent and crater:FindFirstChild("OreNodes") then
                for _, node in ipairs(crater.OreNodes:GetChildren()) do
                    if string.find(node.Name, "Node") and node:IsA("BasePart") then
                        local dist = (myPos - node.Position).Magnitude
                        if dist <= rangeVal then
                            table.insert(targets, node)
                        end
                    end
                end
            end
        end
    end

    return targets
end

function Combat.DamageCharacter(target)
    pcall(function()
        ReplicatedStorage.RemoteEvents.DamageCharacter:FireServer(target)
    end)
end

function Combat.ApplyHitboxExpansion(model, multiplier)
    if not (model and model:IsA("Model") and model.PrimaryPart) then return end
    pcall(function()
        if not Combat.OriginalHitboxSizes[model] then
            Combat.OriginalHitboxSizes[model] = model.PrimaryPart.Size
        end
        local mult = multiplier or 2.5
        model.PrimaryPart.Transparency = 1
        model.PrimaryPart.CanCollide = false
        model.PrimaryPart.CanQuery = true
        model.PrimaryPart.Size = Combat.OriginalHitboxSizes[model] * mult
    end)
end

function Combat.AutoStunMonsters(range, targetsList)
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local rangeVal = tonumber(range) or 50
    local targets = targetsList or { "Ram", "Deer", "Owl" }
    local charFolder = Workspace:FindFirstChild("Characters")
    if not charFolder then return end

    for _, monster in ipairs(charFolder:GetChildren()) do
        if monster ~= char and monster.PrimaryPart and not monster:GetAttribute("NotAttackable") then
            local isMatch = false
            for _, tName in ipairs(targets) do
                if string.find(monster.Name:lower(), tName:lower()) then
                    isMatch = true
                    break
                end
            end
            if isMatch then
                local dist = (hrp.Position - monster.PrimaryPart.Position).Magnitude
                if dist <= rangeVal then
                    pcall(function()
                        ReplicatedStorage.RemoteEvents.StunEntity:FireServer(monster)
                    end)
                end
            end
        end
    end
end

return Combat
