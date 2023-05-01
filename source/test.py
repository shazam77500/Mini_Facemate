import cv2

print(0)

# Ouvre la caméra
cap = cv2.VideoCapture(0)
print(1)

# Capture une image
frame = cap.read()[1]
print(2)

# Enregistre l'image dans un fichier
cv2.imwrite("photo.jpg", frame)
print(3)

# Ferme la caméra
cap.release()
print(4)