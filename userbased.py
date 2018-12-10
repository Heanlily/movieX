# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 09:59:16 2018

@author: Lilylove Huang
"""
import random
from operator import itemgetter
import math
import matplotlib.pyplot as plt
import time
from const import BASE_PATH
import os
from util import timing


class CFalgo(object):
    def __init__(self, k):
        self.num_alikeuser = k
        self.num_movie = 5

        self.trainset = {}
        self.testset = {}

        self.usersim = {}
        self.movie_count = 0

    @timing
    def generate(self, filename, threshod=0.75):
        with open(filename, 'r', encoding='UTF-8') as f:
            for i, line in enumerate(f):
                if i == 0:                         # delete the first line
                    continue
                line = line.strip('\r\n')
                user, movie, rating, timestamp = line.split(',')
                if random.random() < threshod:
                    self.trainset.setdefault(user, {})
                    self.trainset[user][movie] = rating
                else:
                    self.testset.setdefault(user, {})
                    self.testset[user][movie] = rating

    @timing
    def calcu(self):
        movietouser = {}
        for user, movies in self.trainset.items():
            for movie in movies:
                if movie not in movietouser:
                    movietouser[movie] = set()
                movietouser[movie].add(user)

        self.movie_count = len(movietouser)

        for movie, users in movietouser.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.usersim.setdefault(u, {})
                    self.usersim[u].setdefault(v, 0)
                    self.usersim[u][v] += 1

        for u, linkedusers in self.usersim.items():
            for v, count in linkedusers.items():
                self.usersim[u][v] = count / math.sqrt(len(self.trainset[u]) * len(self.trainset[v]))

    @timing
    def recommend(self, user):
        mandr=[]
        K = self.num_alikeuser
        N = self.num_movie
        rank = {}
        watched_movies = self.trainset[user]

        movie_title = {}
        with open(os.path.join(BASE_PATH, "movies.csv"), 'r', encoding='UTF-8') as f:
            for i, line in enumerate(f):
                if i == 0:                         # delete the first line
                    continue
                line = line.strip('\r\n')
                movieid, title = line.split(',')[:2]
                movie_title[movieid] = title

        for v, wuv in sorted(self.usersim[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for movie in self.trainset[v]:
                if movie in watched_movies:
                    continue
                rank.setdefault(movie, 0)
                rank[movie] += wuv
        rank_movie = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]
        for i, v in rank_movie:
            mandr.append((movie_title[i], v))
        return rank_movie, mandr

    @timing
    def judge(self):
        N = self.num_movie
        hit = 0
        rec_count = 0

        for i, user in enumerate(self.trainset):
            tmp = 0
            test_movies = self.testset.get(user, {})
            rec_movies, mandr = self.recommend(user)
            for movie, w in rec_movies:
                if movie in test_movies:
                    hit += 1
                    tmp += 1
            rec_count += N

        rmse = ((rec_count-hit)/rec_count)**(1/2)
        precision = hit / (1.0 * rec_count)
        print('precisioin=%.4f' % precision)
        print('rmse=%.4f' % rmse)

        return precision


@timing
def get_recommendation(user_id):
    rating_file = os.path.join(BASE_PATH, "ratings.csv")
    user = CFalgo(70)
    user.generate(rating_file)
    user.calcu()
    return user.recommend("%s" % user_id)[1]


if __name__ == '__main__':
    print("recommendation for user: %s, %s", 71, get_recommendation(71))
