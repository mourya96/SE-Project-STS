import student_dashboard from "./CDN_Components/student_dashboard.js";

const routes = [
    { path: '/', component: student_dashboard, name: 'student-dashboard' }
]
const router = VueRouter.createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: VueRouter.createWebHashHistory(),
    routes,
})
Vue.createApp({}).use(router).mount('#app')