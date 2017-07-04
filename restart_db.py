'''
4 Jul 17
author: svakulenko

DB maintaince script to init and/or clear the DB

'''

import quizz
quizz.db.drop_all()
quizz.db.create_all()
