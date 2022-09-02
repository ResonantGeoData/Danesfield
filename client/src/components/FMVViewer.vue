<template>
  <video
    ref="videoElement"
    width="100%"
    height="240"
    autobuffer
    autoplay
    crossorigin="true"
    loop
  >
    <source
      :src="fmvMeta.fmv_file.web_video_file"
      type="video/mp4; codecs=&quot;avc1.42E01E, mp4a.40.2&quot;"
    >
  </video>
</template>

<script setup lang="ts">
import {
  onMounted, onUnmounted, PropType, ref,
} from 'vue';
import * as Cesium from 'cesium';
import { cesiumViewer } from '@/store/cesium';
import { FMVMeta } from '@/types';

const props = defineProps({
  fmvMeta: {
    type: Object as PropType<FMVMeta>,
    required: true,
  },
});

const videoSynchronizer = ref<Cesium.VideoSynchronizer | null>(null);
const prevHierarchy = ref<Cesium.PolygonHierarchy | null>(null);
const polygonEntity = ref<Cesium.Entity | null>(null);
const videoElement = ref<HTMLVideoElement>();

onMounted(() => {
  videoSynchronizer.value = new Cesium.VideoSynchronizer({
    clock: cesiumViewer.value.clock,
    element: videoElement.value,
  });

  polygonEntity.value = new Cesium.Entity({
    polygon: new Cesium.PolygonGraphics({
      hierarchy: new Cesium.CallbackProperty(() => {
        if (!videoElement.value) {
          return null;
        }
        const frameRate = props.fmvMeta.fmv_file.frame_rate;
        const frameNumbers = props.fmvMeta.frame_numbers;
        const groundFrames = props.fmvMeta.ground_frames;

        const frame = Math.round(videoElement.value.currentTime * frameRate);
        const index = frameNumbers.indexOf(frame);
        if (index > -1) {
          const coords = groundFrames.coordinates[index][0];

          const newHierarchy = new Cesium.PolygonHierarchy([
            Cesium.Cartesian3.fromDegrees(coords[0][0], coords[0][1]),
            Cesium.Cartesian3.fromDegrees(coords[1][0], coords[1][1]),
            Cesium.Cartesian3.fromDegrees(coords[2][0], coords[2][1]),
            Cesium.Cartesian3.fromDegrees(coords[3][0], coords[3][1]),
          ]);

          prevHierarchy.value = newHierarchy;

          return newHierarchy;
        }
        // If the no positional data exists for the current video frame,
        // use the previous position. If we don't do this, this function
        // will return `undefined`, which causes Cesium to render nothing
        // for this frame, causing a flickering effect.
        return prevHierarchy.value;
      }, false),
      material: Cesium.Color.RED,
    }),
  });

  cesiumViewer.value.entities.add(polygonEntity.value);
});

onUnmounted(() => {
  // Remove these entities from the Cesium map when the user stops the video -
  if (videoSynchronizer.value && Cesium.defined(videoSynchronizer.value)) {
    videoSynchronizer.value.destroy();
    videoSynchronizer.value = null;
  }
  if (polygonEntity.value && Cesium.defined(polygonEntity.value)) {
    cesiumViewer.value.entities.remove(polygonEntity.value);
  }
});

</script>
