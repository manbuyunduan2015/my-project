import React, { useEffect, useState } from 'react';
import { Card, Table, Button, Select, Modal, Form, Input, InputNumber, Popconfirm, message, Space } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import {
  getRelationsApi, createRelationApi, updateRelationApi, deleteRelationApi, getVehicleBomApi,
} from '../../api/vehiclePart';
import { getVehiclesApi } from '../../api/vehicle';
import { getPartsApi } from '../../api/part';
import { ROLE_ADMIN } from '../../utils/constants';

const RelationManage = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [vehicles, setVehicles] = useState([]);
  const [parts, setParts] = useState([]);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [bomModal, setBomModal] = useState(false);
  const [bomData, setBomData] = useState(null);
  const [form] = Form.useForm();
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.roles?.includes(ROLE_ADMIN);

  const fetchVehicles = async () => {
    const res = await getVehiclesApi({ page: 1, page_size: 1000 });
    setVehicles(res.data?.items || []);
  };

  const fetchParts = async () => {
    const res = await getPartsApi({ page: 1, page_size: 1000 });
    setParts(res.data?.items || []);
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const params = { page, page_size: pageSize };
      if (selectedVehicle) params.vehicle_id = selectedVehicle;
      const res = await getRelationsApi(params);
      setData(res.data?.items || []);
      setTotal(res.data?.total || 0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); fetchVehicles(); fetchParts(); }, [page, pageSize, selectedVehicle]);

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
        await updateRelationApi(editId, values);
        message.success('更新成功');
      } else {
        await createRelationApi(values);
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
      await deleteRelationApi(id);
      message.success('删除成功');
      fetchData();
    } catch (err) {
      message.error(err.message || '删除失败');
    }
  };

  const handleViewBom = async (vehicleId) => {
    const res = await getVehicleBomApi(vehicleId);
    setBomData(res.data);
    setBomModal(true);
  };

  const getVehicleName = (vehicleId) => {
    const v = vehicles.find((item) => item.id === vehicleId);
    return v ? `${v.vehicle_code} - ${v.vehicle_name}` : vehicleId;
  };

  const getPartName = (partId) => {
    const p = parts.find((item) => item.id === partId);
    return p ? `${p.part_code} - ${p.part_name}` : partId;
  };

  const columns = [
    { title: '整车', dataIndex: 'vehicle_id', render: getVehicleName },
    { title: '零件', dataIndex: 'part_id', render: getPartName },
    { title: '数量', dataIndex: 'quantity' },
    { title: '位置', dataIndex: 'position_name' },
    { title: '备注', dataIndex: 'remark' },
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

  const bomColumns = [
    { title: '零件编号', dataIndex: 'part_code' },
    { title: '零件名称', dataIndex: 'part_name' },
    { title: '分类', dataIndex: 'category' },
    { title: '数量', dataIndex: 'quantity' },
    { title: '位置', dataIndex: 'position_name' },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="装配关系管理" extra={isAdmin && <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal(null)}>新增装配关系</Button>}>
        <Space style={{ marginBottom: 16 }}>
          <span>筛选整车：</span>
          <Select
            allowClear
            placeholder="选择整车"
            style={{ width: 200 }}
            value={selectedVehicle}
            onChange={(v) => { setSelectedVehicle(v); setPage(1); }}
            options={vehicles.map((v) => ({ label: `${v.vehicle_code} - ${v.vehicle_name}`, value: v.id }))}
          />
        </Space>
        <Table
          columns={columns} dataSource={data} loading={loading} rowKey="id"
          pagination={{ current: page, pageSize, total, onChange: (p, ps) => { setPage(p); setPageSize(ps); } }}
        />
      </Card>

      <Modal title={editId ? '编辑装配关系' : '新增装配关系'} open={modalOpen} onOk={handleSubmit} onCancel={() => setModalOpen(false)} width={500}>
        <Form form={form} layout="vertical">
          <Form.Item name="vehicle_id" label="整车" rules={[{ required: true }]}>
            <Select disabled={!!editId} options={vehicles.map((v) => ({ label: `${v.vehicle_code} - ${v.vehicle_name}`, value: v.id }))} />
          </Form.Item>
          <Form.Item name="part_id" label="零件" rules={[{ required: true }]}>
            <Select disabled={!!editId} options={parts.map((p) => ({ label: `${p.part_code} - ${p.part_name}`, value: p.id }))} />
          </Form.Item>
          <Form.Item name="quantity" label="数量" rules={[{ required: true }]}><InputNumber min={1} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="position_name" label="位置"><Input /></Form.Item>
          <Form.Item name="remark" label="备注"><Input.TextArea rows={2} /></Form.Item>
        </Form>
      </Modal>

      <Modal title="BOM 清单" open={bomModal} onCancel={() => setBomModal(false)} footer={null} width={700}>
        {bomData && (
          <>
            <p><b>整车：</b>{bomData.vehicle?.vehicle_code} - {bomData.vehicle?.vehicle_name}</p>
            <Table columns={bomColumns} dataSource={bomData.parts} rowKey="relation_id" pagination={false} size="small" />
          </>
        )}
      </Modal>
    </div>
  );
};

export default RelationManage;
