-- ==============================================================================
-- MODULE 02: TRAJECTORY, REVEAL MAP (PROTO 2) & 6-DOF FREECAM
-- Reconstructed Strictly From: Mode_ZO_v1/input/test.lua
-- Architecture: Clean Modular Luau
-- ==============================================================================

local Workspace = game:GetService("Workspace")
local UserInputService = game:GetService("UserInputService")
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local Camera = Workspace.CurrentCamera

-- [[ PROTO 2: PATH2D BÉZIER TRAJECTORY ENGINE ]]
local Path2DEngine = {}

function Path2DEngine.CreatePath(controlPoints)
    local path = Instance.new("Path2D")
    local points = {}
    if controlPoints then
        for _, pt in ipairs(controlPoints) do
            if typeof(pt) == "Vector2" or typeof(pt) == "UDim2" then
                table.insert(points, Path2DControlPoint.new(pt))
            end
        end
        path:SetControlPoints(points)
    end
    return path
end

function Path2DEngine.SampleCurve(path, alpha, jitter)
    if not path then return Vector2.new() end
    local pos = path:GetPositionOnCurve(alpha)
    if jitter and jitter > 0 then
        local rng = Random.new()
        pos = pos + rng:NextUnitVector() * rng:NextNumber(0, jitter)
    end
    return pos
end

function Path2DEngine.SampleArcLength(path, arcAlpha)
    if not path then return Vector2.new() end
    return path:GetPositionOnCurveArcLength(arcAlpha)
end

function Path2DEngine.GetTangent(path, alpha)
    if not path then return Vector2.new() end
    return path:GetTangentOnCurve(alpha)
end

function Path2DEngine.GetLength(path)
    if not path then return 0 end
    return path:GetLength()
end

-- [[ REVEAL MAP CONTROLLER ]]
local RevealMapController = {
    IsRunning = false,
}

function RevealMapController.Execute()
    if RevealMapController.IsRunning then return end
    RevealMapController.IsRunning = true

    task.spawn(function()
        local char = LocalPlayer.Character
        local hrp = char and char:FindFirstChild("HumanoidRootPart")
        if not hrp then RevealMapController.IsRunning = false; return end

        local campground = Workspace:FindFirstChild("Map") and Workspace.Map:FindFirstChild("Campground")
        local centerPos = (campground and campground:FindFirstChild("MainFire")) and campground.MainFire:GetPivot().Position or hrp.Position
        local radii = { 150, 300, 500, 750, 1000 }
        local steps = 24
        local flyAltitude = 45

        for _, radius in ipairs(radii) do
            if not RevealMapController.IsRunning then break end
            for i = 0, steps do
                if not RevealMapController.IsRunning then break end
                local angle = (i / steps) * (math.pi * 2)
                local targetPos = Vector3.new(
                    centerPos.X + math.cos(angle) * radius,
                    centerPos.Y + flyAltitude,
                    centerPos.Z + math.sin(angle) * radius
                )
                if char and char:FindFirstChild("HumanoidRootPart") then
                    char.HumanoidRootPart.CFrame = CFrame.new(targetPos)
                end
                task.wait(0.25)
            end
        end

        RevealMapController.IsRunning = false
    end)
end

function RevealMapController.Stop()
    RevealMapController.IsRunning = false
end

-- [[ CLOSURE X: 6-DOF FREECAM ]]
local Freecam = {
    Enabled  = false,
    Speed    = 60,
    PanSpeed = 1.0,
    PanAngle = Vector2.new(0, 0),
    Velocity = Vector3.new(0, 0, 0),
}

function Freecam.Step(deltaTime)
    if not Freecam.Enabled then return end
    local uis = UserInputService
    local moveDir = Vector3.new(
        (uis:IsKeyDown(Enum.KeyCode.D) and 1 or 0) - (uis:IsKeyDown(Enum.KeyCode.A) and 1 or 0),
        (uis:IsKeyDown(Enum.KeyCode.E) and 1 or 0) - (uis:IsKeyDown(Enum.KeyCode.Q) and 1 or 0),
        (uis:IsKeyDown(Enum.KeyCode.S) and 1 or 0) - (uis:IsKeyDown(Enum.KeyCode.W) and 1 or 0)
    )
    Freecam.Velocity = moveDir * Freecam.Speed
    local delta = uis:GetMouseDelta() * Freecam.PanSpeed
    Freecam.PanAngle = Freecam.PanAngle - Vector2.new(delta.X, delta.Y)

    local yaw   = math.rad(Freecam.PanAngle.X)
    local pitch = math.clamp(math.rad(Freecam.PanAngle.Y), -math.pi / 2, math.pi / 2)
    local rot   = CFrame.Angles(0, yaw, 0) * CFrame.Angles(pitch, 0, 0)

    Camera.CFrame = CFrame.new(Camera.CFrame.Position) * rot
    Camera.CFrame = Camera.CFrame + (rot * Freecam.Velocity * deltaTime)
end

return {
    Path2DEngine = Path2DEngine,
    RevealMapController = RevealMapController,
    Freecam = Freecam
}
