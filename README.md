# Danesfield

A [Girder-4](https://github.com/girder/cookiecutter-girder-4)-based web application built on [ResonantGeoData](https://github.com/ResonantGeoData/ResonantGeoData) for running and interacting with Kitware's [Danesfield](https://github.com/Kitware/Danesfield) system.

Danesfield addresses the algorithmic challenges of the IARPA CORE3D program by reconstructing semantically meaningful 3D models of buildings and other man-made structures from satellite imagery. For more information on Danesfield itself, see the [Danesfield README](https://github.com/Kitware/Danesfield/blob/master/README.rst).

## Running the application
See [DEVELOPMENT.md](https://github.com/girder/Danesfield/blob/main/DEVELOPMENT.md) for instructions to run the web app locally.

## Components of the web application
The web application is divided into a Django-based backend and a Vue.js-based frontend.

- The backend is built on top of Kitware's [ResonantGeoData](https://github.com/ResonantGeoData/ResonantGeoData) and [RD-OASIS](https://github.com/ResonantGeoData/RD-OASIS) frameworks, in addition to [Django](https://www.djangoproject.com/) and [Django REST framework](https://www.django-rest-framework.org/).
- The frontend web interface is built using [Vue.js](https://vuejs.org/) and [Vuetify](https://vuetifyjs.com/en/), as well as [CesiumJS](https://cesium.com/platform/cesiumjs/) for visualization of the Danesfield 3D tiles output.
