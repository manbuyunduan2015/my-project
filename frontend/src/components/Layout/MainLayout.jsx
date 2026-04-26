import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Avatar, Dropdown, message } from 'antd';
import {
  DashboardOutlined, CarOutlined, ToolOutlined, LinkOutlined,
  UserOutlined, TeamOutlined, LogoutOutlined,
} from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/slices/authSlice';
import { ROLE_ADMIN } from '../../utils/constants';

const { Sider, Content, Header } = Layout;

const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: '仪表盘' },
  { key: '/vehicles', icon: <CarOutlined />, label: '整车管理' },
  { key: '/parts', icon: <ToolOutlined />, label: '零部件管理' },
  { key: '/vehicle-parts', icon: <LinkOutlined />, label: '装配关系' },
  { key: '/users', icon: <UserOutlined />, label: '用户管理' },
  { key: '/roles', icon: <TeamOutlined />, label: '角色管理' },
];

const MainLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.roles?.includes(ROLE_ADMIN);

  const items = isAdmin ? menuItems : menuItems.filter((item) => !['/users', '/roles'].includes(item.key));

  const handleLogout = () => {
    dispatch(logout());
    message.success('已退出登录');
    navigate('/login');
  };

  const userMenu = {
    items: [{ key: 'logout', icon: <LogoutOutlined />, label: '退出登录', onClick: handleLogout }],
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible>
        <div style={{ height: 32, margin: 16, color: '#fff', textAlign: 'center', fontSize: 14, lineHeight: '32px' }}>
          零部件管理系统
        </div>
        <Menu theme="dark" mode="inline" selectedKeys={[location.pathname]} items={items} onClick={({ key }) => navigate(key)} />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
          <Dropdown menu={userMenu}>
            <span style={{ cursor: 'pointer', color: '#333' }}>
              <Avatar icon={<UserOutlined />} style={{ marginRight: 8 }} />
              {user?.username || '用户'}
            </span>
          </Dropdown>
        </Header>
        <Content style={{ margin: '16px' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
