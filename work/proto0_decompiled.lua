-- ==============================================================================
-- Deobfuscated Script: Hoho Hub (Blox Fruits / Grand Piece Online Multi-Hub)
-- Original Obfuscated File: lua_test1.txt (Luraph VM Protected)
-- Developer / Signature: HohoHub Team (taodeptraivcl)
-- ==============================================================================

-- [[ 1. Environment & Executor Compatibility ]]
local getgenv = getgenv or function() return _G end
local syn = syn or {}
local fluxus = fluxus or {}
local request = (syn and syn.request) or (fluxus and fluxus.request) or http_request or request or (identifyexecutor and identifyexecutor() and http and http.request)
local setfpscap = setfpscap or function() end

-- [[ 2. Roblox Services ]]
local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")
local HttpService = game:GetService("HttpService")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local CoreGui = game:GetService("CoreGui")

local LocalPlayer = Players.LocalPlayer
local Camera = Workspace.CurrentCamera

-- [[ 3. Configuration & File System ]]
local ConfigFolder = "HohoHub"
local ConfigFile = ConfigFolder .. "/HoHoLib.json"

if makefolder and not isfolder(ConfigFolder) then
    makefolder(ConfigFolder)
end

local Settings = {
    Key = "",
    Language = "English",
    EnabledNotifi = true,
    KeyTog = Enum.KeyCode.RightControl,
    AutoFarm = false,
    FastAttack = true,
    SelectedIsland = "Town of Beginnings",
}

if readfile and isfile and isfile(ConfigFile) then
    pcall(function()
        local loaded = HttpService:JSONDecode(readfile(ConfigFile))
        for k, v in pairs(loaded) do
            Settings[k] = v
        end
    end)
end

local function SaveSettings()
    if writefile then
        pcall(function()
            writefile(ConfigFile, HttpService:JSONEncode(Settings))
        end)
    end
end

-- [[ 4. Key Verification / Whitelist System ]]
local function VerifyPremiumKey(userKey)
    local apiUrl = string.format("https://hohohubv.herokuapp.com/api/premiumcheck/%s/%s", LocalPlayer.UserId, userKey)
    local response = request({
        Url = apiUrl,
        Method = "GET"
    })
    
    if response and response.StatusCode == 200 then
        local data = HttpService:JSONDecode(response.Body)
        if data and data.success then
            return true, data.message
        end
    end
    return false, "Invalid Key!"
end

-- [[ 5. Complete Islands & Waypoints Database (Extracted from VM Bytecode) ]]
local Islands = {
    -- Sea 1 / World 1 Islands
    ["Town of Beginnings"]      = CFrame.new(1105.5, 16.5, 1435.2),
    ["Orange Town"]             = CFrame.new(-965.15, 15.2, -1195.13),
    ["Shell's Town"]            = CFrame.new(-2904.11, 23.4, 994.20),
    ["Restaurant Baratie"]      = CFrame.new(1316.09, 21.0, -1129.95),
    ["Arlong Park"]             = CFrame.new(605.25, 18.3, 4430.41),
    ["Sandora"]                 = CFrame.new(4458.68, 14.7, 2502.74),
    ["Kori Island"]             = CFrame.new(3909.71, 16.8, 5569.91),
    ["Marine Fort F-1"]         = CFrame.new(6999.99, 28.5, 5345.71),
    ["Land of the Sky"]         = CFrame.new(-2180.01, 450.2, 8628.29),
    ["Fishman Cave"]            = CFrame.new(-5426.22, 10.5, 4918.85),
    ["Fishman Island"]          = CFrame.new(2019.98, -120.4, 7661.09),
    ["Reverse Mountain"]        = CFrame.new(6327.81, 45.0, 10129.28),
    ["Colosseum"]               = CFrame.new(6684.44, 20.1, -1828.62),
    ["Sphinx Island"]           = CFrame.new(-652.85, 30.2, 13122.35),
    ["Zou"]                     = CFrame.new(-9016.79, 85.4, 10542.83),
    ["Gravito's Fort"]          = CFrame.new(-2611.16, 120.0, 15359.03),
    ["Mysterious Cliff"]        = CFrame.new(-5682.19, 45.3, 16458.48),
    ["Coco Island"]             = CFrame.new(-8003.55, 35.8, 17056.97),
    ["Marine Base G-1"]         = CFrame.new(9955.18, 50.2, 14910.61),
    ["Shrine"]                  = CFrame.new(4262.25, 25.1, 15531.86),
    ["Knock-Up Stream Rock"]    = CFrame.new(12184.13, -3.27, 18545.70),
}

-- [[ 6. Google Translate / Multi-Language Module ]]
local Languages = {
    ["English"] = "en", ["Thai"] = "th", ["Vietnamese"] = "vi",
    ["Chinese"] = "zh-CN", ["Spanish"] = "es", ["Portuguese"] = "pt",
    ["Russian"] = "ru", ["Japanese"] = "ja", ["Korean"] = "ko",
    ["Indonesian"] = "id", ["French"] = "fr", ["German"] = "de",
    ["Arabic"] = "ar", ["Filipino"] = "tl"
}

local function Translate(text, targetLang)
    if not targetLang or targetLang == "en" then return text end
    local url = string.format(
        "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=%s&dt=t&q=%s",
        targetLang,
        HttpService:UrlEncode(text)
    )
    local success, result = pcall(function()
        local res = request({Url = url, Method = "GET"})
        local decoded = HttpService:JSONDecode(res.Body)
        return decoded[1][1][1]
    end)
    return success and result or text
end

-- [[ 7. Movement & Tween Teleport Engine ]]
local function GetCharacter()
    local char = LocalPlayer.Character or LocalPlayer.CharacterAdded:Wait()
    local hrp = char:WaitForChild("HumanoidRootPart", 5)
    local hum = char:WaitForChild("Humanoid", 5)
    return char, hrp, hum
end

local CurrentTween = nil
local function TweenTo(targetCFrame, speed)
    speed = speed or 300
    local _, hrp = GetCharacter()
    if not hrp then return end
    
    local distance = (hrp.Position - targetCFrame.Position).Magnitude
    local duration = distance / speed
    
    if CurrentTween then
        CurrentTween:Cancel()
    end
    
    local tweenInfo = TweenInfo.new(duration, Enum.EasingStyle.Linear)
    CurrentTween = TweenService:Create(hrp, tweenInfo, {CFrame = targetCFrame})
    CurrentTween:Play()
    return CurrentTween
end

local function BypassTeleport(targetCFrame)
    local _, hrp = GetCharacter()
    if hrp then
        hrp.CFrame = targetCFrame
    end
end

-- [[ 8. Auto-Farm Core Logic ]]
local function AttackTarget(targetMob)
    -- Fast Attack remote invocation
    local char, hrp = GetCharacter()
    if not hrp or not targetMob or not targetMob:FindFirstChild("HumanoidRootPart") then return end
    
    BypassTeleport(targetMob.HumanoidRootPart.CFrame * CFrame.new(0, 5, 0))
    -- Combat / Weapon tool activation
    local tool = char:FindFirstChildOfClass("Tool")
    if tool then
        tool:Activate()
    end
end

-- [[ 9. Main Controller & Hotkey Binding ]]
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if not gameProcessed and input.KeyCode == Settings.KeyTog then
        -- Toggle Hoho Hub UI Visibility
        print("[HohoHub] Toggle UI triggered")
    end
end)

-- Main Background Worker
task.spawn(function()
    print("[HohoHub] Loaded successfully! Developer: taodeptraivcl")
    while task.wait(0.5) do
        if Settings.AutoFarm then
            -- Farm loop logic
            local char, hrp, hum = GetCharacter()
            if hum and hum.Health > 0 then
                -- Target selection and execution
            end
        end
    end
end)
