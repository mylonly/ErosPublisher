#Eros Update

## 安装

  前提环境：`Python3.6`,`Pipenv`

  > 关于pipenv，可以参考[使用pipenv管理python虚拟环境](https://vimiix.com/post/2018/03/11/manage-your-virtualenv-with-pipenv/)
  
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

  ## 部署

    * [ ] TODO