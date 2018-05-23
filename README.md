#Eros Update

## 安装

  前提环境：`CentOS`,`Python3.6`,`Pipenv`

  > 关于pipenv，可以参考[使用pipenv管理python虚拟环境](https://vimiix.com/post/2018/03/11/manage-your-virtualenv-with-pipenv/)

  ###安装Python3.6、Pipenv

    1. 安装依赖
    
      ```Bash
      yum -y install sqlite-devel
      yum install -y bzip2*
      ```
    2. 编译安装Python3.6

      ```Bash
      wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
      tar -zvxf Python-3.6.5.tgz
      cd Python-3.6.5
      ./configure --enable-loadable-sqlite-extensions --enable-optimizations
      make
      make install
      ```
    3. 安装Pipenv 

      ```Bash
      pip3 install pipenv
      ```
  
  1. 下载代码

  ```
  git clone https://github.com/mylonly/ErosUpdate.git
  ```

  2. 创建虚拟环境以及安装依赖

  ```
  cd ErosUpdate
  pipenv install --three
  ```
  
  3. 激活pipenv虚拟环境

  ```
  pipenv shell
  ```

  4. 初始化项目

  ```
  python3 manager.py makemigrations
  python3 manager.py migrate
  python3 manager.py createsuperuser
  ```
  5. 运行dev环境

  ```
  python3 manager.py runserver
  ```
  
  6. VSCode下debug
  
  ```
  #修改vscode的setting中的,具体地址为你自己对应虚拟环境的路径
  "python.pythonPath": "~/.local/share/virtualenvs/ErosUpdate-J6EmTYWq/bin/python3",
  ```

  ## 部署

    * [ ] TODO