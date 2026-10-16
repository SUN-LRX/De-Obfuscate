-- ==============================================================================
-- MODULE 01: ENVIRONMENT, SERVICES & SYSTEM CONFIGURATION
-- Reconstructed Strictly From: Mode_ZO_v1/input/test.lua
-- Architecture: Clean Modular Luau
-- ==============================================================================

local getgenv = getgenv or function() return _G end
local shared = shared or {}

-- System Status Flags
getgenv().voidware_loaded = true
shared.VoidwareCustom = true
shared.NightsInTheForest = true
shared.TargetLanguage = "en"
shared.VoidwareLoadingDebug = false
shared.KillauraDebug = false

-- Roblox Engine Services
local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local CoreGui = game:GetService("CoreGui")

local LocalPlayer = Players.LocalPlayer
while not LocalPlayer do
    task.wait(0.1)
    LocalPlayer = Players.LocalPlayer
end
local Camera = Workspace.CurrentCamera

-- Global Toggles Repository
getgenv().Toggles = getgenv().Toggles or {}
local Toggles = getgenv().Toggles

Toggles.AutoStunToggle      = { Value = false, Default = false }
Toggles.StartSpamPlanting   = { Value = false, Default = false }
Toggles.INFSaplings         = { Value = false, Default = false }
Toggles.KillAuraToggle      = { Value = false, Default = false }
Toggles.IceAuraToggle       = { Value = false, Default = false }
Toggles.OreAuraToggle       = { Value = false, Default = false }
Toggles.RangeCircleToggle   = { Value = true,  Default = true }
Toggles.ESPHighlight        = { Value = true,  Default = true }
Toggles.ESPDistance         = { Value = true,  Default = true }
Toggles.AutoOpenSeedBox     = { Value = false, Default = false }
Toggles.AutoDragLogs        = { Value = false, Default = false }

-- Global Options Repository
getgenv().Options = getgenv().Options or {}
local Options = getgenv().Options

Options.AutoStunRange             = { Value = 50 }
Options.AutoStunChoiceDropdown     = { Value = { "Ram", "Deer", "Owl" } }
Options.CrockPotFoodDropdown       = { Value = "Carrot", Values = { "Carrot", "Apple", "Cake", "Mackerel", "Ribs" } }
Options.LanguageChoice             = { Value = "en 🇺🇸", CurrentValue = "en 🇺🇸" }
Options.LibraryChoice              = { Value = "Wind", CurrentValue = "Wind" }
Options.KillAuraRange              = { Value = 25 }
Options.HitboxMultiplier           = { Value = 2.5 }
Options.ESPFillTransparency        = { Value = 0.5 }
Options.ESPOutlineTransparency     = { Value = 0.0 }
Options.ESPTextSize                = { Value = 14 }
Options.FlySpeed                   = { Value = 60 }
Options.FlyPanSpeed                = { Value = 1.0 }

-- Entity Target Pool (Authentic 32 Monsters from 99 Nights in the Forest)
local ALL_GAME_ENTITIES = {
    "Boar", "Jungle Cultist", "Darkstring Cultist", "Shadow Cultist", "Brutal Cultist",
    "Kiwi", "Mossy Wolf", "Turret", "Impostor Santa", "Turkey", "FrogKing", "Frog",
    "Scorpion", "Hellephant", "Ram", "Naill", "FrogBlue", "FrogPurple", "Wolf", "Bear",
    "Bunny", "Mammoth", "Cultist", "Crossbow Cultist", "Juggernaut Cultist", "Alpha Wolf",
    "Alien", "Alien Elite", "Cultist King", "Meteor Crab", "Polar Bear", "Arctic Fox"
}

Options.FreezeCharacters = { Value = {}, Values = ALL_GAME_ENTITIES }
Options.TPCharacters     = { Value = {}, Values = ALL_GAME_ENTITIES }

local State = {
    Craters = {},
    FrozenObjects = {},
    OriginalHitboxSizes = {},
    RangeCircleObject = nil,
    Unloaded = false,
}

return {
    Players = Players,
    Workspace = Workspace,
    RunService = RunService,
    HttpService = HttpService,
    TweenService = TweenService,
    UserInputService = UserInputService,
    ReplicatedStorage = ReplicatedStorage,
    CoreGui = CoreGui,
    LocalPlayer = LocalPlayer,
    Camera = Camera,
    Toggles = Toggles,
    Options = Options,
    State = State,
    ALL_GAME_ENTITIES = ALL_GAME_ENTITIES
}
