# *dailyfresh* 前后端完全分离

## *架构*

- `前端 :`

  - ` vue | react(因为本项目完全分离,适配任意前端框架)` 

- `backend`

  - `基于django-restframework的REST风格API`
  - `django1.11.16(后续将进行升级..)`

- `任务队列(异步处理): celery(django-celery)`

- `缓存:redis(缓存系统待开发)`

- `nginx`

  - `请求转发`

  - `负载均衡配置`

- `Minio`

  - `静态资源存放服务(待做)`

- `mysql`
- `开发环境`
  - `mac and linux`

## *中间件进行登录验证*

- `session验证`
- `白名单验证`
- `csrf 验证`

## *API(通过 Postman调试 )*

```
需要定制返回数据,繁杂业务处理 -> APIVIEW
批量化CRUD  -> LISTAPIVIEW,CREATEAPIVIEW
```

### *用户*

#### *注册*

- `CreateAPIView`
- `celery异步发送邮件`

#### *登录*

- `session`

  - `post`

    ```python
    username:xxx 
    password:xxx
    remember:1 or 0 #是否记住用户名
    ```

- `jwt(待做)`

#### *激活*

- `get`

  ```py
  token：xxx  #激活时产生的token
  ```

  

#### *注销*

- `删除session`
- `删除购物车记录`

#### *用户中心*

##### *信息*

- `ListAPIView`

- `用户收件信息`

##### *订单*

- `查询当前用户所有订单`

##### *地址页面*

- `ListCreateAPIView`
- `此接口接收两种请求`
  - `get用于获得用户的地址表的信息`
  - `post用于提交该用户的地址信息`

##### *添加用户历史记录*

- `redis添加用户历史记录`

- `post`

  ```
  goods_id:
  ```

  

- `key：`

  - `history_6(user_id)：[max=5]`

### *购物车*

#### *添加商品*

- `post`

  ```:
  goods_id:商品id
  count:数量
  ```

#### *更新商品*

- `post`

  ```
  goods_id:商品id
  count:数量
  ```

#### *购物车列表*

#### *删除商品*

- `post`

  ```
  goods_id:商品id
  ```

  

### *商品*

#### *某一类商品列表*

- `get`

  ```
  type_id:类型id
  ```

#### *商品首页*

#### *商品详情*

- `get`

  ```
  goods_id:
  ```

### *订单*

#### *订单首页*

#### *创建订单*

#### *支付*

#### *检测支付状态*



# *待升级功能*

- `开发评论树`
- `jwt认证登录`
- `接口幂等性设计`
- `缓存系统`
- `升级django-2`
- `设置默认地址`
- `订单退款`
- `关于显示购物车数量`
  - `前端ajax请求`

# *BUGFIX*

# 后言

`😉 欢迎issue讨论,同时也邀请使用同种api框架的童鞋一起开发`

