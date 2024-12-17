import cv2 as cv

image = cv.imread(r'C:\Users\angel\OneDrive\Escritorio\IA\Tareas-Trabajos\waldocolor.jpg')
waldo = cv.imread(r'C:\Users\angel\OneDrive\Escritorio\IA\Tareas-Trabajos\waldo.jpg',0)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

result = cv.matchTemplate(gray, waldo, cv.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
buttom_ring = (max_loc[0] + 30, max_loc[1] + 30 )

cv.rectangle(image, max_loc, buttom_ring, (0,0,0),5)
cv.imshow("recuadro negro para encontrar a waldo", image)
cv.waitKey(0)
cv.imwrite(r"C:\Users\angel\OneDrive\Escritorio\IA\Tareas-Trabajos\waldoencontrado.jpg", image)
cv.destroyAllWindows()