import cv2
import imutils
import pytesseract


pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract"

#to read img
img=cv2.imread('honda_city.jfif')

#resizing and standarising our img
img=imutils.resize(img,width=500)

#displaying img
cv2.imshow("Original Image",img)
cv2.waitKey(0)

#convert img to gray scale to reduce the dimension and complexity of img
grayscale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Scale Image",grayscale)
cv2.waitKey(0)

#reducing noise from img to make it smooth
grayscale=cv2.bilateralFilter(grayscale,11,17,17)
cv2.imshow("Smooth Image",grayscale)
cv2.waitKey(0)

#finding edges of images
edge=cv2.Canny(grayscale,100,200)
cv2.imshow("Canny edge",edge)
cv2.waitKey(0)

#finding contours base on the images
contours,new=cv2.findContours(edge.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #new is heirarchy i.e. relationship
#RETR_LIST retrieves all contours but donot create relationship
#CHAIN_APPROX_SIMPLE removes all redundant pts.and compress contour by saving memory

#creating copy of original img to draw contours
img1=img.copy()
cv2.drawContours(img1,contours,-1,(0,255,0),3) #fixed values
cv2.imshow("Canny after Contouring",img1)
cv2.waitKey(0)

#we donot want all contours just the only ones on the number plate
# we will sort the area of the number plate as we can't locate directly
#we will also reverse the order of sorting in order to get from max area to min area

contours=sorted(contours,key=cv2.contourArea,reverse=True)[:30] #we will sort the top 30 areas
NumberPlateCount=None

img2=img.copy()
cv2.drawContours(img2,contours,-1,(0,255,0),3)
cv2.imshow("Top 30 Contours",img2)
cv2.waitKey(0)

#for the best possible contour of our number plate we will run afor loop
count=0
name=None

 #name of the cropped img
for i in contours:
    perimeter=cv2.arcLength(i,True)
    approx=cv2.approxPolyDP(i,0.02*perimeter ,True)
    #approxPolyDP approximates the curve of polygon with the precision
    if(len(approx)==4): 
        NumberPlateCount=approx
        #cropping te rectangular number plate part
        x,y,w,h=cv2.boundingRect(i)
        crp_img=grayscale[y:y+h,x:x+w]
        cv2.imwrite(str(name)+ ".png",crp_img)
        name+=1
        
        break

#draw contour in our original img

cv2.drawcontours(img, [NumberPlateCount], -1, (0,255,0), 3)

cv2.imshow("Final Image",blackandwhite_Img)
cv2.waitKey(0)

#crop only the part of the number plate
crop_img_loc='Np.png'
cv2.imshow("Cropped Image",cv2.imread(crop_img_loc))


text=pytesseract.image_to_string(crop_img_loc,lang='eng')

print("License Plate:",text.upper())

cv2.waitKey(0)