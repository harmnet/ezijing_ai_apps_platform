<template>
  <div class="content">
    <div class="page-header">
      <div class="page-nav">
        <h2>AI局部重绘</h2>
      </div>
      <div class="page-actions">
        <button class="action-btn" title="创作小贴士" @click="showTips">
          <i class="ri-lightbulb-line"></i>
        </button>
      </div>
    </div>

    <div class="function-container">
      <!-- 左侧表单区域 -->
      <div class="form-container">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-settings-3-line"></i>
            输入参数
          </h3>
        </div>
        
        <div class="form-group">
          <label class="required">上传基础图片</label>
          <div class="upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileChange" 
              accept="image/*" 
              style="display: none"
            >
            <div v-if="!previewImage" class="upload-placeholder">
              <i class="ri-upload-cloud-line"></i>
              <p>点击或拖拽图片到此处上传</p>
              <small>支持jpg、png格式，建议尺寸不小于512x512</small>
            </div>
            <img v-else :src="previewImage" class="preview-image" alt="预览图">
          </div>
        </div>

        <!-- 涂抹工具和画布，图片上传后显示 -->
        <div class="form-group" v-if="previewImage">
          <label>在图片上涂抹指定要修改的区域</label>
          
          <!-- 绘图工具栏 -->
          <div class="drawing-tools">
            <button 
              class="tool-btn" 
              :class="{ active: currentTool === 'brush' }"
              @click="setTool('brush')" 
              title="画笔工具"
            >
              <i class="ri-brush-line"></i>
            </button>
            <button 
              class="tool-btn" 
              :class="{ active: currentTool === 'eraser' }"
              @click="setTool('eraser')" 
              title="橡皮擦"
            >
              <i class="ri-eraser-line"></i>
            </button>
            <button 
              class="tool-btn"
              @click="clearCanvas" 
              title="清除全部"
            >
              <i class="ri-delete-bin-line"></i>
            </button>
            
            <div class="brush-size">
              <label for="brushSize">笔刷大小:</label>
              <input 
                type="range" 
                id="brushSize" 
                v-model="brushSize" 
                min="5" 
                max="50" 
                class="size-slider"
              >
              <span>{{ brushSize }}px</span>
            </div>
          </div>
          
          <!-- 画布容器 -->
          <div class="canvas-container">
            <!-- 底层是原图 -->
            <img 
              :src="previewImage" 
              ref="baseImage" 
              class="base-image" 
              alt="原始图片"
              @load="initCanvas"
            >
            <!-- 上层是涂抹画布 -->
            <canvas 
              ref="maskCanvas" 
              class="mask-canvas"
              @mousedown="startDrawing"
              @mousemove="draw"
              @mouseup="stopDrawing"
              @mouseleave="stopDrawing"
              @touchstart="handleTouchStart"
              @touchmove="handleTouchMove"
              @touchend="stopDrawing"
            ></canvas>
          </div>
          
          <small class="helper-text">
            白色区域（涂抹部分）表示需要重绘的部分，黑色区域表示保留的部分。<br>
            提示: 使用画笔涂抹要修改的区域，使用橡皮擦移除不需要修改的部分。
          </small>
        </div>

        <div class="form-group">
          <label for="prompt">提示词</label>
          <textarea 
            id="prompt" 
            v-model="formData.prompt"
            placeholder="描述您希望重绘的内容，例如：给人物添加一顶帽子，将背景改为海滩场景..."
            class="form-control"
            rows="5"
          ></textarea>
          <small>详细的描述可以帮助AI更好地理解您的需求，提供清晰的指导</small>
        </div>

        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateImage" class="btn btn-primary" :disabled="isLoading || !previewImage">
            <i class="ri-magic-line" v-if="!isLoading"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isLoading ? '处理中...' : '开始重绘' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>

      <!-- 右侧显示区域 -->
      <div class="right-column">
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-image-line"></i>
              重绘结果
            </h3>
          </div>

          <div class="result-content-wrapper">
            <!-- 加载中显示 -->
            <div class="loading-overlay" v-if="isLoading">
              <div class="loading-spinner"></div>
              <div class="loading-text">正在处理图片，请稍候...</div>
              <div class="loading-status" v-if="taskStatus">{{ taskStatus }}</div>
            </div>
            
            <!-- 空状态显示 -->
            <div class="empty-result" v-else-if="!resultImage">
              <div class="empty-content">
                <i class="ri-image-add-line" style="font-size: 64px; color: #e9ecef;"></i>
                <div class="empty-message">请上传基础图片，填写提示词后点击"开始重绘"按钮</div>
              </div>
            </div>
            
            <!-- 处理结果显示 -->
            <div class="result-comparison" v-else>
              <div class="image-container original">
                <h4>原始图片</h4>
                <div class="image-wrapper">
                  <img :src="previewImage" alt="原始图片">
                </div>
              </div>
              <div class="image-arrow">
                <i class="ri-arrow-right-line"></i>
              </div>
              <div class="image-container result">
                <h4>重绘结果</h4>
                <div class="image-wrapper">
                  <img :src="resultImage" alt="重绘后的图片">
                  <div class="image-overlay">
                    <button @click="downloadImage(resultImage)" class="overlay-button">
                      <i class="ri-download-line"></i>
                      下载图片
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 错误信息 -->
            <div class="error-message" v-if="error">
              <i class="ri-error-warning-line"></i>
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创作小贴士模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> 局部重绘小贴士</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <h4>AI局部重绘使用指南</h4>
          
          <div class="tips-section">
            <h5>使用场景</h5>
            <ul>
              <li><strong>换装</strong>：修改衣服颜色、款式等</li>
              <li><strong>替换局部物件</strong>：如将桌上的茶杯替换为花瓶</li>
              <li><strong>删除干扰物</strong>：去除旅游照片中的遮挡物或路人</li>
            </ul>
          </div>
          
          <div class="tips-section">
            <h5>提示词技巧</h5>
            <p><strong>增加或修改操作</strong>的提示词有两种方式：</p>
            <ol>
              <li>描述具体动作，例如"给小狗添加一顶帽子"</li>
              <li>客观描述期望生成的内容，例如"一只戴着帽子的小狗"</li>
            </ol>
            <p><strong>删除操作</strong>的提示词策略：</p>
            <ul>
              <li>删除占据空间较少的元素时，可以留空提示词 (prompt="")</li>
              <li>删除占据空间较大的元素时，需要详细描述擦除后的内容，例如"一个透明玻璃花瓶放在桌子上"，而非简单描述为"删除xxx"</li>
            </ul>
          </div>
          
          <div class="tips-section">
            <h5>蒙版绘制指南</h5>
            <p>上传图片后，您可以直接在图片上涂抹指定需要重绘的区域：</p>
            <ul>
              <li>使用<strong>画笔工具</strong>涂抹您想要AI重新生成的区域（白色）</li>
              <li>使用<strong>橡皮擦</strong>清除不需要修改的部分（恢复为黑色）</li>
              <li>调整<strong>笔刷大小</strong>以便于精确绘制</li>
              <li>点击<strong>清除全部</strong>可以重新开始</li>
              <li>白色区域表示需要重绘的部分，黑色区域表示保留的部分</li>
            </ul>
          </div>
          
          <div class="tips-section">
            <h5>最佳实践</h5>
            <ul>
              <li>蒙版区域不宜过大，建议控制在图像的30%以内</li>
              <li>提供足够详细的提示词，描述期望的重绘结果</li>
              <li>图片处理可能需要30-60秒，请耐心等待</li>
              <li>尝试使用不同的提示词以获得最佳效果</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageRedraw',
  
  data() {
    return {
      formData: {
        prompt: '',
        base_image_url: '',
        mask_image_url: ''
      },
      isLoading: false,
      error: null,
      previewImage: null,
      resultImage: null,
      taskId: null,
      taskStatus: '',
      showTipsModal: false,
      pollingInterval: null,
      
      // 画布相关数据
      currentTool: 'brush', // 'brush' 或 'eraser'
      brushSize: 20,
      isDrawing: false,
      lastX: 0,
      lastY: 0,
      canvas: null,
      ctx: null,
      maskDataUrl: null
    }
  },

  methods: {
    showTips() {
      this.showTipsModal = true;
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleFileChange(event) {
      const file = event.target.files[0];
      this.handleImage(file);
    },

    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.handleImage(file);
    },

    handleImage(file) {
      if (!file || !file.type.startsWith('image/')) {
        this.error = '请上传有效的图片文件';
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
        this.error = null;
        
        // 实际环境下上传图片到服务器
        this.uploadImage(file);
      };
      reader.readAsDataURL(file);
    },

    resetForm() {
      this.formData = {
        prompt: '',
        base_image_url: '',
        mask_image_url: ''
      };
      this.previewImage = null;
      this.resultImage = null;
      this.error = null;
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
      this.clearCanvas();
    },

    async uploadImage(file) {
      try {
        this.isLoading = true;
        this.error = null;
        this.taskStatus = '正在上传基础图片...';
        
        // 调试：本地先设置URL备用
        // 上传失败时也可以使用本地预览图
        this.formData.base_image_url = this.previewImage;
        console.log('已设置临时本地基础图片URL:', this.previewImage.substring(0, 50) + '...');
        
        const formData = new FormData();
        formData.append('image', file);
        
        console.log('开始上传基础图片到服务器...');
        
        // 增加超时和重试逻辑
        let response;
        let retryCount = 0;
        const maxRetries = 2;
        
        while (retryCount <= maxRetries) {
          try {
            response = await Promise.race([
              fetch('http://localhost:3000/api/images/upload', {
                method: 'POST',
                body: formData
              }),
              new Promise((_, reject) => 
                setTimeout(() => reject(new Error('请求超时')), 10000)
              )
            ]);
            break; // 成功获取响应，跳出循环
          } catch (fetchError) {
            console.error(`上传尝试 ${retryCount + 1}/${maxRetries + 1} 失败:`, fetchError);
            retryCount++;
            
            if (retryCount <= maxRetries) {
              this.taskStatus = `上传失败，正在尝试第 ${retryCount + 1} 次重试...`;
              await new Promise(resolve => setTimeout(resolve, 1000)); // 等待1秒后重试
            } else {
              throw fetchError; // 达到最大重试次数，抛出错误
            }
          }
        }
        
        console.log('服务器响应状态:', response.status);
        
        // 调试：检查响应类型
        const contentType = response.headers.get("content-type");
        console.log('响应Content-Type:', contentType);
        
        if (contentType && contentType.includes("application/json")) {
          const result = await response.json();
          console.log('上传结果:', result);
          
          if (result.success) {
            this.formData.base_image_url = result.file.url;
            console.log('基础图片上传成功，URL已设置:', this.formData.base_image_url);
            this.taskStatus = '基础图片上传成功';
          } else {
            console.error('服务器返回上传失败:', result.error);
            // 不抛出错误，继续使用本地URL
            this.taskStatus = '服务器上传失败，将使用本地图片（功能可能受限）';
          }
        } else {
          // 如果不是JSON响应，尝试读取文本内容
          const textContent = await response.text();
          console.error('服务器返回非JSON数据:', textContent.substring(0, 150) + '...');
          this.error = '服务器响应格式错误，请检查接口';
          this.taskStatus = '上传失败：服务器响应格式错误';
        }
      } catch (error) {
        console.error('上传基础图片过程中出错:', error);
        
        // 更明确的错误信息
        if (error.message === 'Failed to fetch') {
          this.error = '上传失败：无法连接到服务器，请检查服务器是否运行';
          this.taskStatus = '上传失败：无法连接到服务器';
        } else if (error.message === '请求超时') {
          this.error = '上传失败：请求超时，服务器响应时间过长';
          this.taskStatus = '上传失败：请求超时';
        } else {
          this.error = `上传失败：${error.message || '未知错误'}`;
          this.taskStatus = '上传失败：' + (error.message || '未知错误');
        }
        
        // 仍然使用本地URL
        console.log('上传失败，将使用本地图片URL');
      } finally {
        this.isLoading = false;
        // 确保imageUrl已设置，否则使用预览URL
        if (!this.formData.base_image_url) {
          this.formData.base_image_url = this.previewImage;
          console.log('使用本地预览图URL作为备用');
        }
        
        // 验证最终设置的imageUrl
        console.log('最终基础图片URL:', this.formData.base_image_url ? '已设置' : '未设置');
      }
    },

    async generateImage() {
      // 验证输入
      if (!this.formData.base_image_url) {
        this.error = '请上传基础图片';
        return;
      }
      
      // 确保蒙版图片已生成
      if (this.maskDataUrl) {
        this.formData.mask_image_url = this.maskDataUrl;
      } else {
        // 如果用户没有涂抹，询问是否要处理整张图片
        if (!confirm('您没有涂抹任何区域，将对整张图片进行处理。是否继续？')) {
          return;
        }
        // 创建一个全白的蒙版图片（处理整张图片）
        if (this.canvas) {
          this.ctx.fillStyle = 'white';
          this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
          this.maskDataUrl = this.canvas.toDataURL('image/png');
          this.formData.mask_image_url = this.maskDataUrl;
        }
      }
      
      try {
        this.isLoading = true;
        this.error = null;
        this.resultImage = null;
        this.taskId = null;
        this.taskStatus = '正在创建任务...';
        
        // 发送API请求创建任务
        const createResponse = await fetch('/api/v1/image_redraw/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });
        
        const createResult = await createResponse.json();
        
        if (!createResult.success) {
          throw new Error(createResult.error || '创建任务失败');
        }
        
        this.taskId = createResult.data.task_id;
        this.taskStatus = `任务已创建，ID: ${this.taskId}`;
        
        // 轮询查询任务状态
        this.startPolling();
      } catch (err) {
        this.isLoading = false;
        this.error = err.message || '发生错误，请重试';
        console.error('生成图片错误:', err);
      }
    },

    startPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }
      
      let failedAttempts = 0;
      const maxFailedAttempts = 5;
      let pollingCount = 0;
      const maxPollingCount = 60; // 最多轮询60次，约2分钟
      
      this.pollingInterval = setInterval(async () => {
        try {
          pollingCount++;
          console.log(`开始第${pollingCount}次轮询，任务ID: ${this.taskId}`);
          
          // 检查是否超过最大轮询次数
          if (pollingCount > maxPollingCount) {
            console.log(`已达到最大轮询次数(${maxPollingCount})，停止轮询`);
            clearInterval(this.pollingInterval);
            this.isLoading = false;
            this.error = '任务处理时间过长，请稍后在历史记录中查看结果';
            return;
          }
          
          let statusResponse;
          try {
            // 使用阿里云图片局部重绘API查询任务
            statusResponse = await Promise.race([
              fetch(`http://localhost:9000/api/v1/image_redraw/query/${this.taskId}`, {
                headers: {
                  'Content-Type': 'application/json'
                }
              }),
              new Promise((_, reject) => 
                setTimeout(() => reject(new Error('请求超时')), 5000)
              )
            ]);
          } catch (fetchError) {
            failedAttempts++;
            console.error(`轮询失败 (${failedAttempts}/${maxFailedAttempts}):`, fetchError);
            
            if (failedAttempts >= maxFailedAttempts) {
              throw new Error('多次轮询失败，请检查网络连接');
            }
            
            // 不中断轮询，等待下一次尝试
            this.taskStatus = `查询任务状态失败，将在2秒后重试 (${failedAttempts}/${maxFailedAttempts})`;
            return;
          }
          
          // 重置失败计数
          failedAttempts = 0;
          
          const statusResult = await statusResponse.json();
          console.log('任务状态查询结果:', statusResult);
          
          if (!statusResult.success) {
            throw new Error(statusResult.error || '查询任务状态失败');
          }
          
          // 从阿里云API响应中获取状态信息
          const taskData = statusResult.data;
          const status = taskData.task_status;
          
          // 更新任务状态
          if (status === 'SUCCEEDED' && taskData.image_urls && taskData.image_urls.length > 0) {
            // 任务成功完成，获取第一个图片URL
            clearInterval(this.pollingInterval);
            this.isLoading = false;
            this.taskStatus = '处理完成';
            this.resultImage = taskData.image_urls[0];
            
            // 如果有完成时间，显示
            if (taskData.submit_time && taskData.end_time) {
              this.taskStatus = `处理完成，提交于 ${taskData.submit_time}，完成于 ${taskData.end_time}`;
            }
            
            console.log(`任务完成，结果URL: ${this.resultImage}`);
          } else if (status === 'FAILED' || status === 'ERROR') {
            // 任务失败
            clearInterval(this.pollingInterval);
            this.isLoading = false;
            throw new Error('任务处理失败');
          } else if (status === 'RUNNING' || status === 'PENDING') {
            // 任务处理中
            this.taskStatus = `任务正在${status === 'RUNNING' ? '处理中' : '等待处理'}，请耐心等待...`;
          } else {
            // 其他状态
            this.taskStatus = `任务状态：${status}`;
          }
        } catch (error) {
          clearInterval(this.pollingInterval);
          this.isLoading = false;
          this.error = `处理失败：${error.message || '未知错误'}`;
          console.error('处理任务状态时出错:', error);
        }
      }, 2000); // 每2秒查询一次
    },

    downloadImage(url) {
      const fileName = `重绘结果_${new Date().toISOString().slice(0,10)}.jpg`;
      
      // 如果是远程URL，需要先获取图片
      if (url.startsWith('http')) {
        fetch(url)
          .then(response => response.blob())
          .then(blob => {
            const blobUrl = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
          })
          .catch(error => {
            console.error('下载图片失败:', error);
            this.error = '下载图片失败';
          });
      } else {
        // 本地Base64图片直接下载
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    },

    // 设置当前工具
    setTool(tool) {
      this.currentTool = tool;
    },
    
    // 初始化画布
    initCanvas() {
      const baseImg = this.$refs.baseImage;
      
      if (!baseImg || !this.$refs.maskCanvas) return;
      
      // 等待图片加载完成
      if (!baseImg.complete) {
        baseImg.onload = () => this.initCanvas();
        return;
      }
      
      const canvas = this.$refs.maskCanvas;
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      
      // 设置画布尺寸与图片相同
      canvas.width = baseImg.naturalWidth;
      canvas.height = baseImg.naturalHeight;
      
      // 清除画布
      this.ctx.fillStyle = 'rgba(0, 0, 0, 0)';
      this.ctx.fillRect(0, 0, canvas.width, canvas.height);
      this.ctx.lineJoin = 'round';
      this.ctx.lineCap = 'round';
    },
    
    // 开始绘制
    startDrawing(e) {
      this.isDrawing = true;
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      
      this.lastX = (e.clientX - rect.left) * scaleX;
      this.lastY = (e.clientY - rect.top) * scaleY;
    },
    
    // 处理触摸开始事件
    handleTouchStart(e) {
      e.preventDefault();
      const touch = e.touches[0];
      const mouseEvent = new MouseEvent('mousedown', {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      this.startDrawing(mouseEvent);
    },
    
    // 处理触摸移动事件
    handleTouchMove(e) {
      e.preventDefault();
      if (!this.isDrawing) return;
      
      const touch = e.touches[0];
      const mouseEvent = new MouseEvent('mousemove', {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      this.draw(mouseEvent);
    },
    
    // 绘制
    draw(e) {
      if (!this.isDrawing) return;
      
      const rect = this.canvas.getBoundingClientRect();
      const scaleX = this.canvas.width / rect.width;
      const scaleY = this.canvas.height / rect.height;
      
      const currentX = (e.clientX - rect.left) * scaleX;
      const currentY = (e.clientY - rect.top) * scaleY;
      
      this.ctx.lineWidth = this.brushSize;
      
      // 设置绘制模式
      if (this.currentTool === 'brush') {
        this.ctx.strokeStyle = 'white';
        this.ctx.globalCompositeOperation = 'source-over';
      } else {
        this.ctx.strokeStyle = 'black';
        this.ctx.globalCompositeOperation = 'destination-out';
      }
      
      this.ctx.beginPath();
      this.ctx.moveTo(this.lastX, this.lastY);
      this.ctx.lineTo(currentX, currentY);
      this.ctx.stroke();
      
      this.lastX = currentX;
      this.lastY = currentY;
      
      // 更新蒙版数据
      this.updateMaskDataUrl();
    },
    
    // 停止绘制
    stopDrawing() {
      this.isDrawing = false;
    },
    
    // 清除画布
    clearCanvas() {
      if (this.ctx) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.updateMaskDataUrl();
      }
    },
    
    // 更新蒙版数据URL
    updateMaskDataUrl() {
      if (this.canvas) {
        this.maskDataUrl = this.canvas.toDataURL('image/png');
        this.formData.mask_image_url = this.maskDataUrl;
      }
    }
  },

  beforeDestroy() {
    // 清除轮询定时器
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }
  }
}
</script>

<style scoped>
.content {
  padding: 24px;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-nav h2 {
  font-size: 24px;
  color: #212529;
  margin: 0;
}

.action-btn {
  background: none;
  border: none;
  color: #ba003f;
  cursor: pointer;
  padding: 8px;
  font-size: 20px;
  transition: color 0.3s;
}

.action-btn:hover {
  color: #d4004d;
}

.function-container {
  display: flex;
  gap: 24px;
}

.form-container {
  width: 320px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  color: #212529;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title i {
  color: #ba003f;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #212529;
}

.form-group label.required::after {
  content: '*';
  color: #ba003f;
  margin-left: 4px;
}

.upload-area {
  border: 2px dashed #e9ecef;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #f8f9fa;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #ba003f;
}

.upload-placeholder {
  color: #6c757d;
}

.upload-placeholder i {
  font-size: 48px;
  margin-bottom: 10px;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #ba003f;
  outline: none;
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.form-group small {
  display: block;
  margin-top: 4px;
  color: #6c757d;
  font-size: 12px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-primary {
  background: #ba003f;
  color: white;
  border: none;
  flex: 2;
}

.btn-primary:hover:not(:disabled) {
  background: #d4004d;
}

.btn-secondary {
  background: white;
  color: #212529;
  border: 1px solid #e9ecef;
  flex: 1;
}

.btn-secondary:hover {
  background: #e9ecef;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.reference-section, .result-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.function-info {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.function-info h4 {
  color: #ba003f;
  margin-top: 0;
  margin-bottom: 10px;
}

.function-tips {
  margin-top: 15px;
}

.function-tips h5 {
  color: #212529;
  margin-bottom: 8px;
}

.function-tips ul {
  padding-left: 20px;
}

.function-tips li {
  margin-bottom: 5px;
  color: #495057;
}

.result-content-wrapper {
  position: relative;
  min-height: 400px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e9ecef;
  border-top-color: #ba003f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 16px;
  color: #212529;
  font-weight: 500;
}

.loading-status {
  margin-top: 8px;
  color: #6c757d;
  font-size: 14px;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.empty-content {
  text-align: center;
}

.empty-message {
  margin-top: 16px;
  color: #6c757d;
}

.result-comparison {
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-wrap: wrap;
  padding: 20px;
}

.image-container {
  text-align: center;
  flex: 1;
  min-width: 300px;
  margin-bottom: 20px;
}

.image-container h4 {
  margin-bottom: 12px;
  color: #212529;
}

.image-arrow {
  font-size: 32px;
  color: #6c757d;
  margin: 0 20px;
}

.image-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-wrapper:hover .image-overlay {
  opacity: 1;
}

.overlay-button {
  background: #ba003f;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
  font-weight: 500;
}

.overlay-button:hover {
  background: #d4004d;
}

.image-container img {
  display: block;
  width: 100%;
  max-height: 400px;
  object-fit: contain;
}

.error-message {
  margin-top: 16px;
  padding: 12px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #212529;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-header h3 i {
  color: #ba003f;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6c757d;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #212529;
}

.modal-body {
  padding: 20px;
}

.modal-body h4 {
  margin-top: 0;
  color: #212529;
}

.tips-section {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

.tips-section:last-child {
  border-bottom: none;
}

.tips-section h5 {
  color: #ba003f;
  margin-bottom: 8px;
}

.spinning {
  animation: spin 1s linear infinite;
}

.drawing-tools {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 10px;
}

.tool-btn {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  background: white;
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.tool-btn:hover {
  border-color: #ba003f;
  color: #ba003f;
}

.tool-btn.active {
  background: #ba003f;
  color: white;
  border-color: #ba003f;
}

.brush-size {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.size-slider {
  width: 100px;
}

.canvas-container {
  position: relative;
  width: 100%;
  margin-bottom: 16px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.base-image {
  display: block;
  width: 100%;
  height: auto;
}

.mask-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: crosshair;
}

@media (max-width: 768px) {
  .function-container {
    flex-direction: column;
  }
  
  .form-container {
    width: 100%;
  }
  
  .image-arrow {
    transform: rotate(90deg);
    margin: 20px 0;
  }
}
</style> 