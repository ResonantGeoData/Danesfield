# Danesfield
The Danesfield web client.

## Develop

### Build and Run (Docker)

From the root of the repository, run

```bash
docker compose up
```

The web app will be served at `http://localhost:8080/`.
This is the recommended way to run the application locally,
since it also spins up the backend Django server for you.

### Build and Run (Natively)

Ensure you have Node.js and the Yarn package manager installed.
Then run the following commands from the root of the repo

```bash
cd client/
yarn install
yarn run serve
```

The web app will be served at `http://localhost:8080/`.

This app requires a server component to be useful, which you can run locally; see the [instructions](https://github.com/girder/Danesfield#danesfield) for doing so.
Alternatively, simply run them both in Docker as described above.

### Test

In order to fix the code formatting and check for some common errors, run:

```bash
yarn run lint
```

### Environment Variables

- VUE_APP_CESIUM_ION_API_KEY
  - A Cesium Ion API key. This is needed for terrain to render in Cesium.JS. If not provided, no terrain will be rendered (i.e. the surface will be flat).
