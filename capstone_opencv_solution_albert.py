import numpy as np
import cv2

def av_pix(img, circle, size):
    av_value = []
    for coords in circle[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size, coords[0]-size:coords[0]+size])
        # print(img[coords[1]-size:coords[1]+size, coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value

def get_radius(circles):
    radius = []
    for coords in circles[0,:]:
        radius.append(coords[2])
    return radius

img = cv2.imread('capstone-coins.png',cv2.IMREAD_GRAYSCALE)
original_image = cv2.imread('capstone-coins.png', 1)
img = cv2.GaussianBlur(img, (5,5), 0)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 120, param1=50, param2=27,minRadius=60,maxRadius=120)
print(circles)

circles = np.uint16(np.around(circles))
print(circles)
count = 1
print(circles[0,:])
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(original_image,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(original_image,(i[0],i[1]),2,(0,0,255),3)
    # cv2.putText(original_image, str(count), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count +=1

radii = get_radius(circles)
print(radii)

bright_values = av_pix(img, circles,20)
print(bright_values)

values = []
for a,b in zip(bright_values, radii):
    if a>150 and b>110:
        values.append(10)
    elif a > 150 and b <= 110:
        values.append(5)
    elif a < 150 and b >110:
        values.append(2)
    elif a < 150 and b < 110:
        values.append(1)
print(values)


# # Converting image to a binary image
# # (black and white only image)
# # Start
# _,threshold = cv2.threshold(img, 110, 255,
#                             cv2.THRESH_BINARY)

# # Detecting shapes in image by selecting region
# # with same colors or intensity.
# contours,_ = cv2.findContours(threshold, cv2.RETR_TREE,
#                                 cv2.CHAIN_APPROX_SIMPLE)
# # Searching through every region selected to
# # find the required polygon.
# for cnt in contours:
#     approx = cv2.approxPolyDP(cnt,  
#                                   0.009 * cv2.arcLength(cnt, True), True) 
#     if (len(approx) >= 7):
#         cv2.drawContours(original_image, [approx], 0, (0, 0, 255), 5) 


# # End
count_2 = 0
for i in circles[0,:]:
    cv2.putText(original_image, str(values[count_2]) + 'p',(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count_2 += 1
cv2.putText(original_image, 'ESTIMATED TOTAL VALUE: ' + str(sum(values)) + 'p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255)

cv2.imshow('Detected Coins', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()