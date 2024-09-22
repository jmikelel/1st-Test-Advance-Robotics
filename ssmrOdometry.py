import sys
import time
import numpy as np

# Clase Pose para almacenar la posición y orientación del vehículo
class Pose:
    def __init__(self, size):
        self.x = np.zeros(size)
        self.y = np.zeros(size)
        self.yaw = np.zeros(size)
    def update(self, newX, newY, newYaw):
        self.x = newX
        self.y = newY
        self.yaw = newYaw

# Clase Robot para almacenar las velocidades del vehículo y su orientación
class Robot:
    def __init__(self, xSpeed, ySpeed, turningVel):
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.turningVel = turningVel
    def update(self, newXSpeed, newYSpeed, newTurnSpeed):
        self.xSpeed = newXSpeed
        self.ySpeed = newYSpeed
        self.turningVel = newTurnSpeed

# Función que contiene las ecuaciones del modelo cinemático de un vehículo de tracción diferencial
def computeOdometry(index2Update, rotData, velocityData):
    # Obtener la pose anterior
    previousPose = np.array([
        [poseEstimation.x[index2Update-1]],
        [poseEstimation.y[index2Update-1]],
        [poseEstimation.yaw[index2Update-1]]
    ])
    # Actualizar la nueva pose
    velocitiesFactor = samplingRate * np.dot(rotData, velocityData)
    poseEstimation.x[index2Update] = previousPose[0] + velocitiesFactor[0]
    poseEstimation.y[index2Update] = previousPose[1] + velocitiesFactor[1]
    poseEstimation.yaw[index2Update] = previousPose[2] + velocitiesFactor[2]

# Función para calcular los parámetros del vehículo
def vehicleParameters(rightWheelSpeed, leftWheelSpeed, wheelRadius, widthValue):
    localXSpeed = (wheelRadius * rightWheelSpeed / 2) + (wheelRadius * leftWheelSpeed / 2)
    localTurninigSpeed = (wheelRadius * rightWheelSpeed / (2 * widthValue)) - (wheelRadius * leftWheelSpeed / (2 * widthValue))
    myRobot.update(localXSpeed, 0, localTurninigSpeed)
    localRobotSpeed = np.array([
        [myRobot.xSpeed],
        [myRobot.ySpeed],
        [myRobot.turningVel]
    ])
    return localRobotSpeed

# Función para calcular la matriz de rotación
def rotateAroundZ(previousYaw):
    cosResult = np.cos(previousYaw)
    sinResult = np.sin(previousYaw)
    rotZ = np.array([
        [cosResult, -sinResult, 0],
        [sinResult, cosResult, 0],
        [0, 0, 1]
    ])
    return rotZ

# Leer datos desde la entrada estándar (piping desde el programa C++)
data = list(map(float, sys.stdin.read().split()))
encoderPulsesPerRevolution = data[0]
pulsesPerSecond = data[1]
wheelRadius = data[2]
wheelWidth = data[3]
initialX = data[4]
initialY = data[5]
initialYaw = data[6]
elapsedTime = data[7]

# Configurar los parámetros físicos del robot diferencial
myRobot = Robot(0.0, 0.0, 0.0)

# Configuración de tiempo y tasa de muestreo
samplingRate = 0.25  # Frecuencia de muestreo
vectorSize = int((elapsedTime / samplingRate) + 1)
poseEstimation = Pose(vectorSize)

# Definir la pose inicial
currentIndex = 0
angleRadians = np.radians(initialYaw)
poseEstimation.x[currentIndex] = initialX
poseEstimation.y[currentIndex] = initialY
poseEstimation.yaw[currentIndex] = angleRadians

# Parámetros de las ruedas (velocidades simuladas)
rightSpeed = encoderPulsesPerRevolution * pulsesPerSecond * 2 * np.pi / 60
leftSpeed = rightSpeed  # Consideramos que ambas ruedas tienen la misma velocidad para esta simulación

# Configurar el tiempo inicial y final para la simulación
endTime = time.time() + elapsedTime
pastTime = time.time()

# Iniciar la estimación de pose
while time.time() <= endTime:
    currentTime = time.time()
    if (currentTime - pastTime) >= samplingRate:
        currentIndex += 1
        rotZMat = rotateAroundZ(poseEstimation.yaw[currentIndex - 1])
        robotSpeedData = vehicleParameters(rightSpeed, leftSpeed, wheelRadius, wheelWidth)
        computeOdometry(currentIndex, rotZMat, robotSpeedData)
        pastTime = currentTime

# Mostrar resultados
print("Pose Values: ")
print("x: ", poseEstimation.x)
print("y: ", poseEstimation.y)
print("yaw (rad): ", poseEstimation.yaw)
print("Angular Speed per Wheel (rad/s): ", rightSpeed / wheelRadius)
print("Linear Speed per Wheel (m/s): ", rightSpeed)
