RBXPY_Bit = {
    Has = function(number, bit)
        return number % (bit * 2) >= bit
    end,

    And = function(ca, cb)
        local new = 0
        for i = 0, 31 do
            new = new + ((RBXPY_Bit.Has(ca, 2^i) and RBXPY_Bit.Has(cb, 2^i)) and 2^i or 0)
        end
        return new
    end,

    Or = function(ca, cb)
        local new = 0
        for i = 0, 31 do
            new = new + ((RBXPY_Bit.Has(ca, 2^i) or RBXPY_Bit.Has(cb, 2^i)) and 2^i or 0)
        end
        return new
    end,

    RShift = function(num, times)
        return math.floor(num * 0.5 ^ (times or 1))
    end,

    LShift = function(num, times)
        return num * 2 ^ (times or 1)
    end,

    Xor = function(ca, cb)
        local new = 0
        for i = 0, 31 do
            new = new + ((RBXPY_Bit.Has(ca, 2^i) ~= RBXPY_Bit.Has(cb, 2^i)) and 2^i or 0)
        end
        return new
    end
}
