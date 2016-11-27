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
