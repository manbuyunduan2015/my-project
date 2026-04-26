import React, { useEffect, useState } from 'react';
import { Card, Table, Button, Input, Modal, Form, Select, Tag, Space, Popconfirm, message, Switch } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import SearchForm from '../../components/SearchForm';
import {
  getUsersApi, createUserApi, updateUserApi, deleteUserApi, updateUserStatusApi,
} from '../../api/user';
import { getRolesApi } from '../../api/role';
import { ROLE_ADMIN } from '../../utils/constants';

const UserManage = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [roles, setRoles] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form] = Form.useForm();
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.roles?.includes(ROLE_ADMIN);

  const fetchData = async (searchParams = {}) => {
    setLoading(true);
    try {
      const params = { page, page_size: pageSize, ...searchParams };
      const res = await getUsersApi(params);
      setData(res.data?.items || []);
      setTotal(res.data?.total || 0);
    } finally {
      setLoading(false);
    }
  };

  const fetchRoles = async () => {
    const res = await getRolesApi();
    setRoles(res.data || []);
  };

  useEffect(() => { fetchData(); fetchRoles(); }, [page, pageSize]);

  const handleSearch = (values) => {
    setPage(1);
    fetchData({ ...values, page: 1, page_size: pageSize });
  };

  const handleReset = () => fetchData();

  const handleOpenModal = (record) => {
    setEditId(record?.id || null);
    if (record) {
      form.setFieldsValue({ ...record, role_ids: record.roles?.map((r) => r.id) });
    } else {
      form.resetFields();
      form.setFieldsValue({ status: 1 });
    }
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    const values = await form.validateFields();
    try {
      if (editId) {
        await updateUserApi(editId, values);
        message.success('更新成功');
      } else {
        await createUserApi(values);
        message.success('新增成功');
      }
      setModalOpen(false);
      fetchData();
    } catch (err) {
      message.error(err.message || '操作失败');
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteUserApi(id);
      message.success('删除成功');
      fetchData();
    } catch (err) {
      message.error(err.message || '删除失败');
    }
  };

  const handleStatusChange = async (id, status) => {
    try {
      await updateUserStatusApi(id, status);
      message.success('状态已更新');
      fetchData();
    } catch (err) {
      message.error(err.message || '操作失败');
    }
  };

  const columns = [
    { title: '用户名', dataIndex: 'username' },
    { title: '姓名', dataIndex: 'real_name' },
    { title: '手机号', dataIndex: 'phone' },
    { title: '邮箱', dataIndex: 'email' },
    {
      title: '角色',
      dataIndex: 'roles',
      render: (roles) => (
        <Space>
          {roles?.map((r) => <Tag key={r.id} color={r.role_name === 'admin' ? 'red' : 'blue'}>{r.role_name}</Tag>)}
        </Space>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      render: (status, record) => (
        <Switch checked={status === 1} onChange={(v) => handleStatusChange(record.id, v ? 1 : 0)} />
      ),
    },
    ...(isAdmin ? [{
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => handleOpenModal(record)}>编辑</Button>
          <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      ),
    }] : []),
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="用户管理" extra={isAdmin && <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal(null)}>新增用户</Button>}>
        <SearchForm onSearch={handleSearch} onReset={handleReset}>
          <Form.Item name="username" label="用户名"><Input placeholder="请输入用户名" /></Form.Item>
          <Form.Item name="real_name" label="姓名"><Input placeholder="请输入姓名" /></Form.Item>
        </SearchForm>
        <Table
          columns={columns}
          dataSource={data}
          loading={loading}
          rowKey="id"
          pagination={{ current: page, pageSize, total, onChange: (p, ps) => { setPage(p); setPageSize(ps); } }}
        />
      </Card>
      <Modal title={editId ? '编辑用户' : '新增用户'} open={modalOpen} onOk={handleSubmit} onCancel={() => setModalOpen(false)} width={600}>
        <Form form={form} layout="vertical">
          <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
            <Input disabled={!!editId} />
          </Form.Item>
          <Form.Item name="real_name" label="姓名" rules={[{ required: true }]}><Input /></Form.Item>
          {!editId && <Form.Item name="password" label="密码" rules={[{ required: true }]}><Input.Password /></Form.Item>}
          <Form.Item name="phone" label="手机号"><Input /></Form.Item>
          <Form.Item name="email" label="邮箱"><Input /></Form.Item>
          <Form.Item name="role_ids" label="角色" rules={[{ required: true }]}>
            <Select mode="multiple" options={roles.map((r) => ({ label: r.role_name, value: r.id }))} />
          </Form.Item>
          <Form.Item name="status" label="状态" valuePropName="checked" valueNormalizer={(v) => (v ? 1 : 0)}>
            <Switch checkedChildren="启用" unCheckedChildren="停用" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserManage;
