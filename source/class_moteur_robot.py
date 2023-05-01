from Raspblock import Raspblock

robot=Raspblock()

#robot.Servo_control_single(2,1500)
#robot.Servo_control(1500,1150)
#del robot

class robot:
    __robot = 0
    __nvertical = 0
    __nhorizontal = 0



    def __init__(self,robot,nv,nh):
        self.__robot = robot
        self.__nvertical = nv
        self.__nhorizontal = nh


    def avant(self):
        #test avec la première méthode pour avancer
        for i in range(1000):
            self.__robot.Speed_Wheel_control(2,2,2,2)



    def arriere(self):
        #test avec la première méthode pour reculer
        for i in range(1000):
            self.__robot.Speed_Wheel_control(-2,-2,-2,-2)


    def gauche(self):
        #test avec la première méthode pour tourner à gauche
        for i in range(1000):
            self.__robot.Speed_Wheel_control(2,-2,2,-2)


    def droite(self):
        #test avec la première méthode pour tourner à droite
        for i in range(1000):
            self.__robot.Speed_Wheel_control(-2,2,-2,2)


##Code non utilisé :

    def rotation_horaire(self):
        #test avec la premère méthode pour faire une rotation horaire
        for i in range(2000):
            self.__robot.Speed_Wheel_control(-2,-2,2,2)

    def rotation_trigo(self):
        #test avec la première méthode pour faire une rotation trigo
        for i in range(2000):
            self.__robot.Speed_Wheel_control(2,2,-2,-2)

    def cam_initial(self):
        #Position initial de la caméra
        self.__robot.Servo_control(1500,1500)


    def haut_cam(self):
        #caméra se déplaçant vers le haut
        self.__nvertical-=100
        self.__robot.Servo_control_single(2,self.__nvertical)


    def bas_cam(self):
        #caméra se déplaçant vers le bas
        self.__nvertical+=100
        self.__robot.Servo_control_single(2,self.__nvertical)


    def droite_cam(self):
        #caméra se déplaçant vers la droite
        self.__nhorizontal-=100
        self.__robot.Servo_control_single(1,self.__nhorizontal)


    def gauche_cam(self):
        #caméra se déplaçant vers la gauche
        self.__nhorizontal+=100

        self.__robot.Servo_control_single(1,self.__nhorizontal)


