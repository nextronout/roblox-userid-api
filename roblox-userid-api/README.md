# Roblox Username to UserID API

One-click deploy:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_GITHUB_USERNAME/roblox-userid-api&env=SETUP_PASSWORD&envDescription=Enter%20the%20password%20your%20Roblox%20server%20must%20send%20to%20use%20this%20API&project-name=roblox-userid-api&repository-name=roblox-userid-api)

## Roblox usage

```lua
local HttpService = game:GetService("HttpService")

local Username = "Builderman"
local Password = "YOUR_SETUP_PASSWORD"

local Response = HttpService:RequestAsync({
	Url = "https://YOUR-VERCEL-APP.vercel.app/api/userid",
	Method = "POST",
	Headers = {
		["Content-Type"] = "application/json"
	},
	Body = HttpService:JSONEncode({
		username = Username,
		password = Password
	})
})

local Data = HttpService:JSONDecode(Response.Body)

if Data.ok then
	print("Code " .. Data.code .. ", UserID: " .. Data.userId)
else
	print("Code " .. Data.code .. ", Reason: " .. Data.reason)
end