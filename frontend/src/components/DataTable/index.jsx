import React from 'react';
import { Table, Pagination } from 'antd';

const DataTable = ({
  columns,
  dataSource,
  loading = false,
  rowKey = 'id',
  pagination = true,
  total = 0,
  current = 1,
  pageSize = 10,
  onChange,
  ...rest
}) => (
  <Table
    columns={columns}
    dataSource={dataSource}
    loading={loading}
    rowKey={rowKey}
    pagination={false}
    {...rest}
  />
);

export default DataTable;
