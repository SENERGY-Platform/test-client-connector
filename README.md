test-client-connector
---

#### Setup

Use `docker-compose` with the following yaml snippet:

    version: "2"

    services:
      test-cc:
        container_name: test-cc
        image: <registry>/test-cc:<environment>
        volumes:
          - './test-cc/cc-lib:/usr/src/app/cc-lib'
          - './test-cc/storage:/usr/src/app/storage'
        restart: unless-stopped


Run the below commands to start your test client-connector:

`docker-compose up -d test-cc`

`docker logs -f test-cc`
