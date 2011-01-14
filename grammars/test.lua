-- A comment in Lua starts with a double-hyphen and runs to the end of the line.
--[[ Multi-line strings & comments
     are adorned with double ] square brackets. ]]

function factorial(n)
  if n == 0 then
    return 1
  else
    return n * factorial(n - 1)
  end
end

print("Factorial of 5 is ", factorial(5))

function makeaddfunc(x)
  -- Return a new function that adds x to the argument
  return function(y)
    -- When we refer to the variable x, which is outside of the current
    -- scope and whose lifetime is longer than that of this anonymous
    -- function, Lua creates a closure.
    return x + y
  end
end
plustwo = makeaddfunc(2)
print(plustwo(5))  -- Prints 7

-- Creates a new table, with one associated entry. The string x mapping to
-- the number 10.
a_table = {x = 10}
-- Prints the value associated with the string key, in this case 10.
print(a_table["x"])
b_table = a_table
b_table["x"] = 20    -- The value in the table has been changed to 20.
print(b_table["x"])  -- Prints 20.
-- Prints 20, because a_table and b_table both refer to the same table.
print(a_table["x"])