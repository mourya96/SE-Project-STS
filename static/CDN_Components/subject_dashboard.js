import navBar from "./navBar.js"
const subject_dashboard = {
    template: `
    <div>
        <link rel="stylesheet" href="../static/dashboard.css">

        <navB :title="title"></navB>
        <div v-if="!ready" class="text-center">
            <h1>Please wait Loading</h1>
        </div>
        <div v-else>
            <span class="btn-group btn-group-lg" style="margin-left: 20%;">
                <input type="radio" class="btn-check" value="faq" v-model="selectedOption" @change="FAQ" id="btnradio1">
                <label class="btn btn-outline-primary" for="btnradio1">FAQ</label>
            
                <input type="radio" class="btn-check" value="resolved" v-model="selectedOption" @change="RESOLVED" id="btnradio2">
                <label class="btn btn-outline-primary" for="btnradio2">Resolved</label>
            
                <input type="radio" class="btn-check" value="unresolved" v-model="selectedOption" @change="UNRESOLVED" id="btnradio3">
                <label class="btn btn-outline-primary" for="btnradio3">Unresolved</label>
            </span>
            <span>
                <input class="search" type="text" id="search" placeholder="Search here...." v-model="search">
                <button type="button" class="btn btn-link" @click="search_function"><i class="bi bi-search"></i></button>
            </span>
            <h3 class="text-center" v-if="!ticket_list.length">No tickets found under this section.</h3>
            <div class="row p-1" v-for="ticket in ticket_list">
                <div class="card position-relative " style="width:60%; margin:auto; min-height:4em">
                    <div style="font-size:2.5em;" class="position-absolute">
                        {{ticket.likes}}
                    </div>
                    <div style="font-size: 1.5em; width:90%; margin-left:2.5em" class="mt-1">
                        <div v-if="ticket.sec_name">
                            <span class="badge bg-primary">{{ticket.sec_name}}</span><br>
                        </div>
                        <router-link :to="'/ticket/'+ticket.ticket_id">{{ticket.title}}</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    data() {
        return {
            subject_name: this.$route.params.subject,
            title: "Subject Dashboard",
            ticket_list: [],
            search: '',
            selectedOption: 'faq',
            ready: false
        }
    },
    components: {
        'navB': navBar
    },
    methods: {
        search_function() {
            alert(this.search)
        },
        FAQ() {
            this.ready = false
            fetch(`/api/subject/${this.subject_name}?FAQ=True`)
                .then(res => res.json())
                .then(data => {
                    this.ticket_list = data
                    this.ready = true
                })
        },
        RESOLVED() {
            this.ready = false
            fetch(`/api/subject/${this.subject_name}?ResolvedStatus=True`)
                .then(res => res.json())
                .then(data => {
                    this.ticket_list = data
                    this.ready = true
                })
        },
        UNRESOLVED() {
            this.ready = false
            fetch(`/api/subject/${this.subject_name}?ResolvedStatus=False`)
                .then(res => res.json())
                .then(data => {
                    this.ticket_list = data
                    this.ready = true
                })
        },
    },
    beforeMount() {
        this.FAQ()
    },
    // beforeCreate() {
    //     if (!localStorage.getItem('access-token')) {
    //         alert('plz login first')
    //         // return this.$router.push('/login')
    //     }
    // }
}
export default subject_dashboard