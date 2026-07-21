export type ApplyClickDetails = {
  apply_url: string;
  job_id: string;
  title: string;
  location: string;
  region: string;
  slice_path?: string;
};

export type ApplyClickParameters = {
  job_id: string;
  job_title: string;
  job_location: string;
  job_region: string;
  slice_path: string;
  page_path: string;
  link_url: string;
};

export function buildApplyClickParameters(
  {
    apply_url,
    job_id,
    title,
    location,
    region,
    slice_path,
  }: ApplyClickDetails,
  pagePath: string
): ApplyClickParameters {
  return {
    job_id,
    job_title: title,
    job_location: location,
    job_region: region,
    slice_path: slice_path || pagePath,
    page_path: pagePath,
    link_url: apply_url,
  };
}
