

Install Rover
```bash
curl -sSL https://rover.apollo.dev/nix/latest | sh
```

Run
```bash
rover supergraph compose --config ./config/supergraph-config.yaml > ./config/supergraph.graphql
```

```
curl --request POST \
  --header 'content-type: application/json' \
  --url 'http://prime.local:4000/' \
  --data '{"query":"query { __typename }"}'

```


