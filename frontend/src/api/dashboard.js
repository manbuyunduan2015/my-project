import request from './request';

export function getStatistics() {
  return request.get('/api/dashboard/statistics');
}
