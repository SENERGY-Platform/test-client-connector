test-client-connector
---

#### Setup

Don't clone this repo just use `docker-compose` with the following yaml snippet:

    version: "2"

    services:
      test-cc:
        container_name: test-cc
        build: https://github.com/SENERGY-Platform/test-client-connector.git
        image: test-cc
        volumes:
          - './test-cc/cc-lib:/usr/src/app/cc-lib'
          - './test-cc/test.conf:/usr/src/app/test.conf'


Run the below commands to start your test client-connector:

`nano docker-compose.yml` <-- add the yaml snippet from above!

`mkdir test-cc`

`mkdir test-cc/cc-lib`
    
`touch test-cc/test.conf`
    
`touch test-cc/cc-lib/connector.conf`

`docker-compose build --no-cache test-cc`

`docker-compose up -d test-cc`

`docker logs -f test-cc`
