/* eslint-disable vue/no-unused-components */
<template>
  <div>
    <el-button type="primary" style="float:left" @click="addCustomer">添加<i class="el-icon-circle-plus-outline"></i></el-button>
    <el-table
      :data="customerList"
      style="width: 100%">
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
      :page-size="20"
      layout="prev, pager, next, jumper"
      :total=totalPage>
    </el-pagination>
    <dialog-customer-add @added="added"/>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Vue, Watch } from 'vue-property-decorator'
import MenuAside from '../components/menu.vue'
import pagination from '../components/pagination.vue'
import { getAllCustomer } from '../api/http/customerApi'
import { getInfo } from '../api/http/infoApi'
import DialogCustomerAdd from '@/components/dialogs/customer-add.vue'
import dayjs from 'dayjs'

@Component({
  components: {
    MenuAside,
    pagination,
    DialogCustomerAdd
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

  @Watch('currentPage')
  @Watch('change')
  async getAllCustomerData () {
    const skip = (this.currentPage - 1) * this.pageSize
    const res = await getAllCustomer({ skip: skip, limit: this.pageSize })
    this.customerList = (res as any).data.data.items as any
    this.totalPage = (res as any).data.data.info.page_count
  }

  async added () {
    await this.getAllCustomerData()
  }

  handleSizeChange (val: number) {
    console.log(`每页 ${val} 条`)
  }

  handleCurrentChange (val: number) {
    this.currentPage = val
    this.getAllCustomerData()
  }

  dateFormat (row: any, column: any) {
    const date = row[column.property] * 1000
    return dayjs(date).format('YYYY-MM-DD HH:mm')
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

  async getSubjectInfo () {
    const res = await getInfo()
    this.subjectInfo = (res as any).data
  }

  async intervalGetData () {
    this.timer = setInterval(async () => {
      await this.getAllCustomerData()
    }, 1000 * 5)
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
  }
}
</script>
