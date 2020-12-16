/* eslint-disable vue/no-unused-components */
<template>
  <div>
    <el-button type="primary" style="float:left" @click="addCustomer">添加<i class="el-icon-circle-plus-outline"></i></el-button>
    <el-button type="primary" style="float:left" @click="continueTask">继续<i class="el-icon-arrow-right"></i></el-button>
    <el-button type="primary" style="float:right" @click="resetPassword">修改密码<i class="el-icon-setting"></i></el-button>
    <el-button type="primary" style="float:right" @click="calculateTotalMark">计算总分<i class="el-icon-s-data"></i></el-button>
    <el-select v-model="currentUserId" placeholder="只看">
      <el-option
        v-for="user in users"
        :key="user.id"
        :label="user.username"
        :value="user.id">
      </el-option>
    </el-select>
    <el-table
      :data="customerList"
      style="width: 100%"
      :row-key="getRowKey"
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"
        :reserve-selection="true"
        width="55">
      </el-table-column>
      <el-table-column
        prop="remark"
        label="昵称">
      </el-table-column>
      <el-table-column
        prop="create_at"
        label="创建时间"
        :formatter="dateFormat">
      </el-table-column>
      <el-table-column
        prop="got_mark"
        label="已刷分数">
      </el-table-column>
      <el-table-column
        prop="total_mark"
        label="总分">
      </el-table-column>
      <el-table-column
        prop="subject_id"
        label="科目">
        <template v-slot="{row: { subject_id }}">
          <span>{{ subjectInfo[subject_id] }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="username"
        label="创建者">
      </el-table-column>
      <el-table-column
        prop="accuracy"
        label="正确率">
      </el-table-column>
      <el-table-column
        label="url">
        <template v-slot="{row}">
          <el-tooltip placement="top" effect="light" v-if="row.url">
            <i class="el-icon-view" style="font-size: 24px; color: #409EFF; cursor: pointer" @click="copyUrl(row.url)"></i>
            <div slot="content">{{row.url}}</div>
          </el-tooltip>
          <span v-else>无</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-size=pageSize
      layout="prev, pager, next, jumper"
      :total=totalPage>
    </el-pagination>
    <dialog-customer-add @added="added"/>
    <dialog-password-reset />
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Vue, Watch } from 'vue-property-decorator'
import MenuAside from '../components/menu.vue'
import pagination from '../components/pagination.vue'
import { getAllCustomer, restartTask } from '../api/http/customerApi'
import { getInfo } from '../api/http/infoApi'
import { getAllUsersApi } from '../api/http/userApi'
import DialogCustomerAdd from '@/components/dialogs/customer-add.vue'
import DialogPasswordReset from '@/components/dialogs/reset-password.vue'
import dayjs from 'dayjs'

@Component({
  components: {
    MenuAside,
    pagination,
    DialogCustomerAdd,
    DialogPasswordReset
  }
})
export default class Customer extends Vue {
  customerList = []
  nowMenu: number | undefined
  currentPage = 1
  totalPage = 1
  pageSize = 20
  change = null
  subjectInfo = {}
  timer: any = null
  multipleSelection = []
  users = []
  currentUserId = null

  @Watch('currentPage')
  @Watch('change')
  @Watch('currentUserId')
  async getAllCustomerData () {
    const skip = (this.currentPage - 1) * this.pageSize
    try {
      // eslint-disable-next-line quote-props
      const res = await getAllCustomer({ skip: skip, limit: this.pageSize, 'user_id': this.currentUserId })
      this.customerList = (res as any).data.data.items as any
      this.totalPage = Number((res as any).data.data.info.items_count)
    } catch (err) {
      return this.$router.push({ name: 'Login' })
    }
  }

  async added () {
    await this.getAllCustomerData()
  }

  getRowKey (row: any) {
    return row.id
  }

  handleSizeChange (val: number) {
    console.log(`每页 ${val} 条`)
  }

  handleCurrentChange (val: number) {
    this.currentPage = val
  }

  dateFormat (row: any, column: any) {
    const date = row[column.property] * 1000
    return dayjs(date).format('YYYY-MM-DD HH:mm')
  }

  calculateTotalMark () {
    if (!this.multipleSelection.length) {
      this.$message.warning({
        message: '未选中'
      })
      return
    }
    this.$message.success({
      message: '一共' + this.multipleSelection.reduce((totalMark: number, item: any) => totalMark + item.total_mark, 0) + '分'
    })
    return this.multipleSelection.reduce((totalMark: number, item: any) => totalMark + item.total_mark, 0)
  }

  addCustomer () {
    const lst = []
    for (const key of Object.keys(this.subjectInfo)) {
      lst.push({
        id: Number(key),
        name: (this.subjectInfo as any)[key]
      })
    }
    this.$store.commit('dialogs/ADD_CUSTOMER', lst)
  }

  resetPassword () {
    this.$store.commit('dialogs/RESET_PASSWORD', true)
  }

  async continueTask () {
    if (!this.multipleSelection.length) {
      this.$message.warning({
        message: '未选中'
      })
      return
    }
    const customerIdList = []
    for (const i of this.multipleSelection) {
      customerIdList.push((i as any).id)
    }
    // eslint-disable-next-line quote-props
    const res = await restartTask({ 'customer_id_list': customerIdList })
    if ((res as any).status === 200) {
      this.$message({
        message: '成功',
        type: 'success'
      })
    } else {
      this.$message.error({
        message: '失败'
      })
    }
  }

  handleSelectionChange (val: any) {
    this.multipleSelection = val
  }

  async getSubjectInfo () {
    const res = await getInfo()
    this.subjectInfo = (res as any).data
  }

  async getAllUsers () {
    const res = await getAllUsersApi()
    this.users = (res as any).data.data
  }

  async intervalGetData () {
    this.timer = setInterval(async () => {
      await this.getAllCustomerData()
    }, 1000 * 12)
  }

  copyUrl (url: string) {
    const inputDom: any = document.createElement('input')
    inputDom.value = url
    document.body.appendChild(inputDom)
    inputDom.select()
    if (document.execCommand('copy')) {
      this.$message.success('复制成功！')
    }
    inputDom.parentNode.removeChild(inputDom)
  }

  destroyed () {
    clearInterval(this.timer)
  }

  async created () {
    await this.getAllCustomerData()
    await this.getSubjectInfo()
    await this.intervalGetData()
    await this.getAllUsers()
  }
}
</script>
