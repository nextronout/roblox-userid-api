# Roblox Username to UserID API

One-click deploy:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/nextronout/roblox-userid-api&env=SETUP_PASSWORD&envDescription=Enter%20your%20private%20API%20password&project-name=roblox-userid-api&repository-name=roblox-userid-api)

## Server test page

When you open your deployed Vercel API in the browser, you should see:

```html
<h1>👾 Server is online 🟢</h1>
<p>Username → UserID conversion API</p>
```

## Roblox usage examples

<details>
<summary>UserID of Builderman</summary>

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
```

</details>
