import matplotlib.pyplot as plt
import numpy as np

# plt.style.use('_mpl-gallery')

# # make data
# x = np.linspace(0, 10, 100)
# y = 4 + 2 * np.sin(2 * x)

# # plot
# fig, ax = plt.subplots()

# ax.plot(x, y, linewidth=2.0)
# fig.suptitle('Figure')

# ax.set_xlabel("episode trained")
# ax.set_ylabel("average reward")


# plt.show()
level = np.arange(1,10.1,0.5)
level_reward = np.zeros(len(level))
print(len(level))
