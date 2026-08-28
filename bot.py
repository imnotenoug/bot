import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store farm states for usernames keyed by lowercase username
farm_states = {}

# The modified Roblox script provided
ROBLOX_SCRIPT = """local TeleportService = game:GetService("TeleportService")
local Players = game:GetService("Players")
local TextChatService = game:GetService("TextChatService")

local LocalPlayer = Players.LocalPlayer
local PlaceId = game.PlaceId

local function serverHop()
    pcall(function()
        if QueueTeleport then
            QueueTeleport("https://www.roblox.com/games/" .. PlaceId)
        end
    end)
    
    pcall(function()
        TeleportService:Teleport(PlaceId, LocalPlayer)
    end)
end

local function handleChatCommand(message)
    local msg = message:lower()
    if msg == "!shop" or msg:sub(1, 6) == "!shop " then
        serverHop()
    end
end

LocalPlayer.Chatted:Connect(handleChatCommand)

pcall(function()
    if TextChatService.ChatInputBarConfiguration and TextChatService.ChatInputBarConfiguration.TargetTextChannel then
        TextChatService.MessageReceived:Connect(function(textChatMessage)
            if textChatMessage.TextSource and textChatMessage.TextSource.UserId == LocalPlayer.UserId then
                handleChatCommand(textChatMessage.Text)
            end
        end)
    end
end)
-- ====================================================================
-- AWhub - ok pls no steal (Modified & Fixed)
-- ====================================================================

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local Workspace = game:GetService("Workspace")
local VirtualInputManager = game:GetService("VirtualInputManager")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local HttpService = game:GetService("HttpService")
local CoreGui = game:GetService("CoreGui")
local TeleportService = game:GetService("TeleportService")
local Lighting = game:GetService("Lighting")
local UserGameSettings = UserSettings():GetService("UserGameSettings")
local GuiService = game:GetService("GuiService")

local LP = Players.LocalPlayer
local Camera = Workspace.CurrentCamera

pcall(function()
    if setclipboard then
        setclipboard("https://discord.gg/ux2fjm2rt8")
    end
end)

local function getGuiParent()
    local success, gui = pcall(function()
        if gethui then
            return gethui()
        elseif syn and syn.protect_gui then
            local container = Instance.new("Folder")
            container.Name = "ProtectedGuiContainer"
            syn.protect_gui(container)
            container.Parent = CoreGui
            return container
        elseif CoreGui:FindFirstChild("RobloxGui") then
            return CoreGui
        end
        return LP:WaitForChild("PlayerGui", 5)
    end)
    if success and gui then return gui end
    return LP:FindFirstChild("PlayerGui") or CoreGui
end

-- ==================== WATERPROOF SYSTEM ====================
local table_insert = table.insert

local nicolas = {}
nicolas.__index = nicolas

function nicolas.new()
    return setmetatable({_tasks = {}, _destroyed = false}, nicolas)
end

function nicolas:GiveTask(task)
    if self._destroyed then
        self:_cleanupTask(task)
        return
    end
    table_insert(self._tasks, task)
    return task
end

function nicolas:GiveTasks(...)
    for _, task in ipairs({...}) do
        self:GiveTask(task)
    end
end

function nicolas:_cleanupTask(task)
    local taskType = typeof(task)
    if taskType == "RBXScriptConnection" then
        task:Disconnect()
    elseif taskType == "Instance" then
        task:Destroy()
    elseif taskType == "function" then
        task()
    elseif taskType == "table" and type(task.Destroy) == "function" then
        task:Destroy()
    end
end

function nicolas:DoCleaning()
    if self._destroyed then return end
    self._destroyed = true
    for _, task in ipairs(self._tasks) do
        self:_cleanupTask(task)
    end
    self._tasks = {}
end

function nicolas:Destroy()
    self:DoCleaning()
end

local waterMaid = nil
local modifiedParts = {}

local function DisableWaterPart(part)
    if part and part:IsA("BasePart") then
        if not modifiedParts[part] then
            modifiedParts[part] = {
                CanTouch = part.CanTouch,
                CanCollide = part.CanCollide,
            }
        end
        part.CanTouch = false
        part.CanCollide = false
    end
end

local function CheckMaps()
    local yacht = Workspace:FindFirstChild("Yacht")
    if yacht then
        local intereactive = yacht:FindFirstChild("Intereactive")
        if intereactive then
            local water = intereactive:FindFirstChild("Water")
            if water then
                DisableWaterPart(water:FindFirstChild("WaterPart"))
            end
        end
    end
    
    local pier = Workspace:FindFirstChild("Pier")
    if pier then
        DisableWaterPart(pier:FindFirstChild("Respawn"))
    end
end

local function enableWaterImmunity()
    if waterMaid then
        waterMaid:DoCleaning()
        waterMaid = nil
    end
    
    waterMaid = nicolas.new()
    CheckMaps()
    
    waterMaid:GiveTask(Workspace.DescendantAdded:Connect(CheckMaps))
    waterMaid:GiveTask(Workspace.DescendantRemoved:Connect(CheckMaps))
end

task.spawn(enableWaterImmunity)

local state = {
    farm = true,
    xpFarm = false,
    noclip = false,
    gun = false,
    afk = false,
    autoKillAll = false,
    autoShootMur = false,
    autoFlingMur = false,
    autoResetMurderer = false,
    autoResetSheriff = true,
    autoResetInnocent = true,
    antifling = true,
    disable3d = false,
    sendOnFull = false,
    autoRejoin = true,
    autoServerHop = true,
    autoPrestige = true,
}

local settingsConfig = { 
    webhookUrl = "",
    webhookCooldown = 30,
    discordUserId = "",
    tweenSpeed = 23.5
}

local selectedScale = 1
local TWEEN_SPEED = 23.5
local CONFIG_FILE = "Appleware.json"

local function saveSettings()
    pcall(function()
        if writefile then
            writefile(CONFIG_FILE, HttpService:JSONEncode({
                state = state,
                config = settingsConfig
            }))
        end
    end)
end

local function loadSettings()
    pcall(function()
        if readfile and isfile and isfile(CONFIG_FILE) then
            local decoded = HttpService:JSONDecode(readfile(CONFIG_FILE))
            if decoded.state then
                for k, v in pairs(decoded.state) do
                    if state[k] ~= nil then state[k] = v end
                end
            end
            if decoded.config then
                for k, v in pairs(decoded.config) do
                    if settingsConfig[k] ~= nil then settingsConfig[k] = v end
                end
            end
            if settingsConfig.tweenSpeed then
                TWEEN_SPEED = settingsConfig.tweenSpeed
            end
        end
    end)
end
loadSettings()

local UNDER = 3.4
local HIDE_POS = CFrame.new(0, -300, 0)
local MIN_BAG_FULL = 40

local lastCoinFoundTime = tick()
local NO_COIN_TIMEOUT = 12

local isExecutingAction = false
local currentCoinCount = 0
local maxCoinCount = 40
local bagFull = false
local busy = false
local currentFarmTween = nil
local currentTargetCoin = nil
local farmVelocityConn = nil
local totalCoinsEarned = 0
local activeResets = {}
local sessionStartTime = tick()

local lastRoundState = false
local roundStartTime = 0
local hasCollectedThisRound = false
local roundFullyStarted = false

local roleCache = {
    data = nil,
    timestamp = 0,
    TTL = 0.8,
}

local function getCachedRoleData()
    local now = tick()
    if roleCache.data and (now - roleCache.timestamp) < roleCache.TTL then
        return roleCache.data
    end
    local ok, result = pcall(function()
        local remote = ReplicatedStorage:FindFirstChild("GetPlayerData", true)
        if remote and remote:IsA("RemoteFunction") then
            return remote:InvokeServer()
        end
    end)
    if ok and result then
        roleCache.data = result
        roleCache.timestamp = now
        return result
    end
    roleCache.timestamp = now
    return roleCache.data
end

local function getMurd()
    local roleData = getCachedRoleData()
    if roleData then
        for playerName, data in pairs(roleData) do
            if data.Role == "Murderer" and not data.Killed and not data.Dead then
                local p = Players:FindFirstChild(playerName)
                if p and p ~= LP then return p end
            end
        end
    end
    for _, plr in ipairs(Players:GetPlayers()) do
        if plr ~= LP then
            local bp = plr:FindFirstChild("Backpack")
            local char = plr.Character
            if (bp and bp:FindFirstChild("Knife")) or (char and char:FindFirstChild("Knife")) then
                return plr
            end
        end
    end
    return nil
end

local function triggerMenuReset()
    pcall(function()
        VirtualInputManager:SendKeyEvent(true, Enum.KeyCode.Escape, false, game)
        VirtualInputManager:SendKeyEvent(false, Enum.KeyCode.Escape, false, game)
        task.wait(0.15)
        VirtualInputManager:SendKeyEvent(true, Enum.KeyCode.R, false, game)
        VirtualInputManager:SendKeyEvent(false, Enum.KeyCode.R, false, game)
        task.wait(0.15)
        VirtualInputManager:SendKeyEvent(true, Enum.KeyCode.Return, false, game)
        VirtualInputManager:SendKeyEvent(false, Enum.KeyCode.Return, false, game)
    end)
end

local st
local blackScreen = nil

local function alive()
    local c = LP.Character
    return c and c:FindFirstChild("Humanoid") and c.Humanoid.Health > 0 and c:FindFirstChild("HumanoidRootPart")
end

local function standUp()
    local hum = LP.Character and LP.Character:FindFirstChildOfClass("Humanoid")
    local root = LP.Character and LP.Character:FindFirstChild("HumanoidRootPart")
    if hum then
        hum.PlatformStand = false
        hum.AutoRotate = true
        hum:ChangeState(Enum.HumanoidStateType.GettingUp)
    end
    if root then
        root.Anchored = false
        root.AssemblyLinearVelocity = Vector3.zero
        root.AssemblyAngularVelocity = Vector3.zero
    end
end

local function hideSky()
    local root = LP.Character and LP.Character:FindFirstChild("HumanoidRootPart")
    local hum = LP.Character and LP.Character:FindFirstChildOfClass("Humanoid")
    if hum then hum.PlatformStand = true end
    if root then
        root.Anchored = true
        root.CFrame = HIDE_POS
        root.AssemblyLinearVelocity = Vector3.zero
        root.AssemblyAngularVelocity = Vector3.zero
    end
end

local function cancelFarmTween()
    if currentFarmTween then
        pcall(function() currentFarmTween:Cancel() end)
        currentFarmTween = nil
    end
    if farmVelocityConn then
        farmVelocityConn:Disconnect()
        farmVelocityConn = nil
    end
    currentTargetCoin = nil
end

local function applyLowDeviceOptimizations(enabled)
    pcall(function()
        if enabled then
            RunService:Set3dRenderingEnabled(false)
            if blackScreen then blackScreen.Visible = true end
            UserGameSettings.SavedQualityLevel = Enum.SavedQualityLevel.Level0
            Lighting.GlobalShadows = false
            Lighting.FogEnd = 9e9
            for _, v in ipairs(Lighting:GetChildren()) do
                if v:IsA("PostEffect") or v:IsA("Sky") or v:IsA("Atmosphere") then
                    v.Enabled = false
                end
            end
            task.spawn(function()
                for _, v in ipairs(Workspace:GetDescendants()) do
                    if v:IsA("ParticleEmitter") or v:IsA("Trail") or v:IsA("Beam") or v:IsA("Fire") or v:IsA("Smoke") then
                        v.Enabled = false
                    end
                end
            end)
            collectgarbage("collect")
        else
            RunService:Set3dRenderingEnabled(true)
            if blackScreen then blackScreen.Visible = false end
            UserGameSettings.SavedQualityLevel = Enum.SavedQualityLevel.Level10
            Lighting.GlobalShadows = true
            for _, v in ipairs(Lighting:GetChildren()) do
                if v:IsA("PostEffect") or v:IsA("Sky") or v:IsA("Atmosphere") then
                    v.Enabled = true
                end
            end
        end
    end)
end

-- ==================== WEBHOOK SYSTEM ====================
local httpRequest = request or http_request or (syn and syn.request) or (fluxus and fluxus.request)

local function sendAppleWareWebhook(title, description, fields, color)
    if settingsConfig.webhookUrl == "" then return end

    local ping = ""
    if settingsConfig.discordUserId ~= "" then
        ping = "<@" .. settingsConfig.discordUserId .. ">"
    end

    local embed = {
        title = "⚡ " .. title,
        description = description,
        color = color or 0x2B2D31,
        fields = fields or {},
        footer = {
            text = "AppleWare Automation Suite • " .. os.date("%H:%M:%S")
        },
        timestamp = DateTime.now():ToIsoDate()
    }

    local data = {
        content = ping ~= "" and (ping .. " 🔔 Status update report:") or nil,
        username = "AppleWare's Bot",
        embeds = {embed},
        allowed_mentions = {
            parse = {"users"}
        }
    }

    pcall(function()
        if httpRequest then
            httpRequest({
                Url = settingsConfig.webhookUrl,
                Method = "POST",
                Headers = {["Content-Type"] = "application/json"},
                Body = HttpService:JSONEncode(data)
            })
        end
    end)
end

local function sendStatusWebhook()
    local elapsed = tick() - sessionStartTime
    local hours = math.floor(elapsed / 3600)
    local minutes = math.floor((elapsed % 3600) / 60)
    local seconds = math.floor(elapsed % 60)
    
    local elapsedHours = math.max(elapsed / 3600, 0.001)
    local rate = math.floor((totalCoinsEarned or 0) / elapsedHours)

    local timeFormatted = string.format("%dh %dm %ds", hours, minutes, seconds)
    if hours == 0 then
        timeFormatted = string.format("%dm %ds", minutes, seconds)
    end

    sendAppleWareWebhook(
        "Session Progress Report",
        "Update for " .. tostring(LP.Name),
        {
            {name = "👤 User Profile", value = "`" .. tostring(LP.Name) .. "`\nID: `" .. tostring(LP.UserId) .. "`", inline = true},
            {name = "💰 Coin Statistics", value = "Bag Capacity: **" .. tostring(currentCoinCount) .. "/" .. tostring(maxCoinCount) .. "**\nTotal Harvested: **" .. tostring(totalCoinsEarned) .. " 🪙**", inline = true},
            {name = "⏱️ Performance", value = "Active Time: **" .. timeFormatted .. "**\nHarvest Rate: **" .. tostring(rate) .. " coins/hr**", inline = false},
            {name = "🌐 Server Details", value = "Place ID: `" .. tostring(game.PlaceId) .. "`\nJob ID: `" .. tostring(game.JobId) .. "`", inline = false}
        },
        0x00D26A
    )
end

task.spawn(function()
    while true do
        local waitTime = settingsConfig.webhookCooldown
        if not waitTime or waitTime < 5 then waitTime = 30 end
        task.wait(waitTime)

        if state.sendOnFull and settingsConfig.webhookUrl ~= "" then
            sendStatusWebhook()
        end
    end
end)

-- ==================== HARDWARE-STABLE FLING SYSTEM (4 ATTEMPTS) ====================
local function restoreSelf(character, savedData, originalDestroyHeight)
    if not character or not savedData then
        Workspace.FallenPartsDestroyHeight = originalDestroyHeight
        return
    end
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    local rootPart = character:FindFirstChild("HumanoidRootPart")
    if not humanoid or not rootPart then
        Workspace.FallenPartsDestroyHeight = originalDestroyHeight
        return
    end
    Workspace.FallenPartsDestroyHeight = originalDestroyHeight
    rootPart.Anchored = false
    rootPart.CFrame = savedData.cframe
    rootPart.AssemblyLinearVelocity = Vector3.zero
    rootPart.AssemblyAngularVelocity = Vector3.zero
    humanoid.PlatformStand = false
    pcall(function() humanoid:ChangeState(Enum.HumanoidStateType.GettingUp) end)
end

local function VoidReset(TargetPlayer)
    if not TargetPlayer or TargetPlayer == LP then return end
    if activeResets[TargetPlayer.UserId] then return end

    local Character = LP.Character
    if not Character then return end
    local Humanoid = Character:FindFirstChildOfClass("Humanoid")
    local RootPart = Character:FindFirstChild("HumanoidRootPart")
    local TCharacter = TargetPlayer.Character
    if not (Humanoid and RootPart and TCharacter) then return end
    local TRootPart = TCharacter:FindFirstChild("HumanoidRootPart")
    if not TRootPart then return end

    cancelFarmTween()
    if st then st.Text = " [AWhub] Flinging Murderer..." end

    local savedCF = RootPart.CFrame
    local originalDestroyHeight = Workspace.FallenPartsDestroyHeight
    Workspace.FallenPartsDestroyHeight = -100000
    
    for _, part in ipairs(Character:GetChildren()) do
        if part:IsA("BasePart") then
            part.CanCollide = true
        end
    end

    Humanoid.PlatformStand = true
    RootPart.Anchored = false

    local startTime = tick()
    local resetObj = {conn = nil}
    activeResets[TargetPlayer.UserId] = resetObj

    local function cleanup()
        activeResets[TargetPlayer.UserId] = nil
        if resetObj.conn then resetObj.conn:Disconnect() end
        restoreSelf(Character, {cframe = savedCF}, originalDestroyHeight)
        if st then st.Text = " [AWhub] Murderer fling attempt ended." end
    end

    local toggle = false
    resetObj.conn = RunService.PostSimulation:Connect(function()
        if not TargetPlayer.Character or not TRootPart.Parent or not RootPart.Parent then
            cleanup()
            return
        end
        if tick() - startTime >= 1.8 then
            cleanup()
            return
        end

        toggle = not toggle
        local rotAngle = toggle and 90 or -90
        local velVector = toggle and Vector3.new(99999, 99999, 99999) or Vector3.new(-99999, -99999, -99999)

        RootPart.CFrame = TRootPart.CFrame * CFrame.Angles(math.rad(rotAngle), 0, 0)
        RootPart.AssemblyLinearVelocity = velVector
        RootPart.AssemblyAngularVelocity = Vector3.new(99999, 99999, 99999)

        pcall(firetouchinterest, RootPart, TRootPart, 0)
        pcall(firetouchinterest, RootPart, TRootPart, 1)
    end)
end

local function reliableFling(TargetPlayer)
    if not TargetPlayer or TargetPlayer == LP then return end
    local maxAttempts = 4
    for attempt = 1, maxAttempts do
        if not TargetPlayer or not TargetPlayer.Parent then break end
        
        local tChar = TargetPlayer.Character
        local tHum = tChar and tChar:FindFirstChildOfClass("Humanoid")
        if not tHum or tHum.Health <= 0 then break end

        VoidReset(TargetPlayer)

        while activeResets[TargetPlayer.UserId] do
            task.wait(0.05)
        end

        task.wait(0.3)

        tChar = TargetPlayer.Character
        tHum = tChar and tChar:FindFirstChildOfClass("Humanoid")
        if not tHum or tHum.Health <= 0 then
            if st then st.Text = " [AWhub] Murderer successfully eliminated!" end
            break
        else
            if attempt < maxAttempts then
                if st then st.Text = " [AWhub] Fling retrying (" .. (attempt + 1) .. "/" .. maxAttempts .. ")..." end
                task.wait(0.2)
            end
        end
    end
end

local function flingMurdererNow()
    task.spawn(function()
        local wasFarming = state.farm
        local wasXpFarming = state.xpFarm
        state.farm = false
        state.xpFarm = false
        cancelFarmTween()

        hideSky()
        task.wait(0.2)

        local mur = getMurd()
        if mur and mur.Character then
            reliableFling(mur)
        else
            if st then st.Text = " [AWhub] Murderer not found!" end
        end

        hideSky()
        task.wait(0.2)

        state.farm = wasFarming
        state.xpFarm = wasXpFarming
    end)
end

-- ==================== COMBAT / UTILITY FUNCTIONS ====================
local function findTool(name)
    local char, bp = LP.Character, LP:FindFirstChild("Backpack")
    if char and char:FindFirstChild(name) then return char[name] end
    if bp and bp:FindFirstChild(name) then return bp[name] end
    return nil
end

local function equipTool(name)
    local char = LP.Character
    local bp = LP:FindFirstChild("Backpack")
    local hum = char and char:FindFirstChildOfClass("Humanoid")
    if not char then return nil end
    
    local existing = char:FindFirstChild(name)
    if existing then return existing end
    
    local tool = bp and bp:FindFirstChild(name)
    if tool and hum then
        pcall(function()
            hum:EquipTool(tool)
        end)
        task.wait(0.15)
        if not char:FindFirstChild(name) and tool.Parent == bp then
            pcall(function()
                tool.Parent = char
            end)
        end
        task.wait(0.05)
        return char:FindFirstChild(name)
    end
    return nil
end

local function getRole()
    if findTool("Knife") then return "Murderer" end
    if findTool("Gun") then return "Sheriff" end
    
    local roleData = getCachedRoleData()
    if roleData and roleData[LP.Name] and roleData[LP.Name].Role then
        return roleData[LP.Name].Role
    end
    return "Innocent"
end

local function executeKillBehind(targetPlayer)
    local targetChar = targetPlayer.Character
    local targetRoot = targetChar and targetChar:FindFirstChild("HumanoidRootPart")
    local targetHumanoid = targetChar and targetChar:FindFirstChildOfClass("Humanoid")
    
    local LocalPlayer = Players.LocalPlayer
    local myRoot = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
    
    if targetHumanoid and targetHumanoid.Health > 0 and targetRoot and myRoot then
        local tStart = tick()
        while tick() - tStart < 1.0 and targetHumanoid.Health > 0 and targetRoot.Parent and myRoot.Parent and alive() do
            local knife = LocalPlayer.Character:FindFirstChild("Knife")
            if not knife then
                knife = equipTool("Knife")
            end

            myRoot.CFrame = targetRoot.CFrame * CFrame.new(0, 0, 3)
            myRoot.AssemblyLinearVelocity = Vector3.zero
            myRoot.AssemblyAngularVelocity = Vector3.zero

            pcall(function()
                if knife then knife:Activate() end
            end)
            
            pcall(function()
                for _, v in ipairs(ReplicatedStorage:GetDescendants()) do
                    if v:IsA("RemoteEvent") and (string.lower(v.Name):find("knife") or string.lower(v.Name):find("hit") or string.lower(v.Name):find("stab") or string.lower(v.Name):find("kill")) then
                        v:FireServer(targetRoot.Position)
                    end
                end
            end)
            task.wait(0.03)
        end
    end
end

local function autoKillAllPlayers()
    local LocalPlayer = Players.LocalPlayer

    standUp()
    task.wait(0.1)

    local knife = findTool("Knife")
    if not knife then
        for _, v in ipairs(ReplicatedStorage:GetDescendants()) do
            if v:IsA("Tool") and v.Name == "Knife" then
                knife = v:Clone()
                knife.Parent = LocalPlayer.Character
                break
            end
        end
    end

    if not knife then
        knife = equipTool("Knife")
    end

    if not knife then
        for i = 1, 10 do
            task.wait(0.1)
            knife = equipTool("Knife")
            if knife then break end
        end
    end

    if not knife then 
        if st then st.Text = " [AWhub] No knife found to stab players!" end
        return 
    end

    if st then st.Text = " [AWhub] Stabbing players from behind..." end

    for _, targetPlayer in ipairs(Players:GetPlayers()) do
        if targetPlayer ~= LocalPlayer then
            local tChar = targetPlayer.Character
            local tHum = tChar and tChar:FindFirstChildOfClass("Humanoid")
            if tHum and tHum.Health > 0 then
                executeKillBehind(targetPlayer)
            end
        end
    end
end

-- ==================== UI ====================
local function buildUI()
    local parent = getGuiParent()
    pcall(function()
        local old = parent:FindFirstChild("AWhub")
        if old then old:Destroy() end
    end)

    local baseWidth = 420 * selectedScale
    local baseHeight = 380 * selectedScale
    local fontSizeMult = selectedScale

    local sg = Instance.new("ScreenGui")
    sg.Name = "AWhub"
    sg.Parent = parent
    sg.ResetOnSpawn = false
    sg.DisplayOrder = 999999
    sg.IgnoreGuiInset = true

    blackScreen = Instance.new("Frame")
    blackScreen.Size = UDim2.new(1, 0, 1, 0)
    blackScreen.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
    blackScreen.BorderSizePixel = 0
    blackScreen.Visible = state.disable3d
    blackScreen.ZIndex = -1
    blackScreen.Parent = sg

    local f = Instance.new("Frame")
    f.Size = UDim2.new(0, baseWidth, 0, baseHeight)
    f.Position = UDim2.new(0.5, -baseWidth/2, 0.5, -baseHeight/2)
    f.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
    f.BackgroundTransparency = 0.05
    f.Active = true
    f.Draggable = true
    f.ClipsDescendants = true
    f.Parent = sg
    Instance.new("UICorner", f).CornerRadius = UDim.new(0, 12 * selectedScale)

    local stroke = Instance.new("UIStroke", f)
    stroke.Color = Color3.fromRGB(255, 255, 255)
    stroke.Thickness = 1.5 * selectedScale
    stroke.Transparency = 0.2

    local h = Instance.new("Frame")
    h.Size = UDim2.new(1, 0, 0, 38 * selectedScale)
    h.BackgroundColor3 = Color3.fromRGB(10, 10, 10)
    h.Parent = f
    Instance.new("UICorner", h).CornerRadius = UDim.new(0, 12 * selectedScale)

    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(1, -20 * selectedScale, 1, 0)
    title.Position = UDim2.new(0, 12 * selectedScale, 0, 0)
    title.BackgroundTransparency = 1
    title.Text = "AWhub"
    title.TextColor3 = Color3.fromRGB(255, 255, 255)
    title.Font = Enum.Font.GothamBold
    title.TextSize = 13 * fontSizeMult
    title.TextXAlignment = Enum.TextXAlignment.Left
    title.Parent = h

    local tb = Instance.new("Frame")
    tb.Size = UDim2.new(1, -24 * selectedScale, 0, 34 * selectedScale)
    tb.Position = UDim2.new(0, 12 * selectedScale, 0, 48 * selectedScale)
    tb.BackgroundTransparency = 1
    tb.Parent = f

    local tabs = {"Farm", "Combat", "Webhook", "Misc", "UI"}
    local pages, btns = {}, {}
    local tabWidth = 1 / #tabs

    for i, name in pairs(tabs) do
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(tabWidth, -3 * selectedScale, 1, 0)
        btn.Position = UDim2.new((i - 1) * tabWidth, i > 1 and (2 * selectedScale) or 0, 0, 0)
        btn.BackgroundColor3 = (i == 1) and Color3.fromRGB(40, 40, 40) or Color3.fromRGB(15, 15, 15)
        btn.Text = name
        btn.TextColor3 = Color3.fromRGB(255, 255, 255)
        btn.Font = Enum.Font.GothamBold
        btn.TextSize = 10 * fontSizeMult
        btn.Parent = tb
        Instance.new("UICorner", btn).CornerRadius = UDim.new(0, 8 * selectedScale)
        btns[name] = btn

        local pg = Instance.new("ScrollingFrame")
        pg.Size = UDim2.new(1, -24 * selectedScale, 1, -150 * selectedScale)
        pg.Position = UDim2.new(0, 12 * selectedScale, 0, 92 * selectedScale)
        pg.BackgroundTransparency = 1
        pg.ScrollBarThickness = 4 * selectedScale
        pg.CanvasSize = UDim2.new(0, 0, 0, 400 * selectedScale)
        pg.Parent = f
        pg.Visible = (i == 1)
        pages[name] = pg

        btn.MouseButton1Click:Connect(function()
            for _, b in pairs(btns) do
                TweenService:Create(b, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(15, 15, 15)}):Play()
            end
            TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(40, 40, 40)}):Play()
            for _, p in pairs(pages) do p.Visible = false end
            pg.Visible = true
        end)
    end

    st = Instance.new("TextLabel")
    st.Size = UDim2.new(1, -24 * selectedScale, 0, 26 * selectedScale)
    st.Position = UDim2.new(0, 12 * selectedScale, 1, -34 * selectedScale)
    st.BackgroundColor3 = Color3.fromRGB(10, 10, 10)
    st.Text = " AWhub Ready"
    st.TextColor3 = Color3.fromRGB(255, 255, 255)
    st.Font = Enum.Font.GothamSemibold
    st.TextSize = 11 * fontSizeMult
    st.TextXAlignment = Enum.TextXAlignment.Left
    st.Parent = f
    Instance.new("UICorner", st).CornerRadius = UDim.new(0, 6 * selectedScale)

    local function tgg(page, name, y, key)
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(1, 0, 0, 32 * selectedScale)
        btn.Position = UDim2.new(0, 0, 0, y * selectedScale)
        btn.BackgroundColor3 = state[key] and Color3.fromRGB(35, 35, 35) or Color3.fromRGB(15, 15, 15)
        btn.Text = "  " .. name
        btn.TextColor3 = Color3.fromRGB(255, 255, 255)
        btn.Font = Enum.Font.GothamMedium
        btn.TextSize = 11.5 * fontSizeMult
        btn.TextXAlignment = Enum.TextXAlignment.Left
        btn.Parent = page
        Instance.new("UICorner", btn).CornerRadius = UDim.new(0, 6 * selectedScale)

        local pill = Instance.new("Frame")
        pill.Size = UDim2.new(0, 38 * selectedScale, 0, 18 * selectedScale)
        pill.Position = UDim2.new(1, -44 * selectedScale, 0.5, -9 * selectedScale)
        pill.BackgroundColor3 = state[key] and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(40, 40, 40)
        pill.Parent = btn
        Instance.new("UICorner", pill).CornerRadius = UDim.new(1, 0)

        local dot = Instance.new("Frame")
        dot.Size = UDim2.new(0, 14 * selectedScale, 0, 14 * selectedScale)
        dot.Position = state[key] and UDim2.new(1, -16 * selectedScale, 0.5, -7 * selectedScale) or UDim2.new(0, 2 * selectedScale, 0.5, -7 * selectedScale)
        dot.BackgroundColor3 = state[key] and Color3.fromRGB(0, 0, 0) or Color3.fromRGB(255, 255, 255)
        dot.Parent = pill
        Instance.new("UICorner", dot).CornerRadius = UDim.new(1, 0)

        btn.MouseButton1Click:Connect(function()
            state[key] = not state[key]
            TweenService:Create(btn, TweenInfo.new(0.2), {
                BackgroundColor3 = state[key] and Color3.fromRGB(35, 35, 35) or Color3.fromRGB(15, 15, 15)
            }):Play()
            TweenService:Create(pill, TweenInfo.new(0.2), {
                BackgroundColor3 = state[key] and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(40, 40, 40)
            }):Play()
            TweenService:Create(dot, TweenInfo.new(0.2), {
                Position = state[key] and UDim2.new(1, -16 * selectedScale, 0.5, -7 * selectedScale) or UDim2.new(0, 2 * selectedScale, 0.5, -7 * selectedScale),
                BackgroundColor3 = state[key] and Color3.fromRGB(0, 0, 0) or Color3.fromRGB(255, 255, 255)
            }):Play()
            
            if key == "disable3d" then
                applyLowDeviceOptimizations(state.disable3d)
            end
            
            saveSettings()
        end)
    end

    local function addActionButton(page, name, y, callback)
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(1, 0, 0, 32 * selectedScale)
        btn.Position = UDim2.new(0, 0, 0, y * selectedScale)
        btn.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
        btn.Text = "  " .. name
        btn.TextColor3 = Color3.fromRGB(255, 255, 255)
        btn.Font = Enum.Font.GothamMedium
        btn.TextSize = 11.5 * fontSizeMult
        btn.TextXAlignment = Enum.TextXAlignment.Left
        btn.Parent = page
        Instance.new("UICorner", btn).CornerRadius = UDim.new(0, 6 * selectedScale)
        btn.MouseButton1Click:Connect(function()
            callback()
        end)
    end

    -- Farm Tab
    tgg(pages["Farm"], "Farm (Safe)", 0, "farm")
    tgg(pages["Farm"], "XP Farm", 38, "xpFarm")
    tgg(pages["Farm"], "Disable 3D Rendering", 76, "disable3d")

    local speedContainer = Instance.new("Frame")
    speedContainer.Size = UDim2.new(1, 0, 0, 32 * selectedScale)
    speedContainer.Position = UDim2.new(0, 0, 0, 114 * selectedScale)
    speedContainer.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    speedContainer.Parent = pages["Farm"]
    Instance.new("UICorner", speedContainer).CornerRadius = UDim.new(0, 6 * selectedScale)

    local speedLabel = Instance.new("TextLabel")
    speedLabel.Size = UDim2.new(0.4, 0, 1, 0)
    speedLabel.Position = UDim2.new(0, 8 * selectedScale, 0, 0)
    speedLabel.BackgroundTransparency = 1
    speedLabel.Text = "  Tween Speed"
    speedLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
    speedLabel.Font = Enum.Font.GothamMedium
    speedLabel.TextSize = 11.5 * fontSizeMult
    speedLabel.TextXAlignment = Enum.TextXAlignment.Left
    speedLabel.Parent = speedContainer

    local speedPlus = Instance.new("TextButton")
    speedPlus.Size = UDim2.new(0, 28 * selectedScale, 0, 22 * selectedScale)
    speedPlus.Position = UDim2.new(1, -34 * selectedScale, 0.5, -11 * selectedScale)
    speedPlus.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
    speedPlus.Text = "+"
    speedPlus.TextColor3 = Color3.fromRGB(255, 255, 255)
    speedPlus.Font = Enum.Font.GothamBold
    speedPlus.TextSize = 12 * fontSizeMult
    speedPlus.Parent = speedContainer
    Instance.new("UICorner", speedPlus).CornerRadius = UDim.new(0, 4 * selectedScale)

    local speedBox = Instance.new("TextBox")
    speedBox.Size = UDim2.new(0, 50 * selectedScale, 0, 22 * selectedScale)
    speedBox.Position = UDim2.new(1, -88 * selectedScale, 0.5, -11 * selectedScale)
    speedBox.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
    speedBox.Text = tostring(TWEEN_SPEED)
    speedBox.TextColor3 = Color3.fromRGB(255, 255, 255)
    speedBox.Font = Enum.Font.GothamBold
    speedBox.TextSize = 11 * fontSizeMult
    speedBox.TextXAlignment = Enum.TextXAlignment.Center
    speedBox.Parent = speedContainer
    Instance.new("UICorner", speedBox).CornerRadius = UDim.new(0, 4 * selectedScale)

    local speedMinus = Instance.new("TextButton")
    speedMinus.Size = UDim2.new(0, 28 * selectedScale, 0, 22 * selectedScale)
    speedMinus.Position = UDim2.new(1, -120 * selectedScale, 0.5, -11 * selectedScale)
    speedMinus.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
    speedMinus.Text = "-"
    speedMinus.TextColor3 = Color3.fromRGB(255, 255, 255)
    speedMinus.Font = Enum.Font.GothamBold
    speedMinus.TextSize = 12 * fontSizeMult
    speedMinus.Parent = speedContainer
    Instance.new("UICorner", speedMinus).CornerRadius = UDim.new(0, 4 * selectedScale)

    speedPlus.MouseButton1Click:Connect(function()
        TWEEN_SPEED = math.clamp(TWEEN_SPEED + 1, 1, 100)
        speedBox.Text = tostring(TWEEN_SPEED)
        settingsConfig.tweenSpeed = TWEEN_SPEED
        saveSettings()
    end)

    speedMinus.MouseButton1Click:Connect(function()
        TWEEN_SPEED = math.clamp(TWEEN_SPEED - 1, 1, 100)
        speedBox.Text = tostring(TWEEN_SPEED)
        settingsConfig.tweenSpeed = TWEEN_SPEED
        saveSettings()
    end)

    speedBox.FocusLost:Connect(function()
        local val = tonumber(speedBox.Text)
        if val then
            TWEEN_SPEED = math.clamp(val, 1, 100)
            speedBox.Text = tostring(TWEEN_SPEED)
            settingsConfig.tweenSpeed = TWEEN_SPEED
            saveSettings()
        else
            speedBox.Text = tostring(TWEEN_SPEED)
        end
    end)

    -- Combat Tab
    tgg(pages["Combat"], "Auto Shoot Murderer", 0, "autoShootMur")
    tgg(pages["Combat"], "Auto Kill All", 38, "autoKillAll")
    tgg(pages["Combat"], "Auto Fling Murderer", 76, "autoFlingMur")
    tgg(pages["Combat"], "Auto Reset: Murderer", 114, "autoResetMurderer")
    tgg(pages["Combat"], "Auto Reset: Sheriff", 152, "autoResetSheriff")
    tgg(pages["Combat"], "Auto Reset: Innocent", 190, "autoResetInnocent")
    addActionButton(pages["Combat"], "Fling Murderer Now", 228, flingMurdererNow)

    -- Webhook Tab
    tgg(pages["Webhook"], "Auto send based off of timer", 0, "sendOnFull")

    local intervals = {
        {text = "30s", seconds = 30},
        {text = "1m", seconds = 60},
        {text = "5m", seconds = 300},
        {text = "10m", seconds = 600},
        {text = "20m", seconds = 1200}
    }

    local currentIntervalIndex = 1
    for i, v in ipairs(intervals) do
        if v.seconds == settingsConfig.webhookCooldown then
            currentIntervalIndex = i
            break
        end
    end

    local timerBtn = Instance.new("TextButton")
    timerBtn.Size = UDim2.new(1, 0, 0, 32 * selectedScale)
    timerBtn.Position = UDim2.new(0, 0, 0, 38 * selectedScale)
    timerBtn.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    timerBtn.Text = "  Timer Interval: " .. intervals[currentIntervalIndex].text
    timerBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    timerBtn.Font = Enum.Font.GothamMedium
    timerBtn.TextSize = 11.5 * fontSizeMult
    timerBtn.TextXAlignment = Enum.TextXAlignment.Left
    timerBtn.Parent = pages["Webhook"]
    Instance.new("UICorner", timerBtn).CornerRadius = UDim.new(0, 6 * selectedScale)

    timerBtn.MouseButton1Click:Connect(function()
        currentIntervalIndex = currentIntervalIndex + 1
        if currentIntervalIndex > #intervals then
            currentIntervalIndex = 1
        end
        local selected = intervals[currentIntervalIndex]
        timerBtn.Text = "  Timer Interval: " .. selected.text
        settingsConfig.webhookCooldown = selected.seconds
        saveSettings()
    end)

    local whBox = Instance.new("TextBox")
    whBox.Size = UDim2.new(1, 0, 0, 28 * selectedScale)
    whBox.Position = UDim2.new(0, 0, 0, 76 * selectedScale)
    whBox.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    whBox.PlaceholderText = "Webhook URL..."
    whBox.Text = settingsConfig.webhookUrl
    whBox.TextColor3 = Color3.fromRGB(255, 255, 255)
    whBox.Font = Enum.Font.Gotham
    whBox.TextSize = 10 * fontSizeMult
    whBox.Parent = pages["Webhook"]
    Instance.new("UICorner", whBox).CornerRadius = UDim.new(0, 6 * selectedScale)
    whBox.FocusLost:Connect(function()
        settingsConfig.webhookUrl = whBox.Text
        saveSettings()
    end)

    local idBox = Instance.new("TextBox")
    idBox.Size = UDim2.new(1, 0, 0, 28 * selectedScale)
    idBox.Position = UDim2.new(0, 0, 0, 114 * selectedScale)
    idBox.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    idBox.PlaceholderText = "Discord User ID (for ping)..."
    idBox.Text = settingsConfig.discordUserId
    idBox.TextColor3 = Color3.fromRGB(255, 255, 255)
    idBox.Font = Enum.Font.Gotham
    idBox.TextSize = 10 * fontSizeMult
    idBox.Parent = pages["Webhook"]
    Instance.new("UICorner", idBox).CornerRadius = UDim.new(0, 6 * selectedScale)
    idBox.FocusLost:Connect(function()
        settingsConfig.discordUserId = idBox.Text
        saveSettings()
    end)

    -- Misc Tab
    tgg(pages["Misc"], "Anti AFK", 0, "afk")
    tgg(pages["Misc"], "Anti Fling", 38, "antifling")
    tgg(pages["Misc"], "Auto Grab Gun", 76, "gun")
    tgg(pages["Misc"], "Auto Rejoin", 114, "autoRejoin")
    tgg(pages["Misc"], "Auto Serverhop (<= 4)", 152, "autoServerHop")
    tgg(pages["Misc"], "Auto Prestige (Level 100)", 190, "autoPrestige")

    -- UI Tab
    local scaleOptions = {1, 1.25, 1.5, 1.75, 2}
    local scaleTexts = {"1x", "1.25x", "1.5x", "1.75x", "2x"}

    local currentScaleIndex = 1
    for idx, scaleVal in ipairs(scaleOptions) do
        if scaleVal == selectedScale then
            currentScaleIndex = idx
            break
        end
    end

    local uiContainer = Instance.new("Frame")
    uiContainer.Size = UDim2.new(1, 0, 0, 32 * selectedScale)
    uiContainer.Position = UDim2.new(0, 0, 0, 0)
    uiContainer.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    uiContainer.Parent = pages["UI"]
    Instance.new("UICorner", uiContainer).CornerRadius = UDim.new(0, 6 * selectedScale)

    local uiLabel = Instance.new("TextLabel")
    uiLabel.Size = UDim2.new(0.5, 0, 1, 0)
    uiLabel.Position = UDim2.new(0, 8 * selectedScale, 0, 0)
    uiLabel.BackgroundTransparency = 1
    uiLabel.Text = "  UI Scale"
    uiLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
    uiLabel.Font = Enum.Font.GothamMedium
    uiLabel.TextSize = 11.5 * fontSizeMult
    uiLabel.TextXAlignment = Enum.TextXAlignment.Left
    uiLabel.Parent = uiContainer

    local plusBtn = Instance.new("TextButton")
    plusBtn.Size = UDim2.new(0, 28 * selectedScale, 0, 22 * selectedScale)
    plusBtn.Position = UDim2.new(1, -34 * selectedScale, 0.5, -11 * selectedScale)
    plusBtn.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
    plusBtn.Text = "+"
    plusBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    plusBtn.Font = Enum.Font.GothamBold
    plusBtn.TextSize = 12 * fontSizeMult
    plusBtn.Parent = uiContainer
    Instance.new("UICorner", plusBtn).CornerRadius = UDim.new(0, 4 * selectedScale)

    local valLabel = Instance.new("TextLabel")
    valLabel.Size = UDim2.new(0, 45 * selectedScale, 0, 22 * selectedScale)
    valLabel.Position = UDim2.new(1, -83 * selectedScale, 0.5, -11 * selectedScale)
    valLabel.BackgroundTransparency = 1
    valLabel.Text = scaleTexts[currentScaleIndex]
    valLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
    valLabel.Font = Enum.Font.GothamBold
    valLabel.TextSize = 11 * fontSizeMult
    valLabel.TextXAlignment = Enum.TextXAlignment.Center
    valLabel.Parent = uiContainer

    local minusBtn = Instance.new("TextButton")
    minusBtn.Size = UDim2.new(0, 28 * selectedScale, 0, 22 * selectedScale)
    minusBtn.Position = UDim2.new(1, -115 * selectedScale, 0.5, -11 * selectedScale)
    minusBtn.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
    minusBtn.Text = "-"
    minusBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    minusBtn.Font = Enum.Font.GothamBold
    minusBtn.TextSize = 12 * fontSizeMult
    minusBtn.Parent = uiContainer
    Instance.new("UICorner", minusBtn).CornerRadius = UDim.new(0, 4 * selectedScale)

    plusBtn.MouseButton1Click:Connect(function()
        if currentScaleIndex < #scaleOptions then
            currentScaleIndex = currentScaleIndex + 1
            selectedScale = scaleOptions[currentScaleIndex]
            buildUI()
        end
    end)

    minusBtn.MouseButton1Click:Connect(function()
        if currentScaleIndex > 1 then
            currentScaleIndex = currentScaleIndex - 1
            selectedScale = scaleOptions[currentScaleIndex]
            buildUI()
        end
    end)

    local fb = Instance.new("TextButton")
    fb.Size = UDim2.new(0, 75 * selectedScale, 0, 36 * selectedScale)
    fb.Position = UDim2.new(0, 15 * selectedScale, 0.3, 0)
    fb.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    fb.Text = "close"
    fb.TextColor3 = Color3.fromRGB(255, 255, 255)
    fb.Font = Enum.Font.GothamBold
    fb.TextSize = 12 * fontSizeMult
    fb.Parent = sg
    fb.ZIndex = 99999
    fb.Active = true
    fb.Draggable = true
    Instance.new("UICorner", fb).CornerRadius = UDim.new(0, 8 * selectedScale)

    local isOpen = true
    fb.MouseButton1Click:Connect(function()
        isOpen = not isOpen
        if isOpen then
            f.Visible = true
            TweenService:Create(f, TweenInfo.new(0.3), {Size = UDim2.new(0, baseWidth, 0, baseHeight)}):Play()
            fb.Text = "close"
        else
            TweenService:Create(f, TweenInfo.new(0.25), {Size = UDim2.new(0, baseWidth, 0, 0)}):Play()
            task.delay(0.25, function()
                if not isOpen then f.Visible = false end
            end)
            fb.Text = "open"
        end
    end)
end

buildUI()

if state.disable3d then
    applyLowDeviceOptimizations(true)
end

local function getCoins()
    local coins = {}
    for _, map in ipairs(Workspace:GetChildren()) do
        local cc = map:FindFirstChild("CoinContainer") or (map.Name == "CoinContainer" and map)
        if cc then
            for _, d in ipairs(cc:GetDescendants()) do
                if d:IsA("BasePart") and d:FindFirstChild("TouchInterest") then
                    table.insert(coins, d)
                end
            end
        end
    end
    return coins
end

local function isInRound()
    for _, map in ipairs(Workspace:GetChildren()) do
        if map:FindFirstChild("CoinContainer") or map.Name == "CoinContainer" then return true end
    end
    return false
end

local function isLobby()
    return not isInRound()
end

local function collectCoin(root, coin)
    if not root or not coin or not coin.Parent then return end
    pcall(function()
        for _ = 1, 3 do
            firetouchinterest(root, coin, 0)
            firetouchinterest(root, coin, 1)
        end
    end)
end

local function runBagFullAction()
    if busy then return end

    busy = true
    isExecutingAction = true
    bagFull = true

    local originalFarmState = state.farm
    local originalXpState = state.xpFarm
    state.farm = false
    state.xpFarm = false

    pcall(function()
        cancelFarmTween()
        totalCoinsEarned = totalCoinsEarned + currentCoinCount

        hideSky()
        task.wait(0.3)

        local role = getRole()

        if role == "Murderer" then
            if st then st.Text = " [AWhub] Bag full! Pulling knife & killing all..." end
            
            local knife = equipTool("Knife")
            if not knife then
                for _, v in ipairs(ReplicatedStorage:GetDescendants()) do
                    if v:IsA("Tool") and v.Name == "Knife" then
                        knife = v:Clone()
                        knife.Parent = LP.Character
                        break
                    end
                end
            end

            autoKillAllPlayers()

            if state.autoResetMurderer then
                triggerMenuReset()
                task.wait(1.5)
            end
        else
            local mur = getMurd()
            if mur and mur.Character then
                if st then st.Text = " [AWhub] Bag full! Flinging Murderer as " .. role .. "..." end
                reliableFling(mur)
            else
                if st then st.Text = " [AWhub] Bag full! Murderer not found to fling." end
            end

            hideSky()
            task.wait(0.3)

            if role == "Innocent" and state.autoResetInnocent then
                triggerMenuReset()
                task.wait(1.5)
            elseif role == "Sheriff" and state.autoResetSheriff then
                triggerMenuReset()
                task.wait(1.5)
            end
        end
    end)

    bagFull = false
    currentCoinCount = 0
    hasCollectedThisRound = false
    isExecutingAction = false
    busy = false
    
    task.wait(0.5)

    state.farm = originalFarmState
    state.xpFarm = originalXpState
end

task.spawn(function()
    local ok, remote = pcall(function()
        return ReplicatedStorage:WaitForChild("Remotes", 10):WaitForChild("Gameplay", 10):WaitForChild("CoinCollected", 10)
    end)
    if ok and remote then
        remote.OnClientEvent:Connect(function(_, currentCoins, maxCoins)
            if typeof(currentCoins) == "number" then
                currentCoinCount = math.clamp(currentCoins, 0, 50)
                if currentCoins > 0 then hasCollectedThisRound = true end
            end
            if typeof(maxCoins) == "number" then maxCoinCount = maxCoins end
            if typeof(currentCoins) == "number" and currentCoins <= 0 then
                currentCoinCount = 0
                bagFull = false
                return
            end
            if typeof(currentCoins) == "number" and currentCoins >= MIN_BAG_FULL and not isExecutingAction then
                task.spawn(runBagFullAction)
            end
        end)
    end
end)

task.spawn(function()
    while true do
        task.wait(0.4)
        local inRound = isInRound()
        local hasRoles = getMurd() ~= nil

        if (bagFull or isExecutingAction) and (not alive() or tick() - (lastCoinFoundTime or tick()) > 15) then
            bagFull = false
            isExecutingAction = false
            busy = false
            if st then st.Text = " [AWhub] Unstuck farm loop..." end
        end

        if not inRound then
            lastRoundState = false
            roundFullyStarted = false
            hasCollectedThisRound = false
            currentCoinCount = 0
            bagFull = false
            isExecutingAction = false
            busy = false
        end

        if inRound and hasRoles and not roundFullyStarted then
            if not lastRoundState then
                currentCoinCount = 0
                bagFull = false
                hasCollectedThisRound = false
                busy = false
                isExecutingAction = false
                roundStartTime = tick()
                lastRoundState = true
                if st then st.Text = " [AWhub] Map loaded..." end
            end
            if (tick() - roundStartTime) > 6 then
                roundFullyStarted = true
                if st then st.Text = " [AWhub] Round started" end
            end
        end
    end
end)

task.spawn(function()
    while true do
        task.wait(0.04)

        if not alive() then
            cancelFarmTween()
            continue
        end

        local root = LP.Character and LP.Character:FindFirstChild("HumanoidRootPart")
        local humanoid = LP.Character and LP.Character:FindFirstChildOfClass("Humanoid")
        if not root or not humanoid then continue end

        if state.xpFarm then
            cancelFarmTween()
            humanoid.PlatformStand = true
            root.Anchored = true
            root.CFrame = HIDE_POS
            root.AssemblyLinearVelocity = Vector3.zero
            root.AssemblyAngularVelocity = Vector3.zero
            continue
        end

        if not state.farm then
            cancelFarmTween()
            continue
        end

        if isLobby() or bagFull or isExecutingAction then
            cancelFarmTween()
            if not isExecutingAction and not next(activeResets) then
                humanoid.PlatformStand = true
                root.Anchored = true
                root.CFrame = HIDE_POS
                root.AssemblyLinearVelocity = Vector3.zero
            end
            lastCoinFoundTime = tick()
            continue
        end

        root.Anchored = false
        humanoid.PlatformStand = true
        humanoid.AutoRotate = false
        root.AssemblyLinearVelocity = Vector3.zero
        root.AssemblyAngularVelocity = Vector3.zero

        local coins = getCoins()
        
        if #coins > 0 then
            lastCoinFoundTime = tick()
        else
            if tick() - lastCoinFoundTime > NO_COIN_TIMEOUT then
                if st then st.Text = " [AWhub] No coins found timeout, resetting..." end
                cancelFarmTween()
                lastCoinFoundTime = tick()
                if not isLobby() then
                    triggerMenuReset()
                    task.wait(1.5)
                end
                continue
            end
        end

        if #coins == 0 then
            cancelFarmTween()
            continue
        end

        local closestCoin, shortest = nil, math.huge
        for _, c in ipairs(coins) do
            local dist = (root.Position - c.Position).Magnitude
            if dist < shortest then
                shortest = dist
                closestCoin = c
            end
        end
        
        if not closestCoin then 
            cancelFarmTween()
            continue 
        end

        local dist = (root.Position - closestCoin.Position).Magnitude

        if dist <= 7 then
            collectCoin(root, closestCoin)
        end

        if currentFarmTween and currentFarmTween.PlaybackState == Enum.PlaybackState.Playing and currentTargetCoin == closestCoin then
            collectCoin(root, closestCoin)
            continue
        end

        cancelFarmTween()
        currentTargetCoin = closestCoin

        local targetPos = closestCoin.Position + Vector3.new(0, -UNDER, 0)
        local targetCFrame = CFrame.new(targetPos) * CFrame.Angles(math.rad(90), 0, math.rad(180))
        local duration = math.clamp(dist / TWEEN_SPEED, 0.05, 3.3)

        currentFarmTween = TweenService:Create(
            root,
            TweenInfo.new(duration, Enum.EasingStyle.Linear),
            {CFrame = targetCFrame}
        )
        currentFarmTween:Play()

        farmVelocityConn = RunService.Heartbeat:Connect(function()
            if not root or not root.Parent then
                cancelFarmTween()
                return
            end
            root.AssemblyLinearVelocity = Vector3.zero
            root.AssemblyAngularVelocity = Vector3.zero
        end)
    end
end)

-- ==================== AUTO PRESTIGE (UI & REMOTE SUPPORT) ====================
local function getPrestigeRemote()
    local success, remote = pcall(function()
        if ReplicatedStorage:FindFirstChild("Remotes") then
            local remotes = ReplicatedStorage.Remotes
            if remotes:FindFirstChild("Inventory") and remotes.Inventory:FindFirstChild("Prestige") then
                return remotes.Inventory.Prestige
            end
            if remotes:FindFirstChild("Prestige") then
                return remotes.Prestige
            end
        end
    end)
    if success and remote then return remote end

    for _, v in ipairs(ReplicatedStorage:GetDescendants()) do
        if v.Name:lower():find("prestige") and (v:IsA("RemoteEvent") or v:IsA("RemoteFunction")) then
            return v
        end
    end
    return nil
end

local function mobileClickPrestige()
    local successAction = false
    pcall(function()
        local playerGui = LP:FindFirstChild("PlayerGui")
        if not playerGui then return end

        for _, ui in ipairs(playerGui:GetDescendants()) do
            if ui:IsA("TextButton") or ui:IsA("ImageButton") or ui:IsA("TextLabel") then
                local nameMatch = ui.Name:lower():find("prestige")
                local textMatch = false
                if ui:IsA("TextButton") or ui:IsA("TextLabel") then
                    textMatch = ui.Text:lower():find("prestige")
                end

                if nameMatch or textMatch then
                    local targetButton = ui
                    if not (targetButton:IsA("TextButton") or targetButton:IsA("ImageButton")) then
                        targetButton = ui:FindFirstAncestorWhichIsA("TextButton") or ui:FindFirstAncestorWhichIsA("ImageButton") or ui
                    end

                    local absPos = targetButton.AbsolutePosition
                    local absSize = targetButton.AbsoluteSize
                    local touchX = absPos.X + (absSize.X / 2)
                    local touchY = absPos.Y + (absSize.Y / 2)

                    if VirtualInputManager and pcall(function() VirtualInputManager:SendTouchEvent(0, 1, touchX, touchY, targetButton) end) then
                        VirtualInputManager:SendTouchEvent(0, 1, touchX, touchY, targetButton)
                        task.wait(0.05)
                        VirtualInputManager:SendTouchEvent(0, 2, touchX, touchY, targetButton)
                        successAction = true
                    end

                    if VirtualInputManager then
                        VirtualInputManager:SendMouseButtonEvent(touchX, touchY, 0, true, game, 0)
                        VirtualInputManager:SendMouseButtonEvent(touchX, touchY, 0, false, game, 0)
                        successAction = true
                    end

                    if targetButton:IsA("GuiButton") then
                        for _, conn in ipairs(getconnections(targetButton.MouseButton1Click)) do
                            conn:Fire()
                            successAction = true
                        end
                        for _, conn in ipairs(getconnections(targetButton.Activated)) do
                            conn:Fire()
                            successAction = true
                        end
                    end
                end
            end
        end
    end)
    return successAction
end

task.spawn(function()
    while true do
        task.wait(3)
        if state and state.autoPrestige then
            pcall(function()
                local leaderstats = LP:FindFirstChild("leaderstats")
                local levelVal = leaderstats and (leaderstats:FindFirstChild("Level") or leaderstats:FindFirstChild("Lvl"))
                
                if levelVal and levelVal.Value >= 100 then
                    local clickedUI = mobileClickPrestige()

                    local prestigeRemote = getPrestigeRemote()
                    if prestigeRemote then
                        if prestigeRemote:IsA("RemoteEvent") then
                            prestigeRemote:FireServer()
                        elseif prestigeRemote:IsA("RemoteFunction") then
                            prestigeRemote:InvokeServer()
                        end
                    end

                    if clickedUI or prestigeRemote then
                        if st then st.Text = " [AWhub] Auto prestiged!" end
                        task.wait(5)
                    end
                end
            end)
        end
    end
end)

-- ==================== AUTO REJOIN (FIXED) ====================
task.spawn(function()
    TeleportService.TeleportInitFailed:Connect(function(player, result, errorMessage)
        if player == LP and state.autoRejoin then
            task.wait(2)
            serverHop()
        end
    end)

    while true do
        task.wait(2)
        if state.autoRejoin then
            pcall(function()
                local promptGui = CoreGui:FindFirstChild("RobloxPromptGui")
                if promptGui then
                    local promptOverlay = promptGui:FindFirstChild("promptOverlay")
                    if promptOverlay then
                        for _, child in ipairs(promptOverlay:GetChildren()) do
                            if child.Name == "ErrorPrompt" then
                                serverHop()
                            end
                        end
                    end
                end
            end)
        end
    end
end)

RunService.Stepped:Connect(function()
    if LP.Character and not bagFull and not isExecutingAction and not isLobby() and not state.xpFarm and not next(activeResets) then
        for _, val in ipairs(LP.Character:GetDescendants()) do
            if val:IsA("BasePart") then val.CanCollide = false end
        end
    end
end)

RunService.Heartbeat:Connect(function()
    if not state.antifling or next(activeResets) or isExecutingAction then return end
    local root = LP.Character and LP.Character:FindFirstChild("HumanoidRootPart")
    local hum = LP.Character and LP.Character:FindFirstChildOfClass("Humanoid")
    if root and hum then
        local vel = root.AssemblyLinearVelocity
        if math.abs(vel.X) > 500 or math.abs(vel.Y) > 500 or math.abs(vel.Z) > 500 then
            root.AssemblyLinearVelocity = Vector3.zero
            root.AssemblyAngularVelocity = Vector3.zero
            hum.PlatformStand = false
        end
    end
end)

-- ==================== SERVER HOP ====================
task.spawn(function()
    while true do
        task.wait(3)
        if state.autoServerHop and #Players:GetPlayers() <= 4 and isLobby() then
            if st then st.Text = " [AWhub] Low player count in lobby, switching servers..." end
            serverHop()
            task.wait(10)
        end
    end
end)

task.spawn(function()
    while true do
        task.wait(0.15)
        if state.gun and alive() and not isExecutingAction and not findTool("Gun") then
            local root = LP.Character and LP.Character:FindFirstChild("HumanoidRootPart")
            if root then
                for _, v in pairs(Workspace:GetDescendants()) do
                    if v.Name == "GunDrop" and v:IsA("BasePart") then
                        pcall(function()
                            firetouchinterest(root, v, 0)
                            firetouchinterest(root, v, 1)
                        end)
                        break
                    end
                end
            end
        end
    end
end)

task.spawn(function()
    pcall(function()
        local vu = game:GetService("VirtualUser")
        LP.Idled:Connect(function()
            if state.afk then
                vu:CaptureController()
                vu:ClickButton2(Vector2.new())
            end
        end)
    end)
end)

print("Appleware loaded - enjoy my script also fuck you but have a good day (made by word)")"""


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user} (Synced {len(synced)} commands)")
    except Exception as e:
        print(e)


@bot.tree.command(name="script", description="Get the modded Roblox script to copy on PC or mobile.")
async def get_script(interaction: discord.Interaction):
    # Send a text file for mobile / easy download
    file_bytes = discord.File(
        fp=__import__("io").BytesIO(ROBLOX_SCRIPT.encode("utf-8")),
        filename="script.lua",
    )

    embed = discord.Embed(
        title=" Appleware's Script",
        description=(
            "Here is your script! PC users can copy directly from the code box"
            " below, and mobile users can download the attached file."
        ),
        color=0x2B2D31,
    )

    await interaction.response.send_message(
        embed=embed, file=file_bytes, ephemeral=False
    )

    # Send code block chunks if they want to copy via mobile chat box
    # Discord limits message length to 2000 chars, so we chunk it if necessary
    chunks = [
        ROBLOX_SCRIPT[i : i + 1900] for i in range(0, len(ROBLOX_SCRIPT), 1900)
    ]
    for chunk in chunks:
        await interaction.followup.send(f"```lua\n{chunk}\n```", ephemeral=True)


@bot.tree.command(
    name="farm", description="Start or stop the farm for a specific username."
)
@app_commands.describe(
    username="Your Roblox username",
    action="Choose whether to start or stop the farm",
)
@app_commands.choices(
    action=[
        app_commands.Choice(name="Start", value="start"),
        app_commands.Choice(name="Stop", value="stop"),
    ]
)
async def farm_control(
    interaction: discord.Interaction, username: str, action: app_commands.Choice[str]
):
    key = username.strip().lower()
    farm_states[key] = action.value == "start"

    status_text = (
        "🟢 Started" if action.value == "start" else "🔴 Stopped"
    )

    embed = discord.Embed(
        title="Farm Control Panel",
        description=(
            f"Successfully updated farm status for user **{username}**."
        ),
        color=0x00D26A if action.value == "start" else 0xED4245,
    )
    embed.add_field(name="Target Username", value=f"`{username}`", inline=True)
    embed.add_field(name="New Status", value=status_text, inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=False)


# Run the bot using the token environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print(
        "Error: DISCORD_TOKEN environment variable not set in Railway configuration!"
    )
