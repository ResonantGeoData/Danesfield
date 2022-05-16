// eslint-disable-next-line import/no-unresolved
import type { GeoJSON } from 'geojson';

export interface Paginated<T> {
  count: number;
  next: string;
  previous: string;
  results: T[];
}

export interface Model {
  id: number;
  created: string;
  modified: string;
}

export interface DockerImage extends Model {
  name: string;
  image_id: string | null;
  image_file: number | null;
}

export interface Dataset extends Model {
  name: string;
  files: number[];
  size: number;
}

export interface Algorithm extends Model {
  name: string;
  environment: {[key: string]: string};
  command: string;
  entrypoint: string | null;
  gpu: boolean;
  docker_image: number;
  input_dataset: number[];
}

export type TaskStatus = 'created' | 'queued' | 'running' | 'failed' | 'success';
export interface Task extends Model {
  status: TaskStatus;
  algorithm: number;
}

export interface ChecksumFile extends Model {
  name: string;
  description: string | null;
  status: TaskStatus | 'skipped';
  file: string;
  url: string;
  download_url: string;
  type: 1 | 2;
  failure_reason: string | null;
  checksum: string;
  validate_checksum: boolean;
  last_validation: boolean;
  collection: number | null;
  created_by: number | null;
}

export interface SpatialEntry extends Model {
  spatial_id: number;
  acquisition_date?: string;
  outline: GeoJSON;
  footprint?: GeoJSON;
  instrumentation?: string;
  subentry_name: string;
  subentry_type: string;

}

export interface Raster extends Model {
  name: string;
  description?: string;
  extra_fields?: object;
  raster_meta_id: number;
  status: string;
}

export interface RasterMeta extends SpatialEntry {
  cloud_cover?: number;
  crs: string;
  origin: number[];
  extent: number[];
  resolution: number[];
  transform: number[];
  parent_raster: Raster;
  subentry_type: 'RasterMeta';
}

export interface Tiles3D extends Model {
  name: string;
  description?: string;
  json_file: ChecksumFile;
  status: string;
}

export interface Tiles3DMeta extends SpatialEntry {
  source: Tiles3D;
  subentry_type: 'Tiles3DMeta';
}
