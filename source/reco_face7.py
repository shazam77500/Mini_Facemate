# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pymysql.cursors
import time
import pygame
import speech_recognition as sr
from aip import AipSpeech
import pymysql as MySQLdb
import os
import subprocess

##########################-- PARTIE JASON -############################

''' Configuration des clés d'API pour la synthèse vocale avec Baidu AI'''
SpeechAPP_ID = '17852430'
SpeechAPI_KEY ='eGeO4iQGAjHCrzBTYd1uvTtf'
SpeechSECRET_KEY = 'Cn1EVsUngZDbRLv4OxAFrDHSo8PsvFVP'
Speechclient = AipSpeech(SpeechAPP_ID, SpeechAPI_KEY, SpeechSECRET_KEY)

# Configuration du module de reconnaissance vocale
r = sr.Recognizer()
mic = sr.Microphone()

# Configuration de l'initialisation de la synthèse vocale avec Pygame
pygame.mixer.init()


# Définition de la fonction pour la synthèse vocale
def AudioPlay(phrase):
    # Appel à espeak pour générer le flux audio en français
    espeak_process = subprocess.Popen(["espeak", phrase, "-v", "fr", "-s", "110", "--stdout"], stdout=subprocess.PIPE)

    # Lecture du flux audio généré par espeak en utilisant aplay
    aplay_process = subprocess.Popen(["aplay"], stdin=espeak_process.stdout)

    # Attente de la fin de la lecture audio
    aplay_process.communicate()

# Définition de la fonction pour enregistrer les réponses de l'utilisateur
def enregistrer_reponse():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Parlez maintenant :")
        audio = r.listen(source)
    try:
        reponse = r.recognize_google(audio, language='fr-FR')
        print("Vous avez dit : {}".format(reponse))
        return reponse
    except sr.UnknownValueError:
        AudioPlay("Je n'ai pas compris, pouvez-vous répéter s'il vous plaît ?")
        return enregistrer_reponse()
    except sr.RequestError as e:
        AudioPlay("Je ne peux pas accéder au service Google Speech Recognition. Veuillez réessayer plus tard.")
        return enregistrer_reponse()


##########################-- PARTIE VINCENT -############################



# Connexion à la base de données
connection = pymysql.connect(
    host='localhost',
    user='root2',
    password='root',
    db='projet_nsi',
    charset='utf8mb4',
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

# Chargement du détecteur de visages
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Capture d'une image avec la webcam du Raspberry Pi
cap = cv2.VideoCapture(0)
ret, image = cap.read()

# Conversion de l'image en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Détection des visages dans l'image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

# Vérification des visages détectés
if len(faces) > 0:
    # Extraction des encodages des visages détectés
    encodings = []
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.resize(face, (160, 160))  # Redimensionnement de la face à la taille d'entrée du modèle
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)  # Conversion de la face en RGB
        encodings.append(face)

    encodings = np.array(encodings)

    # Récupération des encodages des visages stockés dans la base de données
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, visage FROM photos WHERE visage IS NOT NULL')
        results = cursor.fetchall()
        print(results)

        if results is not None:
            for result in results:
                id_personne = result['id']
                visage_encode = np.frombuffer(result['visage'], dtype=np.uint8)
                visage_encode = cv2.imdecode(visage_encode, cv2.IMREAD_COLOR)

                # Extraction des encodages des visages stockés dans la base de données
                visage_encode = cv2.resize(visage_encode, (160, 160))
                visage_encode = cv2.cvtColor(visage_encode, cv2.COLOR_BGR2RGB)
                visage_encode = np.expand_dims(visage_encode, axis=0)

                # Comparaison des encodages pour déterminer si c'est la même personne
                for i, encoding_visage in enumerate(encodings):
                    distance = np.linalg.norm(encodings - encoding_visage)
                    print("Distance entre le visage {} et le visage de {} : {}".format(i+1, id_personne, distance))


                    if distance < 0.6:  # Seuil de similarité (peut être ajusté)
                        index = np.argmin(distance)
                        id_personne = results[index]['id']
                        print("La même personne a été reconnue avec l'ID : ", id_personne)

                        ######JASON

                        AudioPlay("Bonjour {}. Comment allez-vous ?".format(id_personne))
                        reponse = enregistrer_reponse()
                        print("{} a répondu : {}".format(id_personne, reponse))
                        AudioPlay("Au revoir.")
                        time.sleep(3)
                        break

                        #####VINCENT

                        # Enregistrement de la nouvelle photo avec l'ID de la personne reconnue dans la base de données
                        with connection.cursor() as cursor:
                            cursor.execute('INSERT INTO photos (visage,id_personnes) VALUES (%s, %s)',
                                           (cv2.imencode('.jpg', image)[1].tobytes(),id_personne))

                            print("Nouvelle photo enregistrée avec l'ID de la personne reconnue : ", id_personne)

                else:
                    # Création d'une nouvelle personne dans la base de données
                    with connection.cursor() as cursor:

                        #####JASON########

                        # Pose de la première question avec synthèse vocale
                        AudioPlay("Bonjour, quel est votre prénom?")
                        prenom = enregistrer_reponse()

                        # Pose de la première question avec synthèse vocale
                        AudioPlay("Bonjour"+ prenom +"quel est votre nom de famille ?")
                        nom = enregistrer_reponse()

                        # Pose de la troisième question avec synthèse vocale
                        AudioPlay("Enchanté"+ prenom + nom +",""Quel est votre âge ?")
                        age = enregistrer_reponse()

                        #####VINCENT########

                        cursor.execute('INSERT INTO personnes (prenom,nom,age) VALUES (%s, %s,%s)',(prenom,nom,age))
                        id_personne = cursor.lastrowid
                        cursor.execute('INSERT INTO photos (visage,id_personnes) VALUES (%s, %s)',(cv2.imencode('.jpg', image)[1].tobytes(),id_personne))
                        print("Nouvelle personne créée avec l'ID : ", id_personne)

else:
    print("Aucun visage détecté dans l'image.")
    AudioPlay("Aucun visage détecté") #####JASON

# Fermeture de la connexion à la base de données
connection.close()

# Libération des ressources de la webcam
cap.release()
cv2.destroyAllWindows()
