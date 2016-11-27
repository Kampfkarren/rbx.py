--This was Python code that was transpiled into Lua by rbx.py. Go to http://github.com/boynedmaster/rbx.py for more information.
function RBXPY_range(numa, numb, step)
  step = step or 1
  ret = {}

  if numb == nil then
    for i=0,numa - 1,step do
      table.insert(ret, i)
    end
  else
    for i=numa,numb - 1,step do
      table.insert(ret, i)
    end
  end

  return ret
end

for _,forloop_i in pairs(RBXPY_range(5)) do
print(forloop_i)
end
print("--------------------")
for _,forloop_i in pairs(RBXPY_range(3, 7)) do
print(forloop_i)
end
print("--------------------")
for _,forloop_i in pairs(RBXPY_range(2, 7, 2)) do
print(forloop_i)
end

