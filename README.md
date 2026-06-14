# Roblox Username to UserID API

One-click deploy:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/nextronout/roblox-userid-api&env=SETUP_PASSWORD&envDescription=Enter%20your%20private%20API%20password&project-name=roblox-userid-api&repository-name=roblox-userid-api)

## Server test page

When you open your deployed Vercel API in the browser, you should see:

```html
<h1>👾 Server is online 🟢</h1>
<p>Username → UserID conversion API</p>
```

## Roblox usage

Make sure to have "Allow HTTP Requests" and "Enable Studio Access to API Services" are enabled in Roblox Studio's Experience Settings.
<img width="1187" height="780" alt="image" src="https://github.com/user-attachments/assets/34590533-d552-4fb6-9a21-b9c4c6822e3b" />

Create a new Script inside ServerScriptService and paste one of the scripts below to test the API.

<details>
<summary>UserID of Builderman</summary>

```lua
local HttpService = game:GetService("HttpService")

local Username = "Builderman"
local API_URL = "https://YOUR-VERCEL-APP.vercel.app/api/userid"
local PASSWORD = "YOUR_SETUP_PASSWORD"

local Response = HttpService:RequestAsync({
	Url = API_URL,
	Method = "POST",
	Headers = {
		["Content-Type"] = "application/json"
	},
	Body = HttpService:JSONEncode({
		username = Username,
		password = PASSWORD
	})
})

local Data = HttpService:JSONDecode(Response.Body)

if Data.ok then
	print("Code " .. Data.code .. ", UserID: " .. Data.userId)
else
	print("Code " .. Data.code .. ", Reason: " .. Data.reason)
end
```
Description:

If the server is set up correctly, this script should return Builderman's UserID.
```
Code 200, UserID: 156  -  Server - Script:22
```

</details>

<details>
<summary>UserID on Player Join</summary>

```lua
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local DataStoreService = game:GetService("DataStoreService")

local UserIdStore = DataStoreService:GetDataStore("UsernameToUserIdCache")

local API_URL = "https://YOUR-VERCEL-APP.vercel.app/api/userid"
local PASSWORD = "YOUR_SETUP_PASSWORD"

local function createUserIdValue(player, userId)
	if player:FindFirstChild("GlobalUserId") then
		return
	end
	
	local old = player:FindFirstChild("GlobalUserId")
	if old then
		old:Destroy()
	end

	local value = Instance.new("NumberValue")
	value.Name = "GlobalUserId"
	value.Value = tonumber(userId)
	value.Parent = player
end

local function getUserIdFromAPI(username)
	local requestSuccess, response = pcall(function()
		return HttpService:RequestAsync({
			Url = API_URL,
			Method = "POST",
			Headers = {
				["Content-Type"] = "application/json"
			},
			Body = HttpService:JSONEncode({
				username = username,
				password = PASSWORD
			})
		})
	end)

	if not requestSuccess then
		return false, 0, "HTTP request failed: " .. tostring(response)
	end

	local success, data = pcall(function()
		return HttpService:JSONDecode(response.Body)
	end)

	if not success then
		return false, response.StatusCode, "Response was not JSON: " .. tostring(response.Body)
	end

	if data.ok then
		return true, data.code or response.StatusCode, data.userId
	else
		return false, data.code or response.StatusCode, data.reason or "Unknown error"
	end
end

Players.PlayerAdded:Connect(function(player)
	local username = player.Name
	local key = "GlobalUserId_" .. string.lower(player.Name)

	local dataStoreSuccess, cachedUserId = pcall(function()
		return UserIdStore:GetAsync(key)
	end)

	if dataStoreSuccess and cachedUserId then
		createUserIdValue(player, cachedUserId)
		print("UserID was found in the DataStore:", username, cachedUserId)
		return
	end

	local apiSuccess, code, result = getUserIdFromAPI(username)

	if not apiSuccess then
		warn("Code " .. tostring(code) .. ", Reason: " .. tostring(result) .. " | failed to retrieve UserID of " .. player.Name)
		return
	end

	local userId = result

	local saveSuccess, saveError = pcall(function()
		UserIdStore:SetAsync(key, userId)
	end)

	if not saveSuccess then
		warn("Failed to save UserID to DataStore for " .. player.Name .. ": " .. tostring(saveError))
	end

	createUserIdValue(player, userId)
	print("UserID successfully retrieved via API:", username, userId)
end)
```
Description:

When a player joins the game, the script first checks DataStores for a saved UserID.
If no saved UserID is found, an HTTP request is sent to the server to retrieve the player's UserID.
Once retrieved, the UserID is saved to DataStores and becomes available as:
```lua
Players.Player.GlobalUserId.Value
```
<img width="335" height="203" alt="image" src="https://github.com/user-attachments/assets/58bd87f6-698c-4196-8760-ac349cc31ab2" />

</details>
