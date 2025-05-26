import React, { useEffect, useState } from "react";
import axios from "axios";

interface UsageLog {
  id: number;
  user_id: number;
  resource_type: string;
  resource_id: number;
  action: string;
  quantity_used?: number;
  duration_minutes?: number;
  purpose?: string;
  notes?: string;
  issues_reported?: string;
  project_name?: string;
  timestamp: string;
  auto_recorded?: boolean;
}

const API_BASE = "http://127.0.0.1:8000/api/logs/";

const App: React.FC = () => {
  const [logs, setLogs] = useState<UsageLog[]>([]);
  const [form, setForm] = useState({
    resource_type: "equipment",
    resource_id: "",
    action: "start_use",
    quantity_used: "",
    duration_minutes: "",
    purpose: "",
    notes: "",
    issues_reported: "",
    project_name: "",
    auto_recorded: false,
  });

  // TODO: 替换为实际token
  const token = localStorage.getItem("access_token") || "";

  // 获取日志列表
  useEffect(() => {
    axios
      .get(API_BASE, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setLogs(res.data))
      .catch(() => {});
  }, []);

  // 提交日志
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    axios
      .post(
        API_BASE,
        {
          ...form,
          resource_id: Number(form.resource_id),
          quantity_used: form.quantity_used ? Number(form.quantity_used) : undefined,
          duration_minutes: form.duration_minutes ? Number(form.duration_minutes) : undefined,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((res) => setLogs([res.data, ...logs]))
      .catch(() => {});
  };

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 24, background: "#fff", borderRadius: 12 }}>
      <h2>📝 使用日志管理</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 32 }}>
        <div>
          <label>资源类型：</label>
          <select value={form.resource_type} onChange={e => setForm(f => ({ ...f, resource_type: e.target.value }))}>
            <option value="equipment">设备</option>
            <option value="material">材料</option>
          </select>
        </div>
        <div>
          <label>资源ID：</label>
          <input value={form.resource_id} onChange={e => setForm(f => ({ ...f, resource_id: e.target.value }))} required />
        </div>
        <div>
          <label>操作类型：</label>
          <select value={form.action} onChange={e => setForm(f => ({ ...f, action: e.target.value }))}>
            <option value="start_use">开始使用</option>
            <option value="end_use">结束使用</option>
            <option value="consume">消耗</option>
            <option value="maintenance">维护</option>
          </select>
        </div>
        <div>
          <label>数量：</label>
          <input type="number" value={form.quantity_used} onChange={e => setForm(f => ({ ...f, quantity_used: e.target.value }))} />
        </div>
        <div>
          <label>使用时长(分钟)：</label>
          <input type="number" value={form.duration_minutes} onChange={e => setForm(f => ({ ...f, duration_minutes: e.target.value }))} />
        </div>
        <div>
          <label>目的：</label>
          <input value={form.purpose} onChange={e => setForm(f => ({ ...f, purpose: e.target.value }))} />
        </div>
        <div>
          <label>备注：</label>
          <input value={form.notes} onChange={e => setForm(f => ({ ...f, notes: e.target.value }))} />
        </div>
        <div>
          <label>问题反馈：</label>
          <input value={form.issues_reported} onChange={e => setForm(f => ({ ...f, issues_reported: e.target.value }))} />
        </div>
        <div>
          <label>项目名称：</label>
          <input value={form.project_name} onChange={e => setForm(f => ({ ...f, project_name: e.target.value }))} />
        </div>
        <div>
          <label>
            <input type="checkbox" checked={form.auto_recorded} onChange={e => setForm(f => ({ ...f, auto_recorded: e.target.checked }))} />
            自动记录
          </label>
        </div>
        <button type="submit">添加日志</button>
      </form>
      <h3>日志列表</h3>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户ID</th>
            <th>资源类型</th>
            <th>资源ID</th>
            <th>操作</th>
            <th>数量</th>
            <th>时长</th>
            <th>目的</th>
            <th>备注</th>
            <th>项目</th>
            <th>时间</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.user_id}</td>
              <td>{log.resource_type}</td>
              <td>{log.resource_id}</td>
              <td>{log.action}</td>
              <td>{log.quantity_used ?? ""}</td>
              <td>{log.duration_minutes ?? ""}</td>
              <td>{log.purpose ?? ""}</td>
              <td>{log.notes ?? ""}</td>
              <td>{log.project_name ?? ""}</td>
              <td>{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
