import numpy as np
import matplotlib.pyplot as plt


marray = np.array([[[220.15405367, -18.08810878],
                    [210.01099842, -33.42300943],
                    [227.68870042,  20.44911701],
                    [207.18261805, -12.90083466],
                    [200.11156063,  11.57822475],
                    [199.40443956,  21.54552652],
                    [213.54656999,  24.46142093],
                    [200.81864793,  50.44217636],
                    [200.11155283,  83.93503198],
                    [235.46685553, -17.76314432],
                    [235.46684514,   2.79109193],
                    [207.18251675,   1.09113239],
                    [222.73894905,  20.25448392],
                    [222.03183058,  43.05324106],
                    [224.8602629,  73.91229793],
                    [211.42521198, -32.55698594],
                    [212.83943074, -26.81264672],
                    [210.01099842, -33.42300943],
                    [213.54653882, -30.78921719]]])


fig = plt.figure()
#ax = fig.add_subplot(111, projection='2d')


print(marray)

newarray = marray.reshape(-1,2)

print(newarray)
# for element in marray[0]:
#     #print("X: {}, Y: {}".format(element[0], element[1]))
#     #ax.scatter(element[0], element[1])
#     plt.scatter(element[1], element[0])


# # ax.set_xlabel('X')
# # ax.set_ylabel('Y')
# # ax.set_zlabel('Z')

# plt.show()
# # plot_keypoints(marray[0])
