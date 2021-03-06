from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

# model 과 serializers import
from .serializers import PostSerializer
from .models import Post
from .serializers import AccountsSerializer
from .models import Accounts

from django.core.files.storage import FileSystemStorage

# for deep learning model
import os
from tensorflow.keras.preprocessing.image import load_img
import threading
import random
import string
import time
# added
from pathlib import Path


class AccountsViewset(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer


class CheckAccountViewset(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer

    def create(self, request):
        post_data = request.data
        print('Posted from ANDROID')
        print(post_data)

        checkID = post_data['checkID']
        checkPW = post_data['checkPW']

        # me = Accounts.objects.filter(identify='sewon')

        if Accounts.objects.filter(identify=checkID).exists():
            if Accounts.objects.filter(password=checkPW).exists():
                print('yay')
                return Response(status=200)

        return Response(status=400)


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):  # Here is the new update comes <<<<
        programStart1 = time.time()
        post_data = request.data
        fileObj = request.FILES['image']
        userAccount = post_data['title']
        category = post_data['category']

        print('-----------')
        print('POST DATA : ' + str(post_data))
        print('FILE OBJECT : ' + str(request.FILES['image']))
        file_name = str(request.FILES['image'])
        file_name = file_name.split('.')
        # 여기서 file_name 은 안드로이드에서 들어온 항상 같은 file_name == "hihi.jpeg"를 split한 "hihi"

        # file_url = file_name[0] + '_.png'
        # 랜덤한 값으로 넣어주기 위해서 file_url 값을 정한다.
        letters = string.ascii_lowercase
        file_url = ''.join(random.choice(letters) for i in range(5)) + '.png'
        # file_name = file_url
        print('FILE URL : ' + str(file_url))

        # images 에 이름은 항상 hihi 로 들어가도록
        file_name = file_name[0]
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        print('filePathName is ' + str(filePathName))
        testimage = '.' + filePathName  # media에 저장된 이미지 이름인데..
        print('testimage is ' + str(testimage))

        img = load_img(testimage)
        directory = os.path.join(os.getcwd(), 'bg_removal/images' + os.sep)  # + os.sep 이거 붙여줘야함
        img.save(directory + file_name + '.jpg')  # image 폴더에 저장

        # thread = threading.Thread(target=self.hiya, args=(file_url, programStart1))
        # thread.daemon = True
        # thread.start()
        command = 'python C:/Users/sewon/django_test/mytestsite/bg_removal/u2net_test.py ' + str(file_url)
        # command = 'python /srv/mytestsite/bg_removal/u2net_test.py ' + str(file_url)
        os.system(command)
        programFinish = time.time()
        print('duration of image processing : ')
        print(programFinish - programStart1)

        # DB 테이블에 직접 값 넣어주기
        db_file_url = file_url
        Subs = Post.objects.create(title=userAccount, category=category, image=db_file_url)
        Subs.save()
        # print('duration of image processing : ')
        # print(programFinish - programStart1)
        return Response(data='heyhey')
        # return Response(data=str(testimage))

    def hiya(self, file_url, start_time):
        # 이 부분은 multithreading 으로 처리해야겠다.
        # 근데 일단 create메소드 안에 들어가는 순간 mysql에는 안 들어가니까 create 메소드 안에 뭔가를 추가해줘야 할 것 같다.
        # BASE_DIR = Path(__file__).resolve().parent.parent
        # os.path.join(BASE_DIR)
        print('CURRENT DIRECTORY : ' + str(os.path.join(os.getcwd())))
        command = 'python C:/Users/sewon/django_test/mytestsite/bg_removal/u2net_test.py ' + str(file_url)
        # command = 'python /srv/mytestsite/bg_removal/u2net_test.py ' + str(file_url)
        os.system(command)
        programFinish = time.time()
        print('duration of image processing : ')
        print(programFinish - start_time)
