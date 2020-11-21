import Vue from 'vue'
import Vuex, { MutationTree, ActionTree, Module } from 'vuex'
import { StateIndex } from '..'

Vue.use(Vuex)

export interface StateDialogs {
  customerAdd: any;
  passwordReset: any;
}

const mutations: MutationTree<StateDialogs> = {
  ADD_CUSTOMER (state, payload) {
    state.customerAdd = payload
  },

  RESET_PASSWORD (state, payload) {
    state.passwordReset = payload
  }
}

const actions: ActionTree<StateDialogs, StateIndex> = {
}

// 命名规则：页面 + 对话框名字
export default {
  namespaced: true,
  state: {
    customerAdd: null,
    passwordReset: null
  } as StateDialogs,
  mutations,
  actions
} as Module<StateDialogs, StateIndex>
