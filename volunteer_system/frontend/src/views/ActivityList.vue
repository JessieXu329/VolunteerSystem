<template>
  <div class="activity-list-container">
    <el-container>
      <el-header class="header">
        <h1>志愿活动列表</h1>
        <p>欢迎参加我们的志愿活动！</p>
      </el-header>
      <el-main>
        <div class="filters">
          <el-input v-model="searchQuery" placeholder="搜索活动..." @keyup.enter="fetchActivities" style="width: 200px; margin-right: 10px;"></el-input>
          <el-select v-model="selectedCategory" placeholder="所有类别" @change="fetchActivities">
            <el-option label="所有类别" value=""></el-option>
            <el-option v-for="(label, value) in categories" :key="value" :label="label" :value="value"></el-option>
          </el-select>
          <el-button type="primary" @click="fetchActivities" style="margin-left: 10px;">筛选</el-button>
          <el-button @click="clearFilters">清除筛选</el-button>
        </div>
        <el-row :gutter="20">
          <el-col :span="8" v-for="activity in activities" :key="activity.id">
            <el-card class="activity-card">
              <template #header>
                <div class="card-header">
                  <span>{{ activity.title }}</span>
                  <el-tag size="small">{{ activity.get_category_display }}</el-tag>
                </div>
              </template>
              <p>{{ activity.description }}</p>
              <p><strong>时间:</strong> {{ new Date(activity.date).toLocaleString() }}</p>
              <p><strong>地点:</strong> {{ activity.location }}</p>
              <p><strong>招募人数:</strong> {{ activity.slots }}</p>
              <el-button type="primary" @click="signUp(activity.id)">立即报名</el-button>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="activities.length === 0" description="没有找到符合条件的活动。"></el-empty>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const activities = ref([]);
const searchQuery = ref('');
const selectedCategory = ref('');
const categories = ref({}); // 将从后端获取
const router = useRouter();

const fetchActivities = async () => {
  try {
    const response = await axios.get('/api/activities/', {
      params: {
        search: searchQuery.value,
        category: selectedCategory.value
      }
    });
    activities.value = response.data.activities;
    categories.value = response.data.categories;
  } catch (error) {
    console.error('获取活动列表失败:', error);
  }
};

const clearFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  fetchActivities();
};

const signUp = (activityId) => {
  router.push({ name: 'SignUp', params: { id: activityId } });
};

onMounted(() => {
  fetchActivities();
});
</script>

<style scoped>
.activity-list-container {
  padding: 20px;
}
.header {
  text-align: center;
}
.filters {
  margin-bottom: 20px;
}
.activity-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>