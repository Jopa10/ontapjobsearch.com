// Keep free-text analytics bounded and omit obvious contact details.
export function safeSearchText(value: string): string {
  return value.replace(/[^\s@]+@[^\s@]+\.[^\s@]+/g, '[redacted]')
    .replace(/\+?\d[\d\s().-]{7,}\d/g, '[redacted]')
    .replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, 100);
}

export const SEARCH_SOURCE_KEY = 'ontap.search-source.v1';

export function searchResultParameters(query: string, location: string, count: number, recognised: boolean, nearby: boolean) {
  return {
    search_term: safeSearchText(query),
    search_location: safeSearchText(location),
    result_count: count,
    search_outcome: count > 0 ? 'results' : 'no_results',
    location_status: !location ? 'not_provided' : recognised ? 'recognised' : 'unrecognised',
    search_mode: nearby ? 'nearby' : 'keyword',
  };
}
