import { ref, watch } from '@vue/composition-api';
import Cesium from '@/plugins/cesium';
import { Cartesian3 } from 'cesium';
import { cesiumViewer } from '@/store/cesium';

const pinBuilder = new Cesium.PinBuilder();

export const visiblePins = ref<Record<string, Cartesian3>>({});

export const addPin = async (position: Cartesian3, id: number) => {
  visiblePins.value = { ...visiblePins.value, [id]: position };
};

const pinSources: Record<string, Cartesian3> = {};

watch(visiblePins, (newPins, oldPins) => {
  Object.keys(oldPins).forEach(
    (key) => {
      if (!Object.keys(newPins).includes(key)) {
        // remove footprint
        if (key in pinSources) {
          cesiumViewer.value.dataSources.remove(pinSources[key]);
          delete pinSources[key];
        }
      }
    },
  );
  Object.entries(newPins).forEach(
    async ([key, coordinates]) => {
      if (!Object.keys(oldPins).includes(key)) {
        // add pin
        const source = cesiumViewer.value.entities.add({
          name: key,
          position: coordinates,
          billboard: {
            image: pinBuilder.fromColor(Cesium.Color.ROYALBLUE, 48).toDataURL(),
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          },
        });
        pinSources[key] = source;
      }
    },
  );
});
