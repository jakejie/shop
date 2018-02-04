#coding=utf-8
import recsys.algorithm
recsys.algorithm.VERBOSE=True

from recsys.algorithm.factorize import SVD


svd=SVD()
svd.load_data(filename='../data/movielens/ratings.csv',sep=',',format={'col':0,'row':1,'value':2,'ids':int})

#train,test=data.split_train_test(percent=70)
#svd=SVD()
#svd.set_data(train)

#假设奇异值的个数为100
k=100
svd.compute(k=k,min_values=1,pre_normalize=None,mean_center=False,post_normalize=True)
#svd.compute(k=k,min_values=10,pre_normalize=None,mean_center=True,post_normalize=True,savefile='/tmp/movielens')


#你可以计算两个电影的相似度
ITEMID1=3
ITEMID2=3
#svd.similarity(ITEMID1,ITEMID2)

print svd.similar(ITEMID1,ITEMID2)

#或者得到类似的电影
print svd.similar(ITEMID1)


#再预测一下用户对电影的评分
MIN_RATING=1.0
MAX_RATING=5.0
USERID1=30
print svd.predict(ITEMID1,USERID1,MIN_RATING,MAX_RATING)

#重头戏，推荐电影给用户！
print svd.recommend(USERID1,is_row=False)
#谁应该看这部电影
print svd.recommend(ITEMID1)