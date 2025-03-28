
str1 = 'hello!,world!'

# 通过索引，获取输出感叹号

for x in str1:
    if x == '!':
        print(x)


# 通过切片获取输出感叹号

print(str1[str1.index('!')])

