<script setup>
import { onMounted, onUnmounted } from 'vue';
import CktDesign from "@chuangkit/chuangkit-design";
import CryptoJS from "crypto-js";
import store from "@/store";

/**
 * 构建签名
 * @param obj 参数对象，对象中的所有属性全部参与签名的生成
 * @returns {string} 签名
 */
const buildSign = obj => {
  let signParameterArray = [];
  for (let key in obj) {
    signParameterArray.push(`${key}=${obj[key]}`)
  }

  let signPlaintext = signParameterArray.sort().join("&");
  return CryptoJS.MD5(signPlaintext)
      .toString()
      .toUpperCase();
}

/**
 * 构建ai功能签名
 * @param appId 第三方企业id
 * @param appSecret 企业密钥
 * @param timestamp 时间戳，取当前时间即可
 * @param unionId 用户标识
 * @returns {string} 签名
 */
const buildAIProgramSign = (appId, appSecret, timestamp, unionId) => {
  let signParameterObj = {
    app_id: appId,
    timestamp: timestamp,
    union_id: unionId,
    app_secret: appSecret
  }

  return buildSign(signParameterObj);
}

// AI图片转设计实例
let instance = null;

// 打开AI图片转设计
const openPainter = () => {
  const appId = "54d9adec77d0402794018d166110f3dd";
  const appSecret = "08097010E0EF4B85EE2B8CE438328249";
  const unionId = store.state.user?.id || 'default_user';
  const timestamp = Date.now();
  const sign = buildAIProgramSign(appId, appSecret, timestamp, unionId);
  
  let params = {
    appId: appId,
    unionId: unionId,
    timestamp: timestamp,
    sign: sign,
    container: "#ai-painter-container",
    companyFlag: "ezijing", // 创客贴提供的公司标记
    device_type: 1,
    mParam: "3", // 新增参数
    aigc_env: 1   // 新增参数
  }
  
  console.log("初始化AI图片转设计实例:", params);
  
  instance = CktDesign.createAiPainter(params);
  instance.open()
    .then(() => {
      console.log("AI图片转设计打开成功");
      
      // 监听生成回调
      instance.onGenerate(res => console.log("图片生成事件:", res)); 
      
      // 监听下载回调
      instance.onDownload(res => console.log("图片下载事件:", res));
    })
    .catch(err => console.error("打开AI图片转设计失败:", err));
}

// 关闭AI图片设计
const closePainter = () => {
  if (instance) {
    try {
      instance.close();
      instance = null;
    } catch (error) {
      console.error("关闭AI图片转设计失败:", error);
    }
  }
};

// 生命周期钩子
onMounted(() => {
  openPainter();
});

onUnmounted(() => {
  closePainter();
});
</script>

<template>
  <div id="ai-painter-container"></div>
</template>

<style scoped>
#ai-painter-container {
  width: 100%;
  height: 85vh;
}
</style> 