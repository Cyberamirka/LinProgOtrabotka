# # библиотеки
# from pprint import pprint
# import math


# # модули
# from CoderMethods.baseFunctions import *
# from CoderMethods.Fano import ShannonFano
# from CoderMethods.Haffman import Huffman



# test = "Hello"
# msg1 = "КРАСНАЯ КРАСКА - КРАСИВАЯ ПОКРАСКА"
# msg2 = "КРАСНАЯ КРАСКА"


# code_table, iters = Huffman(CharPatternFinder(test))
# code = coder_decoder(code_table, test)
# decode = coder_decoder(code_table, code, decode_mode=True)
# print(code, decode)
# table = []
# print()
# print()

# table.append(["Символ", "Pi"] * len(iters) + ["коды", "qi", "Pi*qi", "-Pi*log(Pi)"])
# t = iters[0]

# for i in range(len(iters)):
#     table.append([])
#     for j in range(len(iters[i])):
#         table[-1].append(iters[j][i][0])
#         table[-1].append(iters[j][i][1])
#     table[-1] += [None, None] * (len(iters) - len(iters[i]))

#     code = code_table.toDict()[t[i][0]]
#     table[-1].append(code)
#     frequency = t[i][1]
#     table[-1].append(len(code))
#     table[-1].append(frequency * len(code))
#     table[-1].append(-frequency * math.log2(frequency))

#     print(table[-1])


code = "10101010100001011100101"
crc = "10011"
print(code[:-(len(crc))])
