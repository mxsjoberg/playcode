```
 ______  __       ______   __  __   ______   ______   _____    ______    
/\  == \/\ \     /\  __ \ /\ \_\ \ /\  ___\ /\  __ \ /\  __-. /\  ___\   
\ \  _-/\ \ \____\ \  __ \\ \____ \\ \ \____\ \ \/\ \\ \ \/\ \\ \  __\   
 \ \_\   \ \_____\\ \_\ \_\\/\_____\\ \_____\\ \_____\\ \____- \ \_____\ 
  \/_/    \/_____/ \/_/\/_/ \/_____/ \/_____/ \/_____/ \/____/  \/_____/ 
```

# PlayCode: A Playful Programming Language

PlayCode is procedural because knowing-how is more important than knowing-that, i.e. [street smarts](https://en.wikipedia.org/wiki/Procedural_knowledge). It will most likely be dynamically typed because no one have time for types anyway. There will be numbers, strings, lists, if-statements, for-loops, variables, and comments. There will probably also be a lot of things that are not yet decided.

Additionally, and more importantly, there will be two main features that will make PlayCode exciting:

- Tags `@<tag>` and goto tag `goto @<tag>` to enable any statement to become a function, so that basically every line can be called from anywhere in the program and return itself once. Imagine playing an instrument where each key or string can be played at any moment and always return some sound.

- Swaps `swap <a> <b>` to swap the values of two variables, which is useful for example when sorting.

Below are examples of valid programs.

```
print 42
```

```
x = 42
-- comment
if x < 0:
    print false
else
    print "positive"
end
```

```
-- swap
x = 2
y = 3
swap x y
print y == 2 -> true
```

```
-- tags
x = 0
@inc x++
goto @inc
print x -> 2
```

There are two ways to include comments, `--` and `->`, which also can be used as helpers in source for more readable code.
