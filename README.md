一．	项目简介
1.	三个微服务：用户可以在网页上利用邮箱注册账户，注册成功后可以登录进自己的账户。登录成功后可以发布微博客。 
2.	开发环境：Python Flask框架  
3. 部署步骤： 

a. 安装python3和任一python编译器。（我们使用的是PyCharm编译器）

b. 下载并解压“project”文件夹，并在编译器中打开。 

c. 利用python中的pip 安装“requirements.txt”中的包。 

d. 在本地mysql中创建数据库（数据库名字：project） 

e. 创建项目与数据库的连接及数据库中的表。 

f. 在python编译器中运行project.py文件，在浏览器中输入网址127.0.0.1:5000，点击“register”可以注册账户。注册成功后跳转到登录页面并在数据库中可以看到相应的信息。点击“Question”,用户可以在首页上发布微博客。

二．微服务实现

在实现微服务的时候我们借助了flask的BluePrint. 它可以帮助开发者将不同功能的module分开，从而将一个大的应用分割成各自实现不同功能的module，不同的蓝本需要对应不同的功能模块，并且它们位于不同的Python包中，而蓝图的创建则位于Python包下的init.py文件。不同Python包下的views Python文件对应不同蓝本下的路由，最后再在主程序中通过app.register_blueprint()方法将蓝图注册到URL映射中。在我们的项目中，我们在app文件夹下设置了三个API蓝本，每个蓝本都有各自的init Python 文件 用来创建蓝本并定义该蓝本的总URL，views模块写相关的业务逻辑，在template，static文件夹存储与该业务逻辑相关的界面文件。最后，我们将这三个蓝本注册到了我们的project主程序中。

三．ZooKeeper 部署
1. 原理

zookeeper提供了节点watch的功能，zookeeper的client（对外提供服务的server）监控zookeeper上的节点（znode），当节点变动的时候，client会收到变动事件和变动后的内容，基于zookeeper的这个特性，我们可以给服务器集群中的所有机器（client）都注册watch事件，监控特定znode，节点中存储部署代码的配置信息，需要更新代码的时候，修改znode中的值，服务器集群中的每一台server都会收到代码更新事件，然后触发调用，更新目标代码。也可以很容易的横向扩展，可以随意的增删机器，机器启动的时候注册监控节点事件即可。我的机器数量有限，在本地模拟zookeeper集群和服务器集群，原理都是一样的，可能具体实施的时候有些小异。在本机通过3个端口模拟zookeeper集群，多个目录模拟服务器集。

2.	Zookeeper配置

在三个zookeeper文件夹的conf文件夹下复制zoo_simple.cfg重命名为zoo.cfg,内容改为以下：

  zookeeper1文件下的zoo.cfg:
  dataDir=D:/zookeeper/zookeeper-3.4.10-colony/zookeeper-1/data
  dataLogDir=D:/zookeeper/zookeeper-3.4.10-colony/zookeeper-1/logs
  clientPort=2181
  server.1=192.168.1.108:2888:3888
  server.2=192.168.1.108:2889:3889
  server.3=192.168.1.108:2890:3890
 
  zookeeper2文件下的zoo.cfg:
  dataDir=D:/zookeeper/zookeeper-3.4.10-colony/zookeeper-2/data
  dataLogDir=D:/zookeeper/zookeeper-3.4.10-colony/zookeeper-2/logs
  clientPort=2182
  server.1=192.168.1.108:2888:3888
  server.2=192.168.1.108:2889:3889
  server.3=192.168.1.108:2890:3890
 
  zookeeper3文件下的zoo.cfg:
  dataDir=D:/zookeeper/zookeeper-3.4.10-colony/zookeeper-3/data
  dataLogDir=D:/zookeeper/zookeeper-3.4.10-colony/zookeeper-3/logs
  clientPort=2183
  server.1=192.168.1.108:2888:3888
  server.2=192.168.1.108:2889:3889
  server.3=192.168.1.108:2890:3890
 
3. 参数说明

 •	tickTime：基本事件单元，以毫秒为单位，用来控制心跳和超时，默认情况超时的时间为两倍的tickTime
 
 •	dataDir：数据目录.可以是任意目录.
 
 •	dataLogDir：log目录, 同样可以是任意目录. 如果没有设置该参数, 将使用和dataDir相同的设置.
 
 •	clientPort：监听client连接的端口号.
 
 •	maxClientCnxns：限制连接到zookeeper的客户端数量，并且限制并发连接数量，它通过ip区分不同的客户端。
 
 •	minSessionTimeout和maxSessionTimeout：最小会话超时时间和最大的会话超时时间，在默认情况下，最小的超时时间为2倍的tickTime时间，最大的会话超时时     间为20倍的会话超时时间，系统启动时会显示相应的信息。默认为-1
 
 •	initLimit：参数设定了允许所有跟随者与领导者进行连接并同步的时间，如果在设定的时间段内，半数以上的跟随者未能完成同步，领导者便会宣布放弃领导地位，进行另一次的领导选举。如果zk集群环境数量确实很大，同步数据的时间会变长，因此这种情况下可以适当调大该参数。默认为10
 
 •	syncLimit：参数设定了允许一个跟随者与一个领导者进行同步的时间，如果在设定的时间段内，跟随者未完成同步，它将会被集群丢弃。所有关联到这个跟随者的客 户端将连接到另外一个跟随着。
 
 在三个zookeeper文件夹下创建data文件夹，新建myid文件，分别在里面写入1，2，3.该myid文件没有后缀名。配置好文件后，在cmd分别开启三个节点的zookeeper进程即可
 
 开启三个cmd分别输入以下指令：

~cd D：\zookeeper-3.4.10-colony\zookeeper-1\bin
~zkServer.cmd

~cd D：\zookeeper-3.4.10-colony\zookeeper-2\bin
~zkServer.cmd

~cd D：\zookeeper-3.4.10-colony\zookeeper-3\bin
~zkServer.cmd
  
四．Dockers 部署

根据Dockerfile文件，在项目路径下输入命令“docker build -t miniblog .”创建镜像，在docker terminal中输入“docker images”可查看到所有镜像。

