export type RGDResult = {
  spatial_id: number;
  acquisition_date: string | null;
  footprint: {
    type: string;
    coordinates: Array<Array<number>>;
  };
  instrumentation: string | null;
  outline: {
    type: string;
    coordinates: Array<Array<number>>;
  };
  subentry_type: string;
  subentry_name: string;
  show_footprint: boolean;
  show_overlay: boolean;
}

export type ImageryResult = {
  spatial_id: number;
  outline: string;
  subentry_name: string;
  subentry_type: string;
  parent_raster: {
    id: number;
    image_set: number;
    ancillary_files: number[];
    created: string;
    modified: string;
    failure_reason: string;
    status: string;
    name: string;
    description: string;
  };
  acquisition_date: string;
  instrumentation: string;
  created: string;
  modified: string;
  crs: string;
  origin: number[];
  extent: number[];
  resolution: number[];
  transform: number[];
  cloud_cover: number;
}

export type TileParamsType = {
  index?: number;
  image: {
  id: number;
  name?: string;
  };
  opacity?: number;
}
