| 网站认证方式          | 对应方案                 |
| --------------- | -------------------- |
| HTTP Basic Auth | `BasicAuthProvider`  |
| API Key         | `ApiKeyAuthProvider` |
| Bearer Token    | `BearerAuthProvider` |
| OAuth2          | `OAuth2AuthProvider` |
| 登录页面 + Cookie   | Login/Session        |
| JWT             | `BearerAuthProvider` |
| 无认证             | 不使用 AuthMiddleware   |

HTTP Digest Authentication 和 Basic Authentication 不一样。

Basic：

username + password
        ↓
Base64
        ↓
Authorization

Digest：

server
  ↓
WWW-Authenticate challenge
  ↓
nonce
  ↓
client 根据 username/password/nonce 计算 digest
  ↓
Authorization: Digest ...