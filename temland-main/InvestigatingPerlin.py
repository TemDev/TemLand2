import noise
import matplotlib.pyplot as plt

graph = []

for x in range(128):
    z = noise.pnoise1(x * 0.1, repeat=99999) * 10
    graph.append(z if z > 0.49 else -1)

plt.imshow(graph, cmap='gray')
plt.show()
