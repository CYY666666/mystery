<template>
  <el-dialog
    title=添加客户
    v-if="Boolean(customerAdd)"
    :visible="Boolean(customerAdd)"
    :before-close="cancel"
    width="55%">
    <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="demo-ruleForm">
  <el-form-item label="正确率" prop="accuracy" required>
    <el-input v-model.number="form.accuracy"></el-input>
  </el-form-item>
  <el-form-item label="昵称" prop="remark">
    <el-input v-model="form.remark"></el-input>
  </el-form-item>
  <el-form-item label="总分" prop="total_mark" required>
    <el-input v-model.number="form.total_mark"></el-input>
  </el-form-item>
  <el-form-item label="url" prop="url" required>
    <el-input v-model="form.url" type="textarea"></el-input>
  </el-form-item>
  <el-form-item label="科目" required>
    <el-radio-group v-model="form.subject_id">
      <el-radio
        v-for="subject in subjects"
        :label="subject.id"
        :key="subject.id"
        :value="subject.id"
        style="width: 300px;">
        {{ subject.name }}
      </el-radio>
    </el-radio-group>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="submitForm('form')" :disabled="lodding">立即创建</el-button>
    <el-button @click="resetForm('form')">重置</el-button>
  </el-form-item>
</el-form>
  </el-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters, mapState } from 'vuex'
import { Component, Prop, Watch } from 'vue-property-decorator'
import { insertCustomer } from '@/api/http/customerApi'
import { getInfo } from '@/api/http/infoApi'

@Component({
  computed: {
    ...mapState('dialogs', ['customerAdd'])
  }
})
export default class DialogCustomerAdd extends Vue {
  customerAdd: any
  form = {
    accuracy: 80,
    remark: null,
    // eslint-disable-next-line quote-props
    'subject_id': null,
    // eslint-disable-next-line quote-props
    'total_mark': 500,
    url: null
  }

  subjects: any = []

  lodding = false

  rules = {
    accuracy: [
      { required: true, message: '请输入正确率', trigger: 'blur', type: 'number' },
      { min: 60, max: 100, message: '正确率在60到100之间', trigger: 'blur', type: 'number' }
    ],
    // eslint-disable-next-line quote-props
    'subject_id': [
      { required: true, message: '请选择科目', trigger: 'change' }
    ],
    // eslint-disable-next-line quote-props
    'total_mark': [
      { required: true, message: '请输入分数', trigger: 'blur', type: 'number' },
      { min: 100, max: 1000, message: '分数在100到1000之间', trigger: 'blur', type: 'number' }
    ],
    url: [
      { required: true, message: '请输入url', trigger: 'blur' }
    ]
  }

  @Prop()
  changed: any

  @Watch('customerAdd')
  async function () {
    this.subjects = this.customerAdd
    this.lodding = false
  }

  cancel () {
    this.$store.commit('dialogs/ADD_CUSTOMER', false)
  }

  async newCustomer () {
    const res = await insertCustomer(this.form)
    if ((res as any).status === 200) {
      this.$message({
        message: '添加成功',
        type: 'success'
      })
      this.$emit('added')
    } else {
      this.$message.error({
        message: 'url重复'
      })
    }
  }

  async submitForm (formName: string) {
    (this as any).$refs[formName].validate(async (valid: any) => {
      if (!this.form.subject_id) {
        this.$message.error({
          message: '未选择科目'
        })
        return false
      }
      if (valid) {
        this.lodding = true
        await this.newCustomer()
        this.$store.commit('dialogs/ADD_CUSTOMER', false)
        this.lodding = false
      } else {
        this.$message.error({
          message: '失败'
        })
        return false
      }
    })
  }

  resetForm (formName: string|number) {
    (this as any).$refs[formName].resetFields()
    this.form = {
      accuracy: 80,
      remark: null,
      // eslint-disable-next-line quote-props
      'subject_id': null,
      // eslint-disable-next-line quote-props
      'total_mark': 500,
      url: null
    }
  }
}
</script>
