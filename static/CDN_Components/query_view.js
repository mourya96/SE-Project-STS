import navBar from "./navBar.js"
const query_view = {
    template: `
    <div>        
        <navB :title="title"></navB>
        <h1 class="text-center">{{this.$route.params.ticket_id}}</h1>
    </div>`,
    data() {
        return {
            username: 'student',
            title: "Query View",
            ticket: {}
        }
    },
    components: {
        'navB': navBar
    },
}
export default query_view