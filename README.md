# alpinelinux-apkbuilds

## Configure repository

```sh
# Add the repository under the `@c032` tag.
echo '@c032 https://pkg.c032.dev/alpinelinux/v3.20/main' >> /etc/apk/repositories

# Trust public key.
curl -sSL --compressed 'https://raw.githubusercontent.com/c032/alpinelinux-apkbuilds/master/.keys/c032.dev-66d24367.rsa.pub' > /etc/apk/keys/c032.dev-66d24367.rsa.pub
```

Update repositories:

```sh
apk update
```
