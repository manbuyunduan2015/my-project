import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../components/Layout/MainLayout';
import PrivateRoute from '../components/PrivateRoute';
import LoginPage from '../pages/Login';
import Dashboard from '../pages/Dashboard';
import UserManage from '../pages/UserManage';
import RoleManage from '../pages/RoleManage';
import VehicleManage from '../pages/VehicleManage';
import PartManage from '../pages/PartManage';
import RelationManage from '../pages/RelationManage';

const routes = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: (
      <PrivateRoute>
        <MainLayout />
      </PrivateRoute>
    ),
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'vehicles', element: <VehicleManage /> },
      { path: 'parts', element: <PartManage /> },
      { path: 'vehicle-parts', element: <RelationManage /> },
      { path: 'users', element: <UserManage /> },
      { path: 'roles', element: <RoleManage /> },
    ],
  },
]);

export default routes;
