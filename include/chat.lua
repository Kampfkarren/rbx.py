RBXPY_PlayerChat = Instance.new("BindableEvent", script)
RBXPY_PlayerChat.Name = "RBXPY_PlayerChat" --Not necessary, but can be helpful

game.Players:PlayerAdded:connect(function(ply)
  ply.Chatted:connect(function(msg)
    RBXPY_PlayerChat:Fire(ply, msg)
  end)
end)
