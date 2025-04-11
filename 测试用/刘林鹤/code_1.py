from pandas.core.sample import process_sampling_size

list1 = [1, 2, 3, '4', 5]
num = 1
AAA = None
BBB = None

for x in list1:
    print('循环次数',num)
    xxtype = type(x)
    if num == 1:
        AAA = xxtype    # 记录第一位的AAA
        num += 1


    elif num == 2:
        BBB = xxtype  # 记录第二位的BBB
        if  AAA == BBB:
            print('前两个一致')
            num += 1  # 下一步

        elif AAA != BBB:
            print('前两个不一致')
            num += 1
    elif num > 2:

        if AAA != BBB:  # 如果前两位不一样

            if xxtype ==  AAA and xxtype !=  BBB: # 判断从第三位开始的，与第一位一致

                wd = num-1
                print(f'第{wd}个元素[{x}]是卧底]') # 那第二位就是卧底
                break
            elif xxtype ==  BBB and xxtype !=  AAA:
                wd = num-2
                print(f'第{wd}个元素[{x}]是卧底]') # 那第二位就是卧底
                break

        elif AAA == BBB:  # 如果前两位一样
            if xxtype ==  AAA : #与第一位一样
                num +=1   #进行下一位吧
            else:
                print(f'第{num}个元素[{x}]是卧底]') # 那这个位就是卧底
                break