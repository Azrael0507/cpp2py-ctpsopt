# cpp2py-ctpsopt
 transfer CTPsoptAPI from c++ to python

本项目为将CTP个股期权api转换为python模块版本的开源内容

项目目录说明：
项目下主要文件夹将以原始CTP个股期权api版本为分类，譬如首次更新为v361版本
同时会区分看穿式生产版本与看穿式评测版本（formal为生产版本，sim为评测版本）
在主版本目录下，是不同OS环境的打包内容：
Linux主要是在ubuntu20.04LTS最新环境下进行打包
Win主要是在VS2019cm版本中进行打包，也会标注python版本

项目运行环境说明：

推荐使用python3.8及以上的环境进行，初步运行测试方法如下
1、进入到trade或者md目录中
2、启动本地的python3环境
3、根据进入目录的不同，尝试import soptthostmduserapi/soptthosttraderapi 模块
导入无报错即可正常运行

常见错误处理：

1、在ubuntu20.04原始环境中，导入模块出现runtime问题
ubuntu20.04原始安装情况下，非常可能不包含中文编码包，而ctp的api是包含gb2312的中文编码的
因此需要通过如下命令进入设置，选中所有的中文编码进行重新生成：
#dpkg-reconfigure locales