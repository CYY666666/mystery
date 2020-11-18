import Vue from 'vue'
import Vuex, { ActionTree, MutationTree } from 'vuex'
import dialogs, { StateDialogs } from './modules/dialogs'

Vue.use(Vuex)

export interface StateIndex {
  dialogs: StateDialogs;
}

const mutations: MutationTree<StateIndex> = {
}

const actions: ActionTree<StateIndex, any> = {
}

export default new Vuex.Store({
  modules: {
    dialogs
  },
  state: {
  } as StateIndex,
  mutations,
  actions
})
