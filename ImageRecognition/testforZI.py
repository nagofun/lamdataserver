import tensorflow as tf
import os
import cv2

from numpy.random import RandomState

IMAGE_StandSize = (22, 22)

def readData(PositiveRootDir,NegativeRootDir):
    X=[]    # 图片输入
    Y=[]    # 标签列表
    list = os.listdir(PositiveRootDir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(PositiveRootDir, list[i])
        # fpath, fname = os.path.split(path)
        if os.path.isfile(path):
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            # print(image)
            temp = [[item/255.0 for item in line] for line in image]
            temp2 = []
            for line in temp:
                temp2.extend(line)
            X.append(temp2)
            Y.append([1, 0])


    list = os.listdir(NegativeRootDir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(NegativeRootDir, list[i])
        # fpath, fname = os.path.split(path)
        if os.path.isfile(path):
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, IMAGE_StandSize)
            # print(image)
            temp = [[item / 255.0 for item in line] for line in image]
            temp2 = []
            for line in temp:
                temp2.extend(line)
            X.append(temp2)
            Y.append([0, 1])
    return [X, Y]


X, Y = readData(r'E:\chenbo\Program\14-PrintScreen\template\cut1\auto',r'E:\chenbo\Program\14-PrintScreen\template\cut1\others')

batch_size = 8

# 定义神经网络参数
w1 = tf.Variable(tf.random_normal([484, 10], stddev=2, seed=1))
w2 = tf.Variable(tf.random_normal([10, 2], stddev=2, seed=1))

#
x = tf.placeholder(tf.float32, shape=(None, 484), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None, 2), name='y-input')

# 定义神经网络前向传播的过程
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

# 定义损失函数和反向传播的算法
cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

# 计算正确率
# correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y_, 1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# 创建一个会话来运行TensoeFlow程序。
with tf.Session() as sess:
    init_op = tf.initialize_all_variables()
    # 初始化变量
    sess.run(init_op)

    print(sess.run(w1))
    print(sess.run(w2))

    # 设定训练的轮数
    STEPS = 5000
    for i in range(STEPS):
        sess.run(train_step, feed_dict={x:X, y_:Y})
        if i%1000 == 0:
            # 每隔一段时间计算在所有数据上的交叉熵并输出
            total_cross_entropy = sess.run(
                cross_entropy, feed_dict={x:X, y_:Y}
            )
            print("After %d training step(s), cross entropy on all data is %g"%(i, total_cross_entropy))

            # validate_acc = sess.run(accuracy, feed_dict={x:X, y_:Y})
            # test_acc = sess.run(accuracy, feed_dict={x:X, y_:Y})
            # print("After %d training steps, validation accuracy"
            #       "using average model is %g, test accuracy"
            #       "using average model is %g " % (i, validate_acc, test_acc))

    # print(sess.run(w1))
    print(sess.run(w2))

# with tf.Session() as sess:
#
#     _a = tf.matmul(tf.constant([X[0]]), w1)
#     _y = tf.matmul(_a, w2)
#     print(sess.run(_y))