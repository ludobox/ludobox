## Architecture

### Concepts

We want to keep playing even in the most extreme conditions, so Ludobox is made to support offline, P2P, unstable networks running on low-end hardware.

#### Minimum Viable Architecture

We design for a *“Minimum Viable Architecture”*, that is :
- hardware requirements should be minimal
- static files are prefered
- index and pages can be rebuilt manually
- ideally, it should run properly on a TP-Link for less than 10euros

#### Small and cute

We want our app to stay *small and cute*, that is :
- well-written, in a way that is pleasant to read
- as small as possible, so we can now all its parts and move fast
- fun to use and fun to develop, using technologies and frameworks that we like


### Folders

The app is separated in several main components :

| folder | content | tech |
|---|---|---|
| **/server** | a JSON api | Python/Flask |
| **/frontend** |  single-page application   | React, ES6 |
| **/data** | the games themselves | JSON description and static files |
| **/model** | the schema describing the contents | JSON Schema v4 |
| **/bin** | a bunch of scripts | Bash, node |
| **/docs** | the current doc | MkDocs, Markdown |

All communications between client and server are made using a [REST API](/api)
