import cv2, pyautogui
from PIL import Image

# img = cv2.imread(r'C:\Users\USER\Desktop\strixsmoke.jpeg', 1)
# img2 = cv2.imread(r'C:\Users\USER\Desktop\image.png', -1)
# cv2.imshow("image",img)
# cv2.waitKey(0)
# # cv2.imshow("image",img2)
# # cv2.waitKey(10)

screenshot = pyautogui.screenshot()

screenshot.save(r"C:\Users\USER\Desktop/screenshotimage.png")

img = cv2.imread(r'C:\Users\USER\Desktop/screenshotimage.png', -1)
cv2.imshow("image",img)
cv2.waitKey(1000)
