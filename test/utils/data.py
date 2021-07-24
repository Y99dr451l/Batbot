import os

print(os.getcwd())
admins_file = open('test/utils/admins.txt', 'r')
admins = admins_file.read().split(',')
admins_file.close()
