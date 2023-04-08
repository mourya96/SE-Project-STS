import query_view from "./CDN_Components/query_view.js";
import student_dashboard from "./CDN_Components/student_dashboard.js";
import subject_dashboard from "./CDN_Components/subject_dashboard.js";

const routes = [
    { path: '/', component: student_dashboard, name: 'Student Dashboard' },
    { path: '/subject/:subject', component: subject_dashboard, name: 'Subject Dashboard' },
    { path: '/ticket/:ticket_id', component: query_view, name: 'Query View' },
]
const router = VueRouter.createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: VueRouter.createWebHashHistory(),
    routes,
})
Vue.createApp({}).use(router).mount('#app')