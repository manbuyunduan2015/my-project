import request from './request';

export function getRolesApi() {
  return request.get('/api/roles');
}
