const axios = require("axios");
const pptUrl = "https://ezijingai.oss-cn-beijing.aliyuncs.com/media_upload/customize/user-upload/scene/pdf/7f5964ffc65643ae8b1bcb632710b556_testppt.pptx";

async function testWorkflow() {
  console.log("开始测试完整工作流程");
  console.log("1. 假设PPT文件已上传，URL为:", pptUrl);
  
  try {
    console.log("2. 调用PPT信息获取API");
    const pptInfoResponse = await axios.post("http://localhost:9000/api/v1/aibeings/ppt/info", 
      { pptUrl: pptUrl }, 
      { headers: { "Content-Type": "application/json" }, timeout: 30000 }
    );
    
    console.log("3. PPT信息获取成功:", pptInfoResponse.data);
    const pageCount = pptInfoResponse.data.pageCount;
    
    console.log("4. 根据页数生成场景配置 (", pageCount, "个场景)");
    console.log("5. 模拟发送请求到小冰API...");
    const headers = {
      "subscription-key": "282cd94b697e48e6aca6d20bbdaf0d0f",
      "Content-Type": "application/json"
    };
    console.log("6. 使用的认证头:", JSON.stringify(headers));
    console.log("7. API请求URL: https://openapi.xiaoice.com/vh/openapi/video/task/v2/ppt/submit");
    console.log("8. 测试完成");
  } catch (error) {
    console.error("测试过程中出现错误:", error.message);
  }
}

testWorkflow();
