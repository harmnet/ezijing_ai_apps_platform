<template>
  <div class="text-creation-page app-design-list">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <div class="page-nav">
        <h2>AI应用案例智能设计</h2>
      </div>
      <div class="page-actions">
        <button class="btn btn-primary" @click="createNewCase">
          <i class="el-icon-plus"></i>新建案例
        </button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="section-header">
      <div class="form-row">
        <div class="form-group form-group-wide">
          <input type="text" class="form-control" placeholder="案例名称" v-model="searchForm.name">
        </div>
        <div class="form-group form-group-medium">
          <select class="form-control" v-model="searchForm.industry">
            <option value="">所有行业</option>
            <option value="education">教育</option>
            <option value="healthcare">医疗</option>
            <option value="finance">金融</option>
            <option value="technology">科技</option>
            <option value="manufacturing">制造业</option>
          </select>
        </div>
        <div class="form-group">
          <select class="form-control" v-model="searchForm.case_type">
            <option value="">所有类型</option>
            <option value="experience">场景体验型</option>
            <option value="problem-solving">解决问题型</option>
          </select>
        </div>
        <div class="form-group form-group-wide">
          <input type="text" class="form-control" placeholder="主要标签" v-model="searchForm.tags">
        </div>
      </div>
      <div class="action-buttons">
        <button class="btn btn-primary btn-compact" @click="fetchCases">
          <i class="el-icon-search"></i>查询
        </button>
        <button class="btn btn-secondary btn-compact" @click="resetSearch">
          <i class="el-icon-refresh"></i>重置
        </button>
      </div>
    </div>

    <!-- 表格区域 -->
    <div class="section-content">
      <table class="data-table">
        <thead>
          <tr>
            <th width="60">序号</th>
            <th width="200">案例名称</th>
            <th width="120">所在行业</th>
            <th width="80">学时</th>
            <th width="100">类型</th>
            <th width="180">主要标签</th>
            <th width="160">创建时间</th>
            <th width="160">更新时间</th>
            <th width="100">更新人</th>
            <th width="200">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="10" class="loading-data">加载中...</td>
          </tr>
          <tr v-else-if="tableData.length === 0">
            <td colspan="10" class="empty-data">暂无数据</td>
          </tr>
          <tr v-for="(item, index) in tableData" :key="item.id">
            <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
            <td>{{ item.name }}</td>
            <td>{{ getIndustryName(item.industry) }}</td>
            <td>{{ item.study_hours }}</td>
            <td>{{ getTypeName(item.case_type) }}</td>
            <td>
              <span class="tag" v-for="tag in formatTags(item.tags)" :key="tag">{{ tag }}</span>
            </td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td>{{ formatDate(item.updated_at) }}</td>
            <td>{{ item.updated_by || '-' }}</td>
            <td class="operations">
              <div class="operation-buttons">
                <button class="btn btn-primary btn-compact-sm" @click="editCase(item.id)">
                  <i class="el-icon-edit"></i>编辑
                </button>
                <button class="btn btn-secondary btn-compact-sm" @click="viewCase(item.id)">
                  <i class="el-icon-view"></i>查看
                </button>
                <button class="btn btn-danger btn-compact-sm" @click="deleteCase(item.id)">
                  <i class="el-icon-delete"></i>删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页区域 -->
    <div class="pagination-container">
      <div class="pagination">
        <button class="pagination-button" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
          <i class="el-icon-arrow-left"></i>
        </button>
        <div class="page-info">
          {{ currentPage }}/{{ totalPages }}
        </div>
        <button class="pagination-button" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
          <i class="el-icon-arrow-right"></i>
        </button>
        <div class="page-size-selector">
          <span>每页</span>
          <select v-model="pageSize" @change="handlePageSizeChange">
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
          <span>条</span>
        </div>
      </div>
    </div>

    <!-- 新建案例弹窗 -->
    <div class="modal" v-if="showCreateModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="el-icon-plus"></i>新建AI应用案例</h3>
          <button class="close-btn" @click="cancelCreate">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label class="required">案例名称</label>
              <input type="text" class="form-control" placeholder="请输入案例名称" v-model="caseForm.name">
              <div class="error-message" v-if="formErrors.name">{{ formErrors.name }}</div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="required">类型</label>
              <select class="form-control" v-model="caseForm.case_type">
                <option value="">请选择类型</option>
                <option value="experience">场景体验型</option>
                <option value="problem-solving">解决问题型</option>
              </select>
              <div class="error-message" v-if="formErrors.case_type">{{ formErrors.case_type }}</div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="required">所在行业</label>
              <select class="form-control" v-model="caseForm.industry">
                <option value="">请选择行业</option>
                <option value="education">教育</option>
                <option value="healthcare">医疗</option>
                <option value="finance">金融</option>
                <option value="technology">科技</option>
                <option value="manufacturing">制造业</option>
              </select>
              <div class="error-message" v-if="formErrors.industry">{{ formErrors.industry }}</div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="required">学时</label>
              <input type="number" class="form-control" placeholder="请输入学时" v-model="caseForm.study_hours" min="1">
              <div class="error-message" v-if="formErrors.study_hours">{{ formErrors.study_hours }}</div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="required">主要标签</label>
              <input type="text" class="form-control" placeholder="请输入主要标签，多个标签用逗号分隔" v-model="caseForm.tags">
              <div class="error-message" v-if="formErrors.tags">{{ formErrors.tags }}</div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="required">封面图片</label>
              <div class="cover-upload-container">
                <div class="cover-preview" v-if="coverPreview">
                  <img :src="coverPreview" alt="案例封面预览">
                  <button class="cover-remove-btn" @click="removeCoverImage">
                    <i class="fa fa-trash"></i>
                  </button>
                </div>
                <div class="cover-upload" v-else>
                  <input type="file" id="cover-upload" accept="image/*" @change="handleCoverUpload" class="file-input">
                  <label for="cover-upload" class="cover-upload-button">
                    <i class="fa fa-upload"></i>
                    <span>上传封面图片</span>
                  </label>
                </div>
              </div>
              <div class="upload-tip">建议上传16:9比例的图片，大小不超过2MB</div>
              <div class="error-message" v-if="formErrors.cover_url">{{ formErrors.cover_url }}</div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="btn btn-secondary" @click="cancelCreate">取消</button>
            <button class="btn btn-primary" @click="submitCase" :disabled="uploading">
              {{ uploading ? '上传中...' : '确认创建' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content modal-sm">
        <div class="modal-header">
          <h3><i class="el-icon-warning"></i>删除确认</h3>
          <button class="close-btn" @click="cancelDelete">&times;</button>
        </div>
        <div class="modal-body">
          <p>您确定要删除该案例吗？此操作不可恢复。</p>
          <div class="action-buttons">
            <button class="btn btn-secondary" @click="cancelDelete">取消</button>
            <button class="btn btn-danger" @click="confirmDelete">确认删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'AppDesignList',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      industry: '',
      case_type: '',
      tags: ''
    })

    // 分页相关
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const totalPages = computed(() => Math.ceil(total.value / pageSize.value) || 1)

    // 加载状态
    const loading = ref(false)

    // 表格数据
    const tableData = ref([])

    // 行业映射
    const industryMap = {
      'education': '教育',
      'healthcare': '医疗',
      'finance': '金融',
      'technology': '科技',
      'manufacturing': '制造业'
    }

    // 类型映射
    const typeMap = {
      'experience': '场景体验型',
      'problem-solving': '解决问题型'
    }

    // 获取类型名称
    const getTypeName = (code) => {
      return typeMap[code] || code
    }

    // 获取行业名称
    const getIndustryName = (code) => {
      return industryMap[code] || code
    }

    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      if (isNaN(date.getTime())) return dateStr
      
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }

    // 格式化标签
    const formatTags = (tagsStr) => {
      if (!tagsStr) return []
      return tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag)
    }

    // 获取案例列表
    const fetchCases = async () => {
      loading.value = true
      try {
        // 构建查询参数
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        }
        
        // 添加过滤条件
        if (searchForm.name) params.name = searchForm.name
        if (searchForm.industry) params.industry = searchForm.industry
        if (searchForm.case_type) params.case_type = searchForm.case_type
        if (searchForm.tags) params.tags = searchForm.tags
        
        // 发送API请求
        const response = await axios.get('/api/v1/app-cases', { params })
        
        // 处理响应数据
        if (response.data.status === 'success') {
          tableData.value = response.data.data.items
          total.value = response.data.data.total
        } else {
          console.error('获取案例列表失败:', response.data.message)
        }
      } catch (error) {
        console.error('获取案例列表出错:', error)
      } finally {
        loading.value = false
      }
    }

    // 搜索案例
    const searchCases = () => {
      currentPage.value = 1
      fetchCases()
    }

    // 重置搜索条件
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      currentPage.value = 1
      fetchCases()
    }

    // 切换页码
    const changePage = (page) => {
      currentPage.value = page
      fetchCases()
    }

    // 改变每页显示数量
    const handlePageSizeChange = () => {
      pageSize.value = parseInt(pageSize.value)
      currentPage.value = 1
      fetchCases()
    }

    // 新建案例相关
    const showCreateModal = ref(false)
    const caseForm = reactive({
      name: '',
      case_type: '',
      industry: '',
      study_hours: '',
      tags: '',
      cover_url: '',
      updated_by: '当前用户' // 实际应用中应获取当前登录用户
    })
    const formErrors = reactive({
      name: '',
      case_type: '',
      industry: '',
      study_hours: '',
      tags: '',
      cover_url: ''
    })
    
    // 图片上传相关
    const coverPreview = ref('')
    const uploading = ref(false)
    
    // 处理封面上传
    const handleCoverUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return
      
      // 检查文件类型
      if (!file.type.match('image.*')) {
        alert('请上传图片文件')
        return
      }
      
      // 检查文件大小 (2MB限制)
      if (file.size > 2 * 1024 * 1024) {
        alert('图片大小不能超过2MB')
        return
      }
      
      // 创建本地预览
      const reader = new FileReader()
      reader.onload = (e) => {
        coverPreview.value = e.target.result
      }
      reader.readAsDataURL(file)
      
      // 上传到服务器
      uploading.value = true
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await axios.post('/api/v1/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (response.data && response.data.url) {
          // 设置OSS URL到表单
          caseForm.cover_url = response.data.url
          console.log('图片上传成功：', response.data.url)
        } else {
          alert('图片上传失败，请重试')
          coverPreview.value = ''
        }
      } catch (error) {
        console.error('图片上传错误：', error)
        alert('图片上传出错，请重试')
        coverPreview.value = ''
      } finally {
        uploading.value = false
      }
    }
    
    // 移除封面图片
    const removeCoverImage = () => {
      caseForm.cover_url = ''
      coverPreview.value = ''
    }

    // 表单验证
    const validateForm = () => {
      let isValid = true
      
      // 重置所有错误信息
      Object.keys(formErrors).forEach(key => {
        formErrors[key] = ''
      })
      
      // 验证案例名称
      if (!caseForm.name.trim()) {
        formErrors.name = '请输入案例名称'
        isValid = false
      }
      
      // 验证类型
      if (!caseForm.case_type) {
        formErrors.case_type = '请选择类型'
        isValid = false
      }
      
      // 验证所在行业
      if (!caseForm.industry) {
        formErrors.industry = '请选择行业'
        isValid = false
      }
      
      // 验证学时
      if (!caseForm.study_hours) {
        formErrors.study_hours = '请输入学时'
        isValid = false
      } else if (parseFloat(caseForm.study_hours) < 0.5) {
        formErrors.study_hours = '学时必须不小于0.5'
        isValid = false
      }
      
      // 验证主要标签
      if (!caseForm.tags.trim()) {
        formErrors.tags = '请输入主要标签'
        isValid = false
      }
      
      // 验证封面图片
      if (!caseForm.cover_url) {
        formErrors.cover_url = '请上传封面图片'
        isValid = false
      }
      
      return isValid
    }

    // 创建新案例
    const createNewCase = () => {
      // 重置表单和错误信息
      Object.keys(caseForm).forEach(key => {
        caseForm[key] = ''
      })
      Object.keys(formErrors).forEach(key => {
        formErrors[key] = ''
      })
      caseForm.updated_by = '当前用户' // 设置默认更新人
      coverPreview.value = '' // 重置封面预览
      
      // 显示弹窗
      showCreateModal.value = true
    }
    
    // 取消创建
    const cancelCreate = () => {
      showCreateModal.value = false
    }
    
    // 提交案例
    const submitCase = async () => {
      if (validateForm()) {
        loading.value = true
        try {
          // 发送创建请求
          const response = await axios.post('/api/v1/app-cases', caseForm)
          
          if (response.data.status === 'success') {
            // 关闭弹窗
            showCreateModal.value = false
            // 刷新列表
            fetchCases()
            console.log('案例创建成功:', response.data.data)
          } else {
            console.error('创建案例失败:', response.data.message)
          }
        } catch (error) {
          console.error('创建案例出错:', error)
        } finally {
          loading.value = false
        }
      }
    }

    // 编辑案例
    const editCase = (id) => {
      // 在新窗口中打开编辑页面
      window.open(`/ai-app-design/case-edit/${id}`, '_blank')
    }

    // 查看案例
    const viewCase = (id) => {
      // 在新窗口中打开查看页面
      window.open(`/ai-app-design/case-view/${id}`, '_blank')
    }

    // 删除案例相关
    const showDeleteModal = ref(false)
    const caseIdToDelete = ref(null)

    // 删除案例
    const deleteCase = (id) => {
      caseIdToDelete.value = id
      showDeleteModal.value = true
    }

    // 取消删除
    const cancelDelete = () => {
      showDeleteModal.value = false
      caseIdToDelete.value = null
    }

    // 确认删除
    const confirmDelete = async () => {
      if (!caseIdToDelete.value) return
      
      loading.value = true
      try {
        // 发送删除请求
        const response = await axios.delete(`/api/v1/app-cases/${caseIdToDelete.value}`)
        
        if (response.data.status === 'success') {
          // 关闭弹窗
          showDeleteModal.value = false
          // 刷新列表
          fetchCases()
          console.log('案例删除成功:', caseIdToDelete.value)
        } else {
          console.error('删除案例失败:', response.data.message)
        }
      } catch (error) {
        console.error('删除案例出错:', error)
      } finally {
        loading.value = false
        caseIdToDelete.value = null
      }
    }

    // 组件挂载时获取数据
    onMounted(() => {
      fetchCases()
    })

    return {
      searchForm,
      tableData,
      currentPage,
      pageSize,
      total,
      totalPages,
      loading,
      getIndustryName,
      getTypeName,
      formatDate,
      formatTags,
      fetchCases,
      searchCases,
      resetSearch,
      changePage,
      handlePageSizeChange,
      showCreateModal,
      caseForm,
      formErrors,
      cancelCreate,
      submitCase,
      createNewCase,
      editCase,
      viewCase,
      deleteCase,
      showDeleteModal,
      cancelDelete,
      confirmDelete,
      coverPreview,
      uploading,
      handleCoverUpload,
      removeCoverImage
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/text-creation-common.css';

/* 错误信息样式 */
.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

/* 加载中样式 */
.loading-data {
  text-align: center;
  padding: 20px 0;
  color: #909399;
}

/* 删除确认弹窗样式 */
.modal-sm {
  max-width: 400px;
}

/* 封面上传容器样式 */
.cover-upload-container {
  width: 100%;
  height: 150px;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  margin-bottom: 10px;
}

/* 封面预览样式 */
.cover-preview {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.cover-remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 封面上传样式 */
.cover-upload {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.file-input {
  display: none;
}

.cover-upload-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #606266;
}

.cover-upload-button i {
  font-size: 28px;
  margin-bottom: 8px;
}

/* 上传提示样式 */
.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>