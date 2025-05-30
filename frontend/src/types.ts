/**
 * 资源类型枚举
 */
export enum ResourceType {
  EQUIPMENT = "equipment",
  MATERIAL = "material"
}

/**
 * 操作类型枚举
 */
export enum ActionType {
  START_USE = "start_use",
  END_USE = "end_use",
  CONSUME = "consume",
  MAINTENANCE = "maintenance"
}

/**
 * 使用日志接口定义
 */
export interface UsageLog {
  id: number;
  user_id: number;
  resource_type: ResourceType | string;
  resource_id: number;
  action: ActionType | string;
  quantity_used?: number;
  duration_minutes?: number;
  purpose?: string;
  notes?: string;
  issues_reported?: string;
  project_name?: string;
  timestamp: string;
  auto_recorded?: boolean;
}

/**
 * 表单数据接口
 */
export interface LogFormData {
  resource_type: ResourceType;
  resource_id: string;
  action: ActionType;
  quantity_used: string;
  duration_minutes: string;
  purpose: string;
  notes: string;
  issues_reported: string;
  project_name: string;
  auto_recorded: boolean;
}

/**
 * API 响应接口
 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}
