export interface Attendance {
  id: string
  studentId: string
  studentName: string
  classId: string
  className: string
  date: string
  present: boolean
}

export interface AttendanceRecord {
  studentId: string
  studentName: string
  present: boolean
}
