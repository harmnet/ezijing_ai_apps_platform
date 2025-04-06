<template>
  <div class="digital-human-container">
    <el-card class="filter-container">
      <div class="filter-header">
        <h2>数字人资源库</h2>
        <div class="filter-actions">
          <el-select v-model="filters.type" placeholder="选择类型" clearable @change="fetchData">
            <el-option v-for="type in typeOptions" :key="type.value" :label="type.label" :value="type.value" />
          </el-select>
          <el-select v-model="filters.status" placeholder="选择状态" clearable @change="fetchData">
            <el-option v-for="status in statusOptions" :key="status.value" :label="status.label" :value="status.value" />
          </el-select>
          <el-button type="primary" @click="goToPPTVideo">
            <el-icon><VideoCameraFilled /></el-icon> 生成PPT讲解视频
          </el-button>
        </div>
      </div>
    </el-card>

    <div v-loading="loading" class="digital-human-content">
      <el-empty v-if="aibeings.length === 0 && !loading" description="暂无数字人数据" />
      
      <div v-else class="digital-human-grid">
        <el-card v-for="item in aibeings" :key="item.id" class="digital-human-card" :class="{ 'inactive': item.status === 'inactive' }">
          <div class="card-header">
            <div class="avatar-container">
              <el-avatar :size="64" :src="item.avatar" :alt="item.name">
                <el-icon><User /></el-icon>
              </el-avatar>
              <el-tag v-if="item.status === 'active'" type="success" size="small" effect="light">启用中</el-tag>
              <el-tag v-else type="info" size="small" effect="light">已停用</el-tag>
            </div>
            <div class="header-info">
              <h3>{{ item.name }}</h3>
              <el-tag size="small" :type="getTypeTagType(item.type)">{{ getTypeName(item.type) }}</el-tag>
            </div>
          </div>
          <div class="card-content">
            <p class="description">{{ item.description }}</p>
          </div>
          <div class="card-footer">
            <el-button type="primary" size="small" :disabled="item.status === 'inactive'" @click="handleSelect(item)">
              选择使用
            </el-button>
            <el-button size="small" @click="showDetails(item)">查看详情</el-button>
          </div>
        </el-card>
      </div>

      <div class="pagination-container">
        <el-pagination
          v-if="total > 0"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 数字人详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="数字人详情"
      width="50%"
      :destroy-on-close="true"
    >
      <div v-if="selectedAIBeing" class="dialog-content">
        <div class="dialog-header">
          <el-avatar :size="80" :src="selectedAIBeing.avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <div class="dialog-title">
            <h2>{{ selectedAIBeing.name }}</h2>
            <div class="dialog-tags">
              <el-tag :type="getTypeTagType(selectedAIBeing.type)" effect="light">{{ getTypeName(selectedAIBeing.type) }}</el-tag>
              <el-tag v-if="selectedAIBeing.status === 'active'" type="success" effect="light">启用中</el-tag>
              <el-tag v-else type="info" effect="light">已停用</el-tag>
            </div>
          </div>
        </div>

        <el-divider />

        <div class="dialog-info">
          <h3>基本信息</h3>
          <p><strong>描述：</strong>{{ selectedAIBeing.description }}</p>
          <p><strong>创建时间：</strong>{{ formatDate(selectedAIBeing.created_at) }}</p>
          <p><strong>更新时间：</strong>{{ formatDate(selectedAIBeing.updated_at) }}</p>
        </div>

        <div v-if="selectedAIBeing.config" class="dialog-config">
          <h3>配置信息</h3>
          <el-descriptions :column="1" border>
            <el-descriptions-item v-for="(value, key) in selectedAIBeing.config" :key="key" :label="key">
              {{ value }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button v-if="selectedAIBeing && selectedAIBeing.status === 'active'" type="primary" @click="handleSelect(selectedAIBeing)">选择使用</el-button>
          <el-button v-if="selectedAIBeing && selectedAIBeing.status === 'active'" type="success" @click="goToPPTVideoWithHuman(selectedAIBeing)">
            <el-icon><VideoCameraFilled /></el-icon> 生成PPT讲解视频
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { User, VideoCameraFilled } from '@element-plus/icons-vue';
import { aiBeingApi } from '@/utils/request';
import { useRouter } from 'vue-router';

export default {
  name: 'DigitalHumanList',
  components: {
    User,
    VideoCameraFilled
  },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const aibeings = ref([]);
    const currentPage = ref(1);
    const pageSize = ref(8);
    const total = ref(0);
    const dialogVisible = ref(false);
    const selectedAIBeing = ref(null);

    const filters = reactive({
      type: '',
      status: ''
    });

    const typeOptions = [
      { value: 'chat', label: '智能对话' },
      { value: 'video', label: '视频生成' },
      { value: 'image', label: '图像生成' }
    ];

    const statusOptions = [
      { value: 'active', label: '启用中' },
      { value: 'inactive', label: '已停用' }
    ];

    const getTypeTagType = (type) => {
      const typeMap = {
        'chat': 'primary',
        'video': 'success',
        'image': 'warning'
      };
      return typeMap[type] || 'info';
    };

    const getTypeName = (type) => {
      const typeMap = {
        'chat': '智能对话',
        'video': '视频生成',
        'image': '图像生成'
      };
      return typeMap[type] || type;
    };

    const formatDate = (dateString) => {
      if (!dateString) return '暂无数据';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const fetchData = async () => {
      loading.value = true;
      
      try {
        // 构建查询参数
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };

        if (filters.type) {
          params.type = filters.type;
        }
        
        if (filters.status) {
          params.status = filters.status;
        }

        const response = await aiBeingApi.getAIBeings(params);
        
        aibeings.value = response.data.items;
        total.value = response.data.total_count;
      } catch (error) {
        console.error('获取数字人列表时出错:', error);
        ElMessage.error('获取数字人列表失败，请稍后重试');
      } finally {
        loading.value = false;
      }
    };

    const handlePageChange = (page) => {
      currentPage.value = page;
      fetchData();
    };

    const showDetails = (item) => {
      selectedAIBeing.value = item;
      dialogVisible.value = true;
    };

    const handleSelect = (item) => {
      if (item.status === 'inactive') {
        ElMessage.warning('该数字人当前处于停用状态，无法选择');
        return;
      }
      
      // 这里可以处理选择数字人的逻辑，例如发出事件或者进行路由跳转
      ElMessage.success(`已选择数字人: ${item.name}`);
      
      // 示例：发出选择事件
      // emit('select', item);
      
      // 示例：路由跳转到使用页面
      // router.push({ name: 'digitalHumanUse', params: { id: item.id } });
    };

    const goToPPTVideo = () => {
      router.push({ name: 'DigitalHumanPPTVideo' });
    };

    // 在数字人详情中添加跳转到PPT讲解视频的函数
    const goToPPTVideoWithHuman = (aiBeing) => {
      router.push({
        name: 'DigitalHumanPPTVideo',
        query: {
          humanId: aiBeing.id,
          humanName: aiBeing.name,
          virtualHumanId: aiBeing.virtualHumanId || aiBeing.id
        }
      });
    };

    onMounted(() => {
      fetchData();
    });

    return {
      loading,
      aibeings,
      currentPage,
      pageSize,
      total,
      filters,
      typeOptions,
      statusOptions,
      dialogVisible,
      selectedAIBeing,
      getTypeTagType,
      getTypeName,
      formatDate,
      fetchData,
      handlePageChange,
      showDetails,
      handleSelect,
      goToPPTVideo,
      goToPPTVideoWithHuman
    };
  }
};
</script>

<style scoped>
.digital-human-container {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.filter-header h2 {
  margin: 0;
  color: #303133;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.digital-human-content {
  min-height: 500px;
}

.digital-human-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.digital-human-card {
  transition: all 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.digital-human-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.digital-human-card.inactive {
  opacity: 0.7;
}

.card-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.avatar-container {
  position: relative;
  margin-right: 15px;
}

.avatar-container .el-tag {
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
}

.header-info {
  flex: 1;
}

.header-info h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
}

.card-content {
  flex: 1;
  margin-bottom: 15px;
}

.description {
  margin: 0;
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.dialog-content {
  padding: 0 20px;
}

.dialog-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.dialog-title {
  margin-left: 20px;
}

.dialog-title h2 {
  margin: 0 0 10px 0;
}

.dialog-tags {
  display: flex;
  gap: 8px;
}

.dialog-info, .dialog-config {
  margin-bottom: 20px;
}

.dialog-info h3, .dialog-config h3 {
  margin-top: 0;
  color: #303133;
}
</style> 