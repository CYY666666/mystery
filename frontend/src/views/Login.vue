
<template>
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item label="用户名">
      <el-input v-model="form.username" @input="change($event)"></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="form.password" show-password  @input="change($event)"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="login()">登录</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { Component, Watch, Vue } from 'vue-property-decorator'
import { loginApi } from '../api/http/userApi'
export default class Login extends Vue {
  form = {
    username: '',
    password: ''
  }

  async login () {
    const res = await loginApi(this.form)
    const tmp = (res as any).data.access_token as any
    localStorage.setItem('token', tmp)
    this.$router.push({ name: 'Customer' })
  }

  change (e: any) {
    this.$forceUpdate()
  }

  created () {
    this.form = {
      username: '',
      password: ''
    }
  }
}
</script>
