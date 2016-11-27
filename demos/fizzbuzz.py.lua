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

for _,forloop_i in pairs(RBXPY_range(100)) do

if forloop_i % 15 == 0 then
print("FizzBuzz")
elseif forloop_i % 5 == 0 then
print("Buzz")
elseif forloop_i % 3 == 0 then
print("Fizz")
else
print(forloop_i)
end
end

