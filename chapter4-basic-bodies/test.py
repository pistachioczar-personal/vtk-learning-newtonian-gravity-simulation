import numpy as np



v = np.random.rand(3)

velocity = v/np.linalg.norm(v)

print(*velocity)