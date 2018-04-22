# register and log in
项目简介：用户可以在网页上利用邮箱注册账户，注册成功后可以登录到自己的账户
编译环境：Python Flask框架 （我们使用的是Pycharm编译器）
部署步骤： 
  1.安装python3和任一python编译器
  2.下载并解压“project.zip”并在编译器中打开
  3.利用python中的pip 安装“requirements.txt”中的包。
    cmd命令：D:\大三\软件体系架构\project\venv\Scripts> activate
            (venv)D:\大三\软件体系架构\project\venv\Scripts> pip install -r requirements.txt
  4.在本地mysql中创建数据库（名字：project）
  5.创建项目与数据库的连接及数据库中的表
    cmd命令：D:\大三\软件体系架构\project> python manage.py.db init
            D:\大三\软件体系架构\project> python manage.py.db migrate
            D:\大三\软件体系架构\project> python manage.py.db upgrade
   （此时数据库中有一张表“user”）
  6.在python编译器中运行project.py文件，在浏览器中输入网址127.0.0.1:5000，点击“register”可以注册账户。注册成功后跳转到登录页面并在数据库中可以看到相应的信息。 
  
    
