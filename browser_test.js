// 浏览器控制台测试脚本
const pptUrl = "https://ezijingai.oss-cn-beijing.aliyuncs.com/media_upload/customize/user-upload/scene/pdf/7f5964ffc65643ae8b1bcb632710b556_testppt.pptx";
console.log("开始测试数字人demo页面");
const app = document.querySelector(".dh-demo-container").__vue__;
if (app) {
  console.log("找到Vue应用实例");
  app.form.pptUrl = pptUrl;
  app.form.pptFileName = "7f5964ffc65643ae8b1bcb632710b556_testppt.pptx";
  console.log("已设置PPT URL:", pptUrl);
  console.log("PPT页数设置为4");
  if (typeof app.generateScenesFromPPT === "function") {
    app.generateScenesFromPPT(4);
    console.log("场景已生成");
  }
  if (typeof app.generateRequestData === "function") {
    app.generateRequestData();
    console.log("请求数据已准备");
  }
} else {
  console.error("未找到Vue实例");
}
