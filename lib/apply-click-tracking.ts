export type ApplyClickDetails = {
  apply_url: string;
  job_id: string;
  title: string;
  employer: string;
  location: string;
  region: string;
  source: string;
  slice_path?: string;
};

export type ApplyClickParameters = {
  job_id: string;
  job_title: string;
  job_employer: string;
  job_location: string;
  job_region: string;
  job_source: string;
  slice_path: string;
  page_path: string;
  link_url: string;
  destination_url: string;
};

export function buildApplyClickParameters(
  {
    apply_url,
    job_id,
    title,
    employer,
    location,
    region,
    source,
    slice_path,
  }: ApplyClickDetails,
  pagePath: string
): ApplyClickParameters {
  return {
    job_id,
    job_title: title,
    job_employer: employer,
    job_location: location,
    job_region: region,
    job_source: source,
    slice_path: slice_path || pagePath,
    page_path: pagePath,
    link_url: apply_url,
    destination_url: apply_url,
  };
}
