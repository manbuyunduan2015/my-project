import React, { useEffect, useState } from 'react';
import { Card, Table, Button, Input, Modal, Form, Popconfirm, message, Space, Select } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import {
  getVehiclesApi, createVehicleApi, updateVehicleApi, deleteVehicleApi,
} from '../../api/vehicle';
import { ROLE_ADMIN } from '../../utils/constants';

const VehicleManage = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form] = Form.useForm();
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.roles?.includes(ROLE_ADMIN);

  const fetchData = async (searchParams = {}) => {
    setLoading(true);
    try {
      const params = { page, page_size: pageSize, ...searchParams };
      const res = await getVehiclesApi(params);
      setData(res.data?.items || []);
      setTotal(res.data?.total || 0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [page, pageSize]);

  const handleSearch = (values) => { setPage(1); fetchData({ ...values, page: 1, page_size: pageSize }); };
  const handleReset = () => fetchData();

  const handleOpenModal = (record) => {
    setEditId(record?.id || null);
    if (record) {
      form.setFieldsValue(record);
    } else {
      form.resetFields();
    }
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    const values = await form.validateFields();
    try {
      if (editId) {
        await updateVehicleApi(editId, values);
        message.success('更新成功');
      } else {
        await createVehicleApi(values);
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
      await deleteVehicleApi(id);
      message.success('删除成功');
      fetchData();
    } catch (err) {
      message.error(err.message || '删除失败');
    }
  };

  const columns = [
    { title: '整车编号', dataIndex: 'vehicle_code' },
    { title: '整车名称', dataIndex: 'vehicle_name' },
    { title: '型号', dataIndex: 'vehicle_model' },
    { title: '品牌', dataIndex: 'brand' },
    { title: '年款', dataIndex: 'year_model' },
    { title: '发动机型号', dataIndex: 'engine_model' },
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
      <Card title="整车管理" extra={isAdmin && <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal(null)}>新增整车</Button>}>
        <Form layout="inline" onFinish={handleSearch} style={{ marginBottom: 16 }}>
          <Form.Item name="vehicle_code" label="整车编号"><Input placeholder="请输入编号" /></Form.Item>
          <Form.Item name="vehicle_name" label="整车名称"><Input placeholder="请输入名称" /></Form.Item>
          <Form.Item name="brand" label="品牌">
            <Select allowClear placeholder="请选择品牌" style={{ width: 150 }}>
              <Select.Option value="比亚迪">比亚迪</Select.Option>
              <Select.Option value="特斯拉">Tesla</Select.Option>
              <Select.Option value="宝马">宝马</Select.Option>
              <Select.Option value="奥迪">奥迪</Select.Option>
              <Select.Option value="奔驰">奔驰</Select.Option>
              <Select.Option value="丰田">丰田</Select.Option>
              <Select.Option value="本田">本田</Select.Option>
              <Select.Option value="大众">大众</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Space><Button type="primary" htmlType="submit">查询</Button><Button onClick={handleReset}>重置</Button></Space>
          </Form.Item>
        </Form>
        <Table
          columns={columns} dataSource={data} loading={loading} rowKey="id"
          pagination={{ current: page, pageSize, total, onChange: (p, ps) => { setPage(p); setPageSize(ps); } }}
        />
      </Card>
      <Modal title={editId ? '编辑整车' : '新增整车'} open={modalOpen} onOk={handleSubmit} onCancel={() => setModalOpen(false)} width={600}>
        <Form form={form} layout="vertical">
          <Form.Item name="vehicle_code" label="整车编号" rules={[{ required: true }]}><Input disabled={!!editId} /></Form.Item>
          <Form.Item name="vehicle_name" label="整车名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="vehicle_model" label="型号"><Input /></Form.Item>
          <Form.Item name="brand" label="品牌">
            <Select allowClear placeholder="请选择品牌">
              <Select.Option value="比亚迪">比亚迪</Select.Option>
              <Select.Option value="特斯拉">Tesla</Select.Option>
              <Select.Option value="宝马">宝马</Select.Option>
              <Select.Option value="奥迪">奥迪</Select.Option>
              <Select.Option value="奔驰">奔驰</Select.Option>
              <Select.Option value="丰田">丰田</Select.Option>
              <Select.Option value="本田">本田</Select.Option>
              <Select.Option value="大众">大众</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="year_model" label="年款"><Input /></Form.Item>
          <Form.Item name="engine_model" label="发动机型号"><Input /></Form.Item>
          <Form.Item name="description" label="描述"><Input.TextArea rows={3} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default VehicleManage;
