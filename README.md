test-client-connector
---

#### Setup

Don't clone this repo just use `docker-compose` with the following yaml snippet:

    version: "2"

    services:
      test-client-connector:
        container_name: test-client-connector
        build: https://github.com/SENERGY-Platform/test-client-connector.git
        image: test-client-connector
        volumes:
          - './test-client-connector/cc-lib:/usr/src/app/cc-lib'
          - './test-client-connector/test.conf:/usr/src/app/test.conf'


Run the following commands to start your test client-connector:

`nano docker-compose.yml` <-- add the yaml snippet from above!

`mkdir test-client-connector`

`mkdir test-client-connector/cc-lib`
    
`touch test-client-connector/test.conf`
    
`touch test-client-connector/cc-lib/connector.conf`

`docker-compose up -d test-client-connector`
