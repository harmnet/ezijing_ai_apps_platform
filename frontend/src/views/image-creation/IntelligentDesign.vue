<script setup>
import { onMounted, onUnmounted } from "vue";
import CktDesign from "@chuangkit/chuangkit-design";
import CryptoJS from "crypto-js";
import store from "@/store";

/**
 * 构建签名
 * @param obj 参数对象，对象中的所有属性全部参与签名的生成
 * @returns {string} 签名
 */
const buildSign = (obj) => {
  let signParameterArray = [];
  for (let key in obj) {
    signParameterArray.push(`${key}=${obj[key]}`);
  }

  let signPlaintext = signParameterArray.sort().join("&");
  return CryptoJS.MD5(signPlaintext).toString().toUpperCase();
};

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
    app_secret: appSecret,
  };

  return buildSign(signParameterObj);
};

/**
 * 构建模板编辑器签名
 * @param appId 第三方企业id
 * @param expireTime 时间戳，取当前时间即可
 * @param userFlag 用户标识
 * @param appSecret 企业密钥
 * @returns {string} 签名
 */
const buildVersion2Sign = (appId, expireTime, userFlag, appSecret) => {
  let signParameterObj = {
    app_id: appId,
    expire_time: expireTime,
    user_flag: userFlag,
    app_secret: appSecret
  }

  return buildSign(signParameterObj);
}

// AI设计实例
let instance = null;
// 模板编辑器实例
let cktInstance = null;

// 全局方法，用于接收设计完成回调
window.chuangkitComplete = (result) => {
  console.log("设计完成回调:", result);
  if (result && result.designId) {
    console.log("获取到设计ID:", result.designId);
    // 关闭AI编辑器
    if (instance) {
      try {
        instance.close();
        instance = null;
      } catch (e) {
        console.error("关闭AI编辑器失败", e);
      }
    }
    // 打开模板编辑器进行高级编辑
    openDesignPage(result.designId);
  }
}

// 初始化并打开AI编辑器
const openEditor = () => {
  // 关闭可能存在的模板编辑器
  if (cktInstance) {
    try {
      cktInstance.close();
      cktInstance = null;
    } catch (e) {
      console.error("关闭模板编辑器失败", e);
    }
  }

  // 基本参数
  const appId = "54d9adec77d0402794018d166110f3dd";
  const appSecret = "08097010E0EF4B85EE2B8CE438328249";
  const unionId = store.state.user?.id || 'default_user';
  const timestamp = Date.now();
  const sign = buildAIProgramSign(appId, appSecret, timestamp, unionId);

  // 参数对象
  const params = {
    appId,
    unionId,
    timestamp,
    sign,
    type: 1
  };

  console.log("初始化AI设计实例:", params);
  
  // 创建实例
  instance = CktDesign.createAiDesign(params);
  
  // 打开编辑器
  instance.open()
    .then(() => {
      console.log("AI编辑器打开成功");
      
      // 注册事件
      instance.onSend(res => console.log("设计发送事件:", res));
      instance.onGenerateAgain(res => console.log("重新生成事件:", res));
    })
    .catch(err => console.error("打开AI编辑器失败:", err));
};

// 打开模板编辑器(高级编辑)
const openDesignPage = (designId) => {
  const appId = "54d9adec77d0402794018d166110f3dd";
  const appSecret = "08097010E0EF4B85EE2B8CE438328249";
  const userFlag = store.state.user?.id || 'default_user';
  const expireTime = Date.now() + 300000; // 有效期5分钟
  const sign = buildVersion2Sign(appId, expireTime, userFlag, appSecret);
  
  // 模板编辑器基础参数
  const params = {
    app_id: appId,
    expire_time: expireTime,
    user_flag: userFlag,
    device_type: 1,
    version: "2.0",
    sign: sign
  };
  
  // 根据官方文档，如果有设计ID，使用design_id（下划线形式）
  // kind_id、template_id、design_id和random_id这四个参数四选一
  if (designId) {
    params.design_id = designId; // 正确的参数名应该是design_id而不是designId
  } else {
    // 如果没有设计ID，则使用场景ID
    params.kind_id = 447;
  }
  
  console.log("打开模板编辑器，参数:", params);
  
  // 创建并打开模板编辑器 - 注意：open方法不返回Promise
  try {
    cktInstance = new CktDesign(params);
    cktInstance.open();
    console.log("模板编辑器打开请求已发送");
  } catch (err) {
    console.error("打开模板编辑器失败:", err);
  }
};

// 关闭AI编辑器
const closeEditor = () => {
  if (instance) {
    try {
      instance.close();
      instance = null;
    } catch (error) {
      console.error("关闭AI编辑器失败:", error);
    }
  }
  
  // 同时确保模板编辑器也被关闭
  if (cktInstance) {
    try {
      cktInstance.close();
      cktInstance = null;
    } catch (error) {
      console.error("关闭模板编辑器失败:", error);
    }
  }
};

// 生命周期钩子
onMounted(() => {
  openEditor();
});

onUnmounted(() => {
  closeEditor();
});
</script>

<template>
  <div class="intelligent-design-container"></div>
</template>

<style scoped>
.intelligent-design-container {
  width: 100%;
  height: 100%;
  min-height: 600px;
}
</style>
