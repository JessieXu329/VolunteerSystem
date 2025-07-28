<template>
  <div class="signup-container">
    <el-container>
      <el-main>
        <el-card class="signup-card">
          <template #header>
            <div class="card-header">
              <h2>活动报名</h2>
            </div>
          </template>
          <div v-if="activity" class="activity-details">
            <h3>{{ activity.title }}</h3>
            <p class="description">{{ activity.description }}</p>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="活动时间">{{ new Date(activity.date).toLocaleString() }}</el-descriptions-item>
              <el-descriptions-item label="活动地点">{{ activity.location }}</el-descriptions-item>
              <el-descriptions-item label="招募人数">{{ activity.slots }}</el-descriptions-item>
              <el-descriptions-item label="活动类别">{{ activity.get_category_display }}</el-descriptions-item>
            </el-descriptions>
            
            <el-form :model="form" :rules="rules" ref="formRef" class="signup-form" label-width="100px">
              <el-form-item label="姓名" prop="name">
                <el-input v-model="form.name" placeholder="请输入您的姓名"></el-input>
              </el-form-item>
              <el-form-item label="手机号码" prop="phone">
                <el-input v-model="form.phone" placeholder="请输入您的手机号码"></el-input>
              </el-form-item>
              <el-form-item label="备注" prop="notes">
                <el-input v-model="form.notes" type="textarea" placeholder="如有特殊需求请在此说明"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitForm">提交报名</el-button>
                <el-button @click="goBack">返回列表</el-button>
              </el-form-item>
            </el-form>
          </div>
          <div v-else class="loading">
            <el-empty description="加载中..."></el-empty>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const route = useRoute();
const router = useRouter();
const activity = ref(null);
const formRef = ref(null);

const form = ref({
  name: '',
  phone: '',
  notes: ''
});

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  notes: [{ max: 200, message: '备注不能超过200个字符', trigger: 'blur' }]
};

const fetchActivity = async () => {
  try {
    const response = await axios.get(`/api/activities/${route.params.id}/`);
    activity.value = response.data;
  } catch (error) {
    ElMessage.error('获取活动信息失败');
    console.error('获取活动信息失败:', error);
  }
};

const submitForm = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    const response = await axios.post(`/api/activities/${route.params.id}/signup/`, form.value);
    if (response.data.success) {
      ElMessage.success('报名成功！');
      router.push('/');
    } else {
      ElMessage.error(response.data.message || '报名失败，请稍后重试');
    }
  } catch (error) {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message);
    } else {
      ElMessage.error('报名失败，请稍后重试');
    }
    console.error('提交报名失败:', error);
  }
};

const goBack = () => {
  router.push('/');
};

onMounted(() => {
  fetchActivity();
});
</script>

<style scoped>
.signup-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.signup-card {
  margin-bottom: 20px;
}

.card-header {
  text-align: center;
}

.activity-details {
  margin-bottom: 30px;
}

.description {
  margin: 20px 0;
  color: #666;
}

.signup-form {
  margin-top: 30px;
}

.loading {
  padding: 40px 0;
}
</style>