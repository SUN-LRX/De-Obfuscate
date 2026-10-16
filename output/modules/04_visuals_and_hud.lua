-- ==============================================================================
-- MODULE 04: VISUALS, RANGECIRCLE & BILLBOARD ESP
-- Reconstructed Strictly From: Mode_ZO_v1/input/test.lua
-- Architecture: Clean Modular Luau
-- ==============================================================================

local Workspace = game:GetService("Workspace")
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer

local Visuals = {
    RangeCircleObject = nil,
}

function Visuals.CreateRangeCircle(range)
    local p = Instance.new("Part")
    p.Name = "RangeCircle"
    p.Shape = Enum.PartType.Cylinder
    p.Material = Enum.Material.ForceField
    p.Color = Color3.fromRGB(0, 255, 200)
    p.Transparency = 0.6
    p.Anchored = true
    p.CanCollide = false
    p.CanQuery = false
    p.CanTouch = false
    p.Size = Vector3.new(0.2, (range or 25) * 2, (range or 25) * 2)
    p.Parent = Workspace
    return p
end

function Visuals.UpdateRangeCircle(enabled, range)
    if enabled then
        if not Visuals.RangeCircleObject or not Visuals.RangeCircleObject.Parent then
            Visuals.RangeCircleObject = Visuals.CreateRangeCircle(range)
        end
        local char = LocalPlayer.Character
        local hrp = char and char:FindFirstChild("HumanoidRootPart")
        if hrp then
            local r = range or 25
            Visuals.RangeCircleObject.Size = Vector3.new(0.2, r * 2, r * 2)
            Visuals.RangeCircleObject.CFrame = hrp.CFrame * CFrame.Angles(0, 0, math.rad(90))
        end
    else
        if Visuals.RangeCircleObject then
            pcall(function() Visuals.RangeCircleObject:Destroy() end)
            Visuals.RangeCircleObject = nil
        end
    end
end

function Visuals.ApplyESP(target, text, fillTrans, outlineTrans, textSize, showDist)
    if not (target and target:IsDescendantOf(Workspace)) then return end

    local highlight = target:FindFirstChild("ESP_Highlight") or Instance.new("Highlight")
    highlight.Name = "ESP_Highlight"
    highlight.Adornee = target
    highlight.Enabled = true
    highlight.FillTransparency = fillTrans or 0.5
    highlight.OutlineTransparency = outlineTrans or 0.0
    highlight.Parent = target

    local billboard = target:FindFirstChild("ESP_Billboard") or Instance.new("BillboardGui")
    billboard.Name = "ESP_Billboard"
    billboard.Adornee = target
    billboard.Size = UDim2.new(0, 100, 0, 40)
    billboard.AlwaysOnTop = true
    billboard.Parent = target

    local label = billboard:FindFirstChild("ESP_Label") or Instance.new("TextLabel")
    label.Name = "ESP_Label"
    label.Size = UDim2.new(1, 0, 1, 0)
    label.BackgroundTransparency = 1
    label.TextColor3 = Color3.new(1, 1, 1)
    label.TextSize = textSize or 14
    label.Parent = billboard

    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    local primary = target.PrimaryPart or (target:IsA("BasePart") and target or target:FindFirstChildWhichIsA("BasePart"))

    local distText = ""
    if showDist and hrp and primary then
        local dist = math.floor((hrp.Position - primary.Position).Magnitude)
        distText = string.format("\n[%d]", dist)
    end
    label.Text = (text or target.Name) .. distText
end

return Visuals
