## set server
```
pip install mitmproxy
```

```
mitmweb --ssl-insecure --mode regular --showhost --set block_global=false --listen-host 0.0.0.0 --listen-port 80
```

## set client environment
NODE_TLS_REJECT_UNAUTHORIZED=0