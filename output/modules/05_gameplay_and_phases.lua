-- ==============================================================================
-- MODULE 05: WORLD AUTOMATION, TELEPORTS & IN-GAME EXPLOITS
-- Reconstructed Strictly From: Mode_ZO_v1/input/test.lua
-- Architecture: Clean Modular Luau
-- ==============================================================================

local Workspace = game:GetService("Workspace")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local LocalPlayer = Players.LocalPlayer

local World = {
    Craters = {},
    FrozenObjects = {},
}

function World.OpenBox(box)
    pcall(function()
        local prompt = box:FindFirstChildWhichIsA("ProximityPrompt", true)
        if prompt then
            fireproximityprompt(prompt)
        end
    end)
end

function World.AutoOpenSeedBox(box)
    if box and box.Name == "Seed Box" and box:IsA("Model") and box.PrimaryPart then
        local char = LocalPlayer.Character
        if not (char and char.PrimaryPart) then return end
        local prevCF = char:GetPrimaryPartCFrame()
        char:PivotTo(box:GetPrimaryPartCFrame())
        World.OpenBox(box)
        World.OpenBox(box)
        char:PivotTo(prevCF)
    end
end

function World.BringLogToMainFire(logModel)
    if not (logModel and logModel:IsA("Model") and logModel:IsDescendantOf(Workspace) and logModel.PrimaryPart) then
        return
    end
    pcall(function()
        local campground = Workspace:WaitForChild("Map"):WaitForChild("Campground")
        local mainFire = campground:WaitForChild("MainFire")
        logModel:PivotTo(mainFire:GetPrimaryPartCFrame())
        logModel.PrimaryPart.Anchored = true
        task.delay(0.1, function()
            if logModel and logModel.Parent and logModel.PrimaryPart then
                logModel.PrimaryPart.Anchored = false
            end
        end)
    end)
end

function World.DragScrapToWorkbench()
    local workbench = Workspace:FindFirstChild("Workbench", true)
    if not workbench or not workbench.PrimaryPart then return end
    local items = Workspace:FindFirstChild("Items") or Workspace
    for _, obj in ipairs(items:GetChildren()) do
        if (obj.Name == "Log" or string.find(obj.Name, "Gear") or string.find(obj.Name, "Scrap")) and obj:IsA("BasePart") then
            obj.CFrame = workbench.PrimaryPart.CFrame + Vector3.new(0, 2, 0)
        end
    end
end

function World.TeleportAllChests()
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    for _, obj in ipairs(Workspace:GetDescendants()) do
        if obj:IsA("Model") and string.find(obj.Name:lower(), "chest") and obj.PrimaryPart then
            pcall(function()
                obj:PivotTo(hrp.CFrame + Vector3.new(0, 2, 0))
            end)
        end
    end
end

function World.TeleportAllChildren()
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local charFolder = Workspace:FindFirstChild("Characters")
    if charFolder then
        for _, child in ipairs(charFolder:GetChildren()) do
            if string.find(child.Name:lower(), "child") or string.find(child.Name:lower(), "baby") then
                if child.PrimaryPart then
                    pcall(function()
                        child:PivotTo(hrp.CFrame + Vector3.new(0, 2, 0))
                    end)
                end
            end
        end
    end
end

function World.TeleportAllTrees(onlyBig)
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local foliage = Workspace:FindFirstChild("Map") and Workspace.Map:FindFirstChild("Foliage")
    local container = foliage or Workspace
    for _, tree in ipairs(container:GetChildren()) do
        if tree:IsA("Model") and string.find(tree.Name:lower(), "tree") and tree.PrimaryPart then
            local isBig = (tree:GetAttribute("Health") or 50) > 100 or string.find(tree.Name:lower(), "big")
            if not onlyBig or isBig then
                pcall(function()
                    tree:PivotTo(hrp.CFrame + Vector3.new(0, 5, 0))
                end)
            end
        end
    end
end

function World.FreezeSelectedEntities(freeze, selectedList)
    local selected = selectedList or {}
    local charFolder = Workspace:FindFirstChild("Characters")
    if not charFolder then return end

    for _, ent in ipairs(charFolder:GetChildren()) do
        if ent:IsA("Model") and ent.PrimaryPart then
            local shouldFreeze = false
            for _, name in ipairs(selected) do
                if ent.Name == name then shouldFreeze = true; break end
            end
            if shouldFreeze then
                ent.PrimaryPart.Anchored = freeze
                if freeze then
                    World.FrozenObjects[ent] = true
                else
                    World.FrozenObjects[ent] = nil
                end
            end
        end
    end
end

function World.PickupAllFlowers()
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local items = Workspace:FindFirstChild("Items") or Workspace
    for _, item in ipairs(items:GetChildren()) do
        if string.find(item.Name:lower(), "flower") then
            local primary = item:IsA("Model") and item.PrimaryPart or item
            if primary and primary:IsA("BasePart") then
                primary.CFrame = hrp.CFrame
            end
        end
    end
end

function World.CollectAllGoldStacks()
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local items = Workspace:FindFirstChild("Items") or Workspace
    for _, item in ipairs(items:GetChildren()) do
        if string.find(item.Name:lower(), "gold") then
            local primary = item:IsA("Model") and item.PrimaryPart or item
            if primary and primary:IsA("BasePart") then
                primary.CFrame = hrp.CFrame
            end
        end
    end
end

function World.BringFlashlights()
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local items = Workspace:FindFirstChild("Items") or Workspace
    for _, item in ipairs(items:GetChildren()) do
        if string.find(item.Name:lower(), "flashlight") then
            local primary = item:IsA("Model") and item.PrimaryPart or item
            if primary and primary:IsA("BasePart") then
                primary.CFrame = hrp.CFrame
            end
        end
    end
end

function World.AutoCrockPot(foodChoice)
    pcall(function()
        local pot = Workspace:FindFirstChild("Crock Pot", true)
        if pot then
            ReplicatedStorage.RemoteEvents.CookFood:FireServer(pot, foodChoice or "Carrot")
        end
    end)
end

function World.RegisterCrater(model)
    if string.find(string.lower(tostring(model)), "crater") then
        if model.ClassName == "Model" and model.PrimaryPart and model:FindFirstChild("OreNodes") then
            if not table.find(World.Craters, model) then
                table.insert(World.Craters, model)
            end
        end
    end
end

function World.OptimizeStreaming()
    pcall(function()
        local landmarks = Workspace:WaitForChild("Map"):WaitForChild("Landmarks")
        for _, landmark in ipairs(landmarks:GetChildren()) do
            landmark.ModelStreamingMode = Enum.ModelStreamingMode.Persistent
        end
    end)
    pcall(function()
        local items = Workspace:WaitForChild("Items")
        for _, item in ipairs(items:GetChildren()) do
            item.ModelStreamingMode = Enum.ModelStreamingMode.Persistent
        end
    end)
end

return World
