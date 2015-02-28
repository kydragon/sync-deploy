sync-deploy

简介:
-----
    在部署自动化方面, 有太多的形式, 也有更好的选择, 该package的初衷是用程序自动化的形式来模拟实现以上人工的过程, 仅此而已.

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
        CUSTOM_FABRIC_MODULE = 'demo.fabric'
        CUSTOM_FABRIC_UPLOAD = 'update_upload'
        CUSTOM_FABRIC_ROLLBACK = 'update_rollback'

        CUSTOM_IGNORE_FOLDER = ('deploy',)  # 忽略掉某些指定文件夹
        CUSTOM_FILTER_TYPE = ('.pyo', '.pyc', '.js', '.css', '.html', '.gif', '.jpg', '.png')  # 查找哪些类型的文件

        # noinspection PyUnresolvedReferences
        CUSTOM_FABRIC_ENV = {
            'project_path': BASE_DIR,  # 当前项目搜索目标
            'storage_path': os.path.join(BASE_DIR, r'archives'),  # 生成文件存放路径

            'filter_type': CUSTOM_FILTER_TYPE,
            'ignore_folder': CUSTOM_IGNORE_FOLDER,
            'dynamic_file_exist': None,  # 动态文件存在与否
        }
        
        # INSTALLED_APPS 增加:
        'sync_deploy',


    django manage.py 命令项如下：
    ::

        $ python manage.py compile
        $ python manage.py forcecompile
        $ python manage.py namelower
        $ python manage.py upload
        $ python manage.py rollback
