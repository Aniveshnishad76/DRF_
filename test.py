# from itertools import *
#
# var = "1222311"
#
# for i,j in groupby(list(var)):
#     print((len(list(j)), int(i)))

# list = [1, 3, 4, 5, 3, 6, 7, 9]
# area = 0
# for i in range(len(list)):
#     for j in range(i+1, len(list)):
#         area = max( area,min(list[j],list[i]) * (j-i) )
# print(area)

# strs = ["flower", "flow", "flight"]

# const = strs[0]
#
# for i in range(1,len(strs)):
#     temp = ""
#     for j in range(len(strs[i])):
#         if j < len(const) and const[j] == strs[i][j]:
#             temp = temp + const[j]
#     const = temp
#
# print(const)

# nums = [0,1]
# list =[]
# if len(nums) == 0:
#     list = []
# elif len(nums)< 3:
#     list = [0]
# else:
#     for i in range(len(nums)):
#         for j in range(i+1,len(nums)):
#             for k in range(j+1,len(nums)):
#                 if nums[i]+nums[j]+nums[k] == 0:
#                     test = [nums[i],nums[j],nums[k]]
#                     test.sort()
#                     if test not in list:
#                         list.append([nums[i],nums[j],nums[k]])
#
# print(list)
# importing the library
from PIL import Image
import matplotlib.pyplot as plt
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

image = Image.open("/home/my/PycharmProjects/AuthenticationSystem/static/user_profile/profile_default.jpeg")

# this open the photo viewer
# image.show()
width, height = image.size

draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/home/my/PycharmProjects/AuthenticationSystem/arial/arial.ttf', 40)
text = "testing purpose"
textwidth, textheight = draw.textsize(text, font)

# calculate the x,y coordinates of the text
margin = 5
x = width - textwidth - margin
y = height - textheight - margin
draw.text((x, y), text, font=font)
image.show()


#
# draw.text((0, 0), "Eyes", (0, 0, 0), font=font)
#
# plt.subplot(4, 7, 1)
# plt.title("black text")
# plt.imshow(watermark_image)
# watermark_image.show()
