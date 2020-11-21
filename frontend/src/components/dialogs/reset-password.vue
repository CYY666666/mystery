<template>
  <el-dialog
    title=修改密码
    v-if="Boolean(passwordReset)"
    :visible="Boolean(passwordReset)"
    :before-close="cancel"
    width="55%">
    <el-form :model="form" ref="form" label-width="100px" class="demo-ruleForm">
      <el-form-item label="密码" required>
        <el-input v-model="form.password" show-password></el-input>
      </el-form-item>
      <el-form-item label="确认密码" required>
        <el-input v-model="form.passwordConfirm" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('form')" :disabled="lodding">修改</el-button>
        <el-button @click="resetForm('form')">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters, mapState } from 'vuex'
import { Component, Prop, Watch } from 'vue-property-decorator'
import { resetPasswordApi } from '@/api/http/userApi'

@Component({
  computed: {
    ...mapState('dialogs', ['passwordReset'])
  }
})
export default class DialogPasswordReset extends Vue {
  passwordReset: any
  form = {
    password: '',
    passwordConfirm: ''
  }

  lodding = false

  @Watch('passwordReset')
  async function () {
    this.form = {
      password: '',
      passwordConfirm: ''
    }
  }

  cancel () {
    this.$store.commit('dialogs/ADD_CUSTOMER', false)
  }

  async resetPassword () {
    const res = await resetPasswordApi(this.form)
    if ((res as any).status === 200) {
      this.$message({
        message: '修改成功',
        type: 'success'
      })
      this.$emit('added')
    } else {
      this.$message.error({
        message: '修改失败'
      })
    }
  }

  async submitForm (formName: string) {
    if (this.form.password.length < 6) {
      this.$message.error({
        message: '密码过短'
      })
      return false
    }
    console.log(this.form.password)
    console.log(this.form.passwordConfirm)
    console.log(this.form.passwordConfirm === this.form.password)
    console.log(typeof this.form.password)
    console.log(typeof this.form.passwordConfirm)
    if (this.form.password !== this.form.passwordConfirm) {
      this.$message.error({
        message: '两次输入密码不一样'
      })
      return false
    }
    this.lodding = true
    await this.resetPassword()
    this.$store.commit('dialogs/RESET_PASSWORD', false)
    this.lodding = false
  }

  resetForm (formName: string|number) {
    this.form = {
      password: '',
      passwordConfirm: ''
    }
  }
}
</script>
