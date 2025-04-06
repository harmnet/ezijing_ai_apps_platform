// 浏览器控制台测试脚本
const pptUrl = "https://ezijingai.oss-cn-beijing.aliyuncs.com/media_upload/customize/user-upload/scene/pdf/7f5964ffc65643ae8b1bcb632710b556_testppt.pptx";
async function testDigitalHumanDemo() {
  console.log("开始测试数字人PPT讲解视频生成流程");
  try {
    const app = document.querySelector(".dh-demo-container").__vue__;
    if (!app) {
      console.error("未找到Vue实例");
      return;
    }
    console.log("1. 设置PPT URL:", pptUrl);
    app.form.pptUrl = pptUrl;
    app.form.pptFileName = "testppt.pptx";
    console.log("2. 获取PPT信息...");
    const pageCount = 4;
    console.log("3. 获取到PPT页数:", pageCount);
    app.generateScenesFromPPT(pageCount);
    console.log("4. 场景生成完成");
    console.log("5. 生成请求数据");
    app.generateRequestData();
    console.log("6. 请求数据准备完成:", app.requestReady);
    console.log("请求URL:", app.requestUrl);
    console.log("场景数量:", app.requestData.creationDetail.scenes.length);
  } catch (error) {
    console.error("测试过程中出现错误:", error);
  }
}
testDigitalHumanDemo();
