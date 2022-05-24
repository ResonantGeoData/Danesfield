<template>
  <div>
    <v-table v-if="!loading">
      <template #default>
        <thead>
          <tr>
            <th class="text-left">
              File Name
            </th>
            <th class="text-left">
              File Type
            </th>
            <th class="text-left">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="tileset in tiles3d"
            :key="tileset.spatial_id"
          >
            <td>{{ tileset.source.name }}</td>
            <td>3D Tiles</td>
            <td>
              <v-btn
                icon
                @click="setTiles3dVisibility(tileset.spatial_id)"
              >
                <v-icon :color="tiles3dIsVisible(tileset.spatial_id) ? 'success' : ''">
                  mdi-eye
                </v-icon>
              </v-btn>
            </td>
          </tr>
          <tr
            v-for="raster in rasters"
            :key="raster.spatial_id"
          >
            <td>{{ raster.parent_raster.name }}</td>
            <td>Raster</td>
            <td>
              <v-btn
                icon
                @click="setRasterVisibility(raster.spatial_id)"
              >
                <v-icon :color="rasterIsVisible(raster.spatial_id) ? 'success' : ''">
                  mdi-eye
                </v-icon>
              </v-btn>
            </td>
          </tr>
          <tr
            v-for="fmv in Object.values(fmvs)"
            :key="fmv.spatial_id"
          >
            <td
              class="text-truncate"
              style="max-width: 350px;"
            >
              {{ fmv.subentry_name }}
            </td>
            <td>FMV</td>
            <td>
              <v-btn
                icon
                @click="setFMVFootprintVisibility(fmv.spatial_id)"
              >
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                />
                <v-icon
                  v-else
                  :color="fmvFootprintIsVisible(fmv.spatial_id) ? 'success' : ''"
                >
                  mdi-foot-print
                </v-icon>
              </v-btn>
              <v-btn
                icon
                @click="setFMVFlightPathVisibility(fmv.spatial_id)"
              >
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                />
                <v-icon
                  v-else
                  :color="fmvFlightPathIsVisible(fmv.spatial_id) ? 'success' : ''"
                >
                  mdi-airplane
                </v-icon>
              </v-btn>
              <v-btn
                icon
                @click="setVideoSrc(fmv.spatial_id)"
              >
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                />
                <v-icon
                  v-else
                  :color="fmvBeingViewed ? 'success' : ''"
                >
                  mdi-eye
                </v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-table>
    <FMVViewer
      v-if="fmvBeingViewed"
      :fmv-meta="fmvBeingViewed"
    />
  </div>
</template>

<script lang="ts">
import {
  defineComponent, ref, PropType, onMounted,
} from 'vue';
import { axiosInstance } from '@/api';
import { addVisibleOverlay, visibleOverlayIds } from '@/store/cesium/layers';
import { cesiumViewer } from '@/store/cesium';
import * as Cesium from 'cesium';
import { addFootprint, removeFootprint, visibleFootprints } from '@/store/cesium/footprints';
import { FMVMeta, RasterMeta, Tiles3DMeta } from '@/types';
import { renderFlightPath } from '@/utils/cesium';
import FMVViewer from './FMVViewer.vue';

export default defineComponent({
  name: 'FileList',
  components: { FMVViewer },
  props: {
    datasetId: {
      type: String,
      required: true,
    },
    rasterIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
    meshIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
    tiles3dIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
    fmvIds: {
      type: Array as PropType<number[]>,
      required: true,
    },
  },
  setup(props) {
    const rasters = ref<RasterMeta[]>([]);
    const tiles3d = ref<Tiles3DMeta[]>([]);
    const fmvs = ref<Record<number, FMVMeta>>({});

    const fmvBeingViewed = ref<FMVMeta | null>(null);

    const loading = ref(true);

    function rasterIsVisible(rasterId: number) {
      return visibleOverlayIds.value?.includes(rasterId);
    }

    async function setRasterVisibility(rasterId: number) {
      if (rasterIsVisible(rasterId)) {
        visibleOverlayIds.value = visibleOverlayIds.value?.filter((id) => id !== rasterId);
      } else {
        addVisibleOverlay(rasterId);
      }
    }

    function tiles3dIsVisible(tiles3dId: number) {
      const current = tiles3d.value.filter((tile) => tile.spatial_id === tiles3dId)[0];
      const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
      const { scene } = cesiumViewer.value;
      const { primitives } = scene;
      for (let i = 0; i < primitives.length; i += 1) {
        // eslint-disable-next-line no-underscore-dangle
        if (primitives.get(i)._url === tilesetURL) {
          return true;
        }
      }
      return false;
    }

    function setTiles3dVisibility(tiles3dId: number) {
      const current = tiles3d.value.filter((tile) => tile.spatial_id === tiles3dId)[0];
      const tilesetURL = `${axiosInstance.defaults.baseURL}/datasets/${props.datasetId}/file/${current.source.json_file.name}`;
      const { scene } = cesiumViewer.value;
      const { primitives } = scene;

      // Check if this tileset is already displayed. If it is, remove it and return.
      for (let i = 0; i < primitives.length; i += 1) {
        const currentTileset = primitives.get(i);
        // eslint-disable-next-line no-underscore-dangle
        if (currentTileset._url === tilesetURL) {
          cesiumViewer.value.scene.primitives.remove(currentTileset);
          return;
        }
      }

      // Otherwise, display it.
      const tileset = new Cesium.Cesium3DTileset({
        url: tilesetURL,
      });
      cesiumViewer.value.scene.primitives.add(tileset);
      addFootprint(current.spatial_id, current.footprint, 'tiles3d');
    }

    function setVideoSrc(fmvId: number) {
      if (!fmvBeingViewed.value) {
        fmvBeingViewed.value = fmvs.value[fmvId];
      } else {
        fmvBeingViewed.value = null;
      }
    }

    function fmvFootprintIsVisible(fmvId: number) {
      return Object.keys(visibleFootprints.value).includes(`fmv_${fmvId}`);
    }

    async function setFMVFootprintVisibility(fmvId: number) {
      loading.value = true;
      if (fmvFootprintIsVisible(fmvId)) {
        // If the footprint is already visible, make it invisible
        removeFootprint(fmvId, 'fmv');
      } else {
        addFootprint(fmvId, fmvs.value[fmvId].footprint, 'fmv');
      }

      loading.value = false;
    }

    function fmvFlightPathIsVisible(fmvId: number) {
      const { entities } = cesiumViewer.value;
      for (let i = 0; i < entities.values.length; i += 1) {
        if (entities.values[i].id.startsWith(`flight_path_${fmvId}`)) {
          return true;
        }
      }
      return false;
    }

    async function setFMVFlightPathVisibility(fmvId: number) {
      loading.value = true;

      // If the flight path is already visible, make it invisible
      if (fmvFlightPathIsVisible(fmvId)) {
        const { entities } = cesiumViewer.value;
        const entitiesToRemove: string[] = [];
        for (let i = 0; i < entities.values.length; i += 1) {
          // remove all cesium entities associated with this flight path
          if (entities.values[i].id.startsWith(`flight_path_${fmvId}`)) {
            entitiesToRemove.push(entities.values[i].id);
          }
        }
        entitiesToRemove.forEach((id) => entities.removeById(id));
        loading.value = false;
        return;
      }

      // otherwise, proceed with adding the flight path to the cesium map
      const airplaneEntity = renderFlightPath(fmvId, fmvs.value[fmvId].flight_path.coordinates);

      const handler = new Cesium.ScreenSpaceEventHandler(cesiumViewer.value.scene.canvas);
      handler.setInputAction((movement: {position: Cesium.Cartesian2}) => {
        const clickedObject: {
          primitive: Cesium.Primitive;
           id: Cesium.Entity;
          } = cesiumViewer.value.scene.pick(
            movement.position,
          );
        // If anywhere besides the flight path is clicked, disable any camera tracking
        if (cesiumViewer.value.trackedEntity) {
          cesiumViewer.value.trackedEntity = undefined;
        } else if (clickedObject?.id.id?.startsWith(`flight_path_${fmvId}`)) {
          // If the flight path is clicked, make the camera track it
          cesiumViewer.value.trackedEntity = airplaneEntity;
        }
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

      loading.value = false;
    }

    onMounted(async () => {
      await Promise.all(props.rasterIds.map(async (id) => {
        const { data } = await axiosInstance.get(`/rgd_imagery/raster/${id}`);
        rasters.value.push(data);
      }));

      await Promise.all(props.tiles3dIds.map(async (id) => {
        const { data } = await axiosInstance.get(`/rgd_3d/tiles3d/${id}`);
        tiles3d.value.push(data);
      }));

      await Promise.all(props.fmvIds.map(async (id) => {
        const { data } = await axiosInstance.get(`/rgd_fmv/${id}/data`);
        fmvs.value[data.spatial_id] = data;
      }));

      if (tiles3d.value.length > 0) {
        setTiles3dVisibility(tiles3d.value[0].spatial_id);
      } else if (rasters.value.length > 0) {
        setRasterVisibility(rasters.value[0].spatial_id);
      }

      loading.value = false;
    });

    return {
      loading,
      rasters,
      tiles3d,
      fmvs,
      fmvBeingViewed,
      setRasterVisibility,
      setTiles3dVisibility,
      setFMVFootprintVisibility,
      setFMVFlightPathVisibility,
      setVideoSrc,
      fmvFootprintIsVisible,
      fmvFlightPathIsVisible,
      tiles3dIsVisible,
      rasterIsVisible,
    };
  },
});
</script>
