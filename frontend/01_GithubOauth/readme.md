# 登录模块
登录模块使用 [supabase](https://supabase.com)提供的baas服务构建。
## 开通Github Oauth app
### supabase创建项目
1. 前往 https://app.supabase.com 注册账号
2. 点击`New project`创建新项目
![截屏2022-07-30 下午4 29 37](https://user-images.githubusercontent.com/56476336/181898762-606a2df0-c52c-4bfc-9e0c-522168ad3dae.png)
3. 在左侧选择`Settings`，再选择`api`。记录`Project URL`和`anon public key`（后面会用到）。
![181900354-13afa220-08da-4985-afe5-2a760a28a1bd](https://user-images.githubusercontent.com/56476336/181902260-bd16fdad-b4f0-49f6-af9f-bde9294237f5.png)

4. 前往 https://github.com/settings/developers 页面
5. 左侧选择`OAuth App`，点击右上角`New OAuth App`
6. 依次填写应用名称，主页URL，应用描述和callback URL，callbak URL为我们之前记录的`Project URL`后面再加上/auth/v1/callback,大概是这样的格式：
https://[project-ref].supabase.co/auth/v1/callback
![截屏2022-07-30 下午4 26 03](https://user-images.githubusercontent.com/56476336/181897076-8c707a00-dcd4-44b8-b3b3-2fa040df9419.png)
7. 创建`Github Oauth App`后，点击Generate a new client secret，生成一个新的secret，记录这个client secret和Client ID。
    **注意，请不要像下图一样泄露自己的client secret**
![截屏2022-07-30 下午4 50 18](https://user-images.githubusercontent.com/56476336/181903032-8d456d0f-0c45-4d73-b678-1d3a567d7b86.png)
8. 回到supabase的项目页面，点击左侧第三个`authentication`，再点击`settings`，设置Site URL为主页的URL，向下滑动，在`Auth Providers`中找到GitHub，开启`GitHub enabled`，填写`Client ID`和`Client Secret`，点击`save`保存。
![截屏2022-07-30 下午4 46 35](https://user-images.githubusercontent.com/56476336/181902898-c4700892-c0f4-4e49-9d7c-2ddb996c25f9.png)
![截屏2022-07-30 下午4 47 27](https://user-images.githubusercontent.com/56476336/181902910-5655f76f-4fe8-4f4b-9a19-b0284fb12c86.png)
9. 接下来就可以在项目中使用Supabase提供的函数接入Github登录并获取用户信息了。
- 创建一个supbase 客户端
    ```js
    // CLIENT_URL和ANON_PUBLIC_KEY是我们在步骤3中获取到的。
    export const supabase = createClient(CLIENT_URL, ANON_PUBLIC_KEY);
    ```
- 登录
    ```js
    const { user, session, error } = await supabase.auth.signIn({
      provider: 'github',
    })
    // 封装成函数，可以在点击按钮或者其他UI元素时调用
    async function signInWithGithub() {
      const { user, session, error } = await supabase.auth.signIn({
        provider: 'github',
      })
    }
    ```
- 登出
    ```js
    async function signout() {
      const { error } = await supabase.auth.signOut()
    }
    ```
## 获取用户信息
可以通过session()函数获取token和用户信息，token可用于向github发送请求。
```js
const session = supabase.auth.session()

```
session包含如下信息
```json
{
    "provider_token": "...",
    "access_token": "...",
    "expires_in": 3600,
    "expires_at": 1659101941,
    "refresh_token": "0JcxfnY2IsFu_AiV5ClBZg",
    "token_type": "bearer",
    "user": {
        ...
    }
}
```
也可以通过user()函数获取用户信息
```js
const user = supabase.auth.user()
```
获取到的用户信息如下，其中的id是用户的唯一标识。
```json
{
    "id": "a909b2cb-cd98-4e14-8d12-a94de8ade1cc",
    "aud": "authenticated",
    "role": "authenticated",
    "email": "841298391cp@gmail.com",
    "email_confirmed_at": "2022-07-28T16:30:58.444232Z",
    "phone": "",
    "confirmed_at": "2022-07-28T16:30:58.444232Z",
    "last_sign_in_at": "2022-07-29T12:27:39.530272Z",
    "app_metadata": {
        "provider": "github",
        "providers": [
            "github"
        ]
    },
    "user_metadata": {
        "avatar_url": "https://avatars.githubusercontent.com/u/56476336?v=4",
        "email": "841298391cp@gmail.com",
        "email_verified": true,
        "full_name": "vecpeng",
        "iss": "https://api.github.com",
        "name": "vecpeng",
        "preferred_username": "vecpeng",
        "provider_id": "56476336",
        "sub": "56476336",
        "user_name": "vecpeng"
    },
    "identities": [
        {
            "id": "56476336",
            "user_id": "a909b2cb-cd98-4e14-8d12-a94de8ade1cc",
            "identity_data": {
                "avatar_url": "https://avatars.githubusercontent.com/u/56476336?v=4",
                "email": "841298391cp@gmail.com",
                "email_verified": true,
                "full_name": "vecpeng",
                "iss": "https://api.github.com",
                "name": "vecpeng",
                "preferred_username": "vecpeng",
                "provider_id": "56476336",
                "sub": "56476336",
                "user_name": "vecpeng"
            },
            "provider": "github",
            "last_sign_in_at": "2022-07-28T16:30:58.438285Z",
            "created_at": "2022-07-28T16:30:58.438343Z",
            "updated_at": "2022-07-29T12:27:39.526339Z"
        }
    ],
    "created_at": "2022-07-28T16:30:58.431998Z",
    "updated_at": "2022-07-29T12:27:39.532774Z"
}
```
## 监听用户状态
用户登录或者登出时可以使用onAuthStateChange()函数监听
```js
supabase.auth.onAuthStateChange((event, session) => {
  if (event == 'SIGNED_IN') console.log('SIGNED_IN', session)
})
```
## 配合React Hooks使用
在src/hooks目录下，有两个封装的hook，useUser和useSession，用他们可以分别获取最新的用户信息和session。
以useSession为例:
```js
export default function App() {
  const session = useSession();

  return (
    <div className="container" style={{ padding: '50px 0 100px 0' }}>
      {!session ? <Auth /> : <Account key={session.user.id} session={session} />}
    </div>
  )
}
```
更多更详细的信息可以查看[supabase的文档](https://supabase.com/docs)。
