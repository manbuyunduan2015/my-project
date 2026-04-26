import request from './request';

export function getRelationsApi(params) {
  return request.get('/api/relations', { params });
}

export function createRelationApi(data) {
  return request.post('/api/relations', data);
}

export function updateRelationApi(id, data) {
  return request.put(`/api/relations/${id}`, data);
}

export function deleteRelationApi(id) {
  return request.delete(`/api/relations/${id}`);
}

export function getVehicleBomApi(vehicleId) {
  return request.get(`/api/vehicles/${vehicleId}/parts`);
}

export function getPartVehiclesApi(partId) {
  return request.get(`/api/parts/${partId}/vehicles`);
}
