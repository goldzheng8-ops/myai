                 OAuth2 Token Endpoint
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      request_token()          refresh_token()
             │                       │
       initial grant             refresh grant
             │                       │
             └───────────┬───────────┘
                         ▼
                  OAuth2TokenSet

                

然后未来可以实现：

Authorization Code
Client Credentials
Refresh Token
Device Authorization

而不需要修改：

AuthMiddleware
OAuth2CredentialsProvider
OAuth2TokenStore