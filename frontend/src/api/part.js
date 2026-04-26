import request from './request';

export function getPartsApi(params) {
  return request.get('/api/parts', { params });
}

export function createPartApi(data) {
  return request.post('/api/parts', data);
}

export function updatePartApi(id, data) {
  return request.put(`/api/parts/${id}`, data);
}

export function deletePartApi(id) {
  return request.delete(`/api/parts/${id}`);
}

export function getPartDetailApi(id) {
  return request.get(`/api/parts/${id}`);
}
