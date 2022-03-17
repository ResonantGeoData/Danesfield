import Cesium from '@/plugins/cesium';
import ConstantPositionProperty from 'cesium/Source/DataSources/ConstantPositionProperty';
import { Entity, Cartesian3 } from 'cesium'; // GeoJsonDataSource
import { drawnShape } from '@/store/search'; // specifiedShape
import { ref, watch } from '@vue/composition-api';
import { cesiumViewer } from '@/store/cesium';

export const useMap = ref(false);

export const polyPoints: number[][][] = [];

// NOTE: disabled for WATCH demo where region/sites are shown
// let searchSource: GeoJsonDataSource;
// watch(specifiedShape, async () => {
//   cesiumViewer.value.dataSources.remove(searchSource);
//   searchSource = await cesiumViewer.value.dataSources.add(
//     Cesium.GeoJsonDataSource.load(specifiedShape.value, {
//       stroke: Cesium.Color.HOTPINK,
//     }),
//   );
// }, { deep: true });

watch(useMap, () => {
  if (!useMap) { return; }
  {
    cesiumViewer.value.cesiumWidget.screenSpaceEventHandler.removeInputAction(
      Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK,
    );
    const createPoint = (worldPosition: Cartesian3): Entity => {
      const point = cesiumViewer.value.entities.add({
        position: worldPosition,
        point: {
          color: Cesium.Color.GREY,
          pixelSize: 10,
          heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
        },
      });
      return point;
    };
    const drawShape = (positionData: Cartesian3[]): Entity => cesiumViewer.value.entities.add({
      polygon: {
        hierarchy: positionData,
        outline: true,
        outlineColor: Cesium.Color.RED,
        outlineWidth: 3,
        fill: false,
      },
    });

    let activeShapePoints: Cartesian3[] = [];
    let activeShape: Entity | null;
    let floatingPoint: Entity | null;
    const handler = new Cesium.ScreenSpaceEventHandler(cesiumViewer.value.canvas);
    handler.setInputAction((event: { position: Cartesian3 }) => {
      const earthPosition = cesiumViewer.value.camera.pickEllipsoid(event.position);
      if (Cesium.defined(earthPosition)) {
        if (activeShapePoints.length === 0) {
          floatingPoint = createPoint(earthPosition);
          activeShapePoints.push(earthPosition);
          // eslint-disable-next-line max-len
          const dynamicPositions = new Cesium.CallbackProperty((() => new Cesium.PolygonHierarchy(activeShapePoints)), false);
          activeShape = drawShape(dynamicPositions);
        }
        activeShapePoints.push(earthPosition);
        createPoint(earthPosition);
      }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    handler.setInputAction((event: { endPosition: Cartesian3 }) => {
      if (Cesium.defined(floatingPoint)) {
        const newPosition = cesiumViewer.value.camera.pickEllipsoid(event.endPosition);
        if (floatingPoint?.position && Cesium.defined(newPosition)) {
          (floatingPoint.position as ConstantPositionProperty).setValue(newPosition);
          activeShapePoints.pop();
          activeShapePoints.push(newPosition);
        }
      }
    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
    const terminateShape = () => {
      activeShapePoints.pop();
      drawShape(activeShapePoints);
      cesiumViewer.value.entities.remove(floatingPoint);
      cesiumViewer.value.entities.remove(activeShape);
      floatingPoint = null;
      activeShape = null;
      activeShapePoints = [];
      useMap.value = false;
    };
    handler.setInputAction(() => {
      activeShapePoints.forEach((element) => {
        polyPoints.push([
          Cesium.Math.toDegrees(
            (Cesium.Cartographic.fromCartesian(element)
            ).longitude,
          ),
          Cesium.Math.toDegrees(
            (Cesium.Cartographic.fromCartesian(element)
            ).latitude,
          ),
        ]);
      });
      polyPoints.push(polyPoints[0]);
      drawnShape.value.type = 'Polygon';
      // This is super duper important!!!!
      drawnShape.value.coordinates[0] = polyPoints;
      terminateShape();
    }, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);
  }
}, { deep: true });
