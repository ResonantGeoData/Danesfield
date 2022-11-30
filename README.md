# Danesfield

A [Girder-4](https://github.com/girder/cookiecutter-girder-4)-based web application built on [ResonantGeoData](https://github.com/ResonantGeoData/ResonantGeoData) for running and interacting with Kitware's [Danesfield](https://github.com/Kitware/Danesfield) system.

Danesfield addresses the algorithmic challenges of the IARPA CORE3D program by reconstructing semantically meaningful 3D models of buildings and other man-made structures from satellite imagery. For more information on Danesfield itself, see the [Danesfield README](https://github.com/Kitware/Danesfield/blob/master/README.rst).

## Running the application
See [DEVELOPMENT.md](https://github.com/girder/Danesfield/blob/main/DEVELOPMENT.md) for instructions to run the web app locally.

## Components of the web application
The web application is divided into a Django-based backend and a Vue.js-based frontend.

- The backend is built on top of Kitware's [ResonantGeoData](https://github.com/ResonantGeoData/ResonantGeoData) and [RD-OASIS](https://github.com/ResonantGeoData/RD-OASIS) frameworks, in addition to [Django](https://www.djangoproject.com/) and [Django REST framework](https://www.django-rest-framework.org/).
- The frontend web interface is built using [Vue.js](https://vuejs.org/) and [Vuetify](https://vuetifyjs.com/en/), as well as [CesiumJS](https://cesium.com/platform/cesiumjs/) for visualization of the Danesfield 3D tiles output.

## Video demo - viewing a dataset
![jacksonville](https://user-images.githubusercontent.com/37340715/204680821-7609f484-b6c5-47b6-89ec-261252a4e5fa.gif)


## Screenshots
![explore](https://user-images.githubusercontent.com/37340715/204678326-b7ca4210-ed69-41cf-a2fa-d564f0a2a545.png)
![3dtiles](https://user-images.githubusercontent.com/37340715/204678340-c422da02-3c16-4b57-b895-ab57e1290bce.png)
![tasks](https://user-images.githubusercontent.com/37340715/204678377-71d18418-9656-4386-933f-d9bcec0964fa.png)
![fmv](https://user-images.githubusercontent.com/37340715/204678386-0dbb4b09-4765-4cc4-842d-e28218355f75.png)
![Self-LE90](https://user-images.githubusercontent.com/37340715/204678548-0b202252-d4d2-4443-b752-2edf62634a8b.png)
