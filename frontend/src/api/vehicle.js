import request from './request';

export function getVehiclesApi(params) {
  return request.get('/api/vehicles', { params });
}

export function createVehicleApi(data) {
  return request.post('/api/vehicles', data);
}

export function updateVehicleApi(id, data) {
  return request.put(`/api/vehicles/${id}`, data);
}

export function deleteVehicleApi(id) {
  return request.delete(`/api/vehicles/${id}`);
}

export function getVehicleDetailApi(id) {
  return request.get(`/api/vehicles/${id}`);
}
