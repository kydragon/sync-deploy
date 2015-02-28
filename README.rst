test-service

简介:
-----

        在部署自动化方面, 有太多的形式, 也有更好的选择, 该APP的初衷是用程序自动化的形式来模拟实现以上人工
    的过程, 仅此而已.

依赖:
-----
    1, fabric 走 ssh 通道, 服务器要装 openssh-server.
    2, config.py 中的账户要有登陆及远程目录等等相应的权限.

使用:
-----

    模块介绍：
    ::

        service/conf.py         打包环境配置项
        service/utils.py        打包代码工具箱
        service/collector.py    打包功能模块
        service/compile.py      编译代码为字节码文件

    配置settings.py修改：
    ::

        # sync-deploy配置项
        CUSTOM_FABRIC_MODULE = 'demo.fab_upload'
        
        # INSTALLED_APPS 增加:
        'sync_deploy',


    django manage.py 命令项如下：
    ::

        $ python manage.py compile
        $ python manage.py forcecompile
        $ python manage.py namelower
        $ python manage.py upload
        $ python manage.py rollback
