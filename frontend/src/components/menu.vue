<template>
    <div class="menuBox">
        <el-menu
            default-active="all"
            class="menu"
            text-color="#000"
            active-text-color="#e20000"
            @select="handleSelect"
        >
            <el-menu-item index="all">全部</el-menu-item>
            <el-menu-item
                :index="item.id.toString()"
                v-for="item in menuList" :key="item.id"
            >{{item.name}}</el-menu-item>
        </el-menu>
    </div>
</template>

<script>
export default {
  props: {
    menuList: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      now: ''
    }
  },
  methods: {
    handleSelect (sel) {
      this.$emit('menuSelectOk', sel)
    }
  }
}
</script>

<style scope>
.menuBox{
    height: 100%;
}
.menu{
    height: 100%;
    text-align: center;
}
.el-menu-item.is-active {
    background-color: #f7e4ea!important;
}
</style>
