import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import FertilizerOptimizer from '@/components/FertilizerOptimizer'
import AddFertilizer from '@/components/AddFertilizer'
// import dialog1 from '@/components/dialog1'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/optimize',
      name: 'FertilizerOptimizer',
      component: FertilizerOptimizer
    },
    {
      path: '/fertilizeradd',
      name: 'AddFertilizer',
      component: AddFertilizer
    }
    // {
    //   path: '/dialog1',
    //   name: 'dialog1',
    //   component: dialog1
    // }
  ]
})
