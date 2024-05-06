import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import random


#개체 클래스 정의

class Light:
    def __init__(self, position, magnitude):
        self.position = position
        self.magnitude = magnitude

class Midge:
    def __init__(self, isMale, position):
        self.isMale = isMale
        self.position = position
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])
        self.acceleration = np.array([random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)])
    
    #개체의 가속도를 조정 - 주변 개체와 빛의 위치에 영향    
    def setacceleration(self, midgelist, lights):
        a = 0
        b = 1.0

        byPheromon = np.array([0, 0, 0])
        bylight = np.array([0, 0, 0])
        if self.isMale == True:
            for mi in midgelist:
                if self.isMale == False:
                    byPheromon = byPheromon + (mi.position - self.position) / (np.linalg.norm(mi.position - self.position) ** 3)

        for li in lights:
            bylight = bylight + li.magnitude * (li.position - self.position) / (np.linalg.norm(li.position - self.position) ** 3)

        targetPt = a * byPheromon + b * bylight
        if np.linalg.norm(targetPt) == 0:
            self.acceleration = targetPt
        else:
            self.acceleration = targetPt / np.linalg.norm(targetPt)

    #가속도에 따른 개체의 움직임 설정
    def refresh(self, dt):
        self.velocity += self.acceleration * dt
        self.velocity /= np.linalg.norm(self.velocity)
        self.position += self.velocity * dt


#광원 및 깔따구 개체 생성

lights = [Light(np.array([0, 0, 3]), 10), Light(np.array([0, 1, 2]), 5)]

midges = []
for i in range(20):
    midges.append(Midge(True, np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])))
    midges.append(Midge(False, np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])))


# 임의의 데이터 생성
num_points = 100

# 3D 그래프 초기화
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

size = 3

sc = ax.scatter([-size, size], [-size, size], [-size, size])

# 축 라벨링
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 애니메이션 함수 정의
def update(frame):
    x = []
    y = []
    z = []
    colors = []

    for mi in midges:
        mi.setacceleration(midges, lights)
        mi.refresh(1/30)
        x.append(mi.position[0])
        y.append(mi.position[1])
        z.append(mi.position[2])
        if mi.isMale:
            colors.append(0.3)
        else:
            colors.append(0.9)

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    colors = np.array(colors)
    sc._offsets3d = (x, y, z)
    sc._offsets3d = (x, y, z)
    sc.set_array(colors)
    return sc,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=range(30), interval=1000/30)

# 그래프 표시
plt.show()
