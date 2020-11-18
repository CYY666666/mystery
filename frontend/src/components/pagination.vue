<template>
    <div class="pagination">
        <el-pagination
            :page-size="size"
            :current-page="page"
            :page-sizes="[20, 50, 100, 300]"
            :total="total"
            layout="total, prev, pager, next, sizes"
            @current-change="updatePage('page', $event)"
            @size-change="updatePage('size', $event)"
        >
        </el-pagination>
    </div>
</template>

<script>
export default {
  props: {
    total: {
      type: Number,
      default: 0
    },
    size: {
      type: Number,
      default: 20
    },
    page: {
      type: Number,
      default: 1
    }
  },
  methods: {
    updatePage (type, val) {
      this.$emit('chagnePage', type, val)
    }
  }
}
</script>

<style scope>
.pagination{
    text-align: right;
    margin: 15px;
}
</style>
