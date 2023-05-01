import mysql.connector

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root2",
    password="root",
    database="projet_nsi"
)

# Création de la table "personnes"
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE personnes (id INT AUTO_INCREMENT PRIMARY KEY, prenom VARCHAR(255), nom VARCHAR(255), age INT)")

# Création de la table "photos"
mycursor.execute("CREATE TABLE photos (id INT AUTO_INCREMENT PRIMARY KEY, visage LONGBLOB, id_personnes INT, FOREIGN KEY (id_personnes) REFERENCES personnes(id))")

print("Tables créées avec succès!")
