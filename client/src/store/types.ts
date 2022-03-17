import { GeoJSON } from 'geojson';  // eslint-disable-line

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

export type RegionResult = {
  created: string;
  end_date: string;
  footprint: GeoJSON;
  id: number;
  modified: string;
  outline: GeoJSON;
  properties: {
    comments: string[];
    end_date: string;
    mgrs: string;
    model_content: string;
    originator: string;
    region_id: string;
    start_date: string;
    type: string;
    version: string;
  };
  region_id: string;
  start_date: string;
}

export type FocusedDataType = {
  bandsList: Array<Record<string, string>>;
  images: Array<Record<string, string>>;
  title: string;
  spatialId: number;
}

export type RGDResultList = Array<RGDResult>

export interface SearchParameters {
  predicate: string | null;
  acquired: {
    startDate: string | null;
    endDate: string | null;
    startDateModal?: boolean;
    endDateModal?: boolean;
  };
}

export interface Collection {
  id: number | null;
  name: string | null;
}
export interface ResultsFilter {
  distance: {
    min: string | null;
    max: string | null;
  };
  instrumentation: string | null;
  collections: Collection[];
  time: {
    startTime: string | null;
    endTime: string | null;
    startTimeModal?: boolean;
    endTimeModal?: boolean;
  };
}

export interface SitesResult{
  id: number;
  outline: string;
  footprint: string;
  created: string;
  modified: string;
  site_id: string;
  start_date: string;
  end_date: string;
  parent_region: number;
}

export interface SitesFilter {
  regionID: number | null;
  date: string | null;
  originator: string | null;
}

export type TileParamsType = {
  index?: number;
  image: {
  id: number;
  name?: string;
  };
  opacity?: number;
}
