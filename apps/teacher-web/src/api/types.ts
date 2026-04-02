/**
 * 通用 API 类型定义
 * 对应后端若依框架的返回结构
 */

// ===== 通用分页参数 =====
export interface PageParams {
  pageNum?: number
  pageSize?: number
}

// ===== 通用分页结果 =====
export interface PageResult<T> {
  total: number
  rows: T[]
  pageNum: number
  pageSize: number
}

// ===== 通用 API 响应 =====
export interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T
}

// ===== 学生信息 =====
export interface StudentInfo {
  id: number
  userName: string
  realName: string
  nickName?: string
  grade?: string
  major?: string
  className?: string
  avatar?: string
}

// ===== 教师信息 =====
export interface TeacherInfo {
  id: number
  userName: string
  realName: string
  nickName?: string
  deptName?: string
  avatar?: string
}
