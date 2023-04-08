import navBar from "./navBar.js"
const student_dashboard = {
    template: `
    <div>
        <link rel="stylesheet" href="../static/dashboard.css">
        
        <navB :title="title"></navB>
        <div v-if="!ready">
            <h1>Please wait Loading</h1>
        </div>
        <div class="row" v-else>
            <div class="col-sm-4" v-for="(faq, subject) in subjects" :key="subject">
                <div class="card" style="margin-left: 5%; margin-right: 5%;">
                    <div class="card-body ">
                        <router-link :to="'/subject/'+subject"><h3 class="card-title text-center">{{subject}}</h3></router-link>
                        <hr class="ms-3">
                        <div v-if="faq.length == 0" class="text-center">
                            <router-link :to="'/subject/'+subject">Click Here to view all the tickets of this subject</router-link>
                        </div>
                        <div v-else>
                            <ul v-for="ticket in faq" :key="title">
                                <router-link :to="'/ticket/'+ticket.ticket_id"> <li class="card-title">{{ticket.title}}</li></router-link>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    data() {
        return {
            username: 'student',
            title: "Student Dashboard",
            subjects: {},
            ready: false,
            darkMode: false
        }
    },
    components: {
        'navB': navBar
    },
    methods: {
    },
    beforeMount() {
        fetch('/api/tag/subject')
            .then(res => res.json())
            .then(data => {
                const subject_names = data.map(x => x.subject_name)
                // subject_names=['MLT', 'BDM', 'BA'] (output format)
                for (const subject of subject_names) {
                    fetch(`/api/subject/${subject}?FAQ=True&limit=5`)
                        .then(res => res.json())
                        .then(data => this.subjects[subject] = data)
                }
            }).catch(err => console.log(err))
        this.ready = true
    },
    // beforeCreate() {
    //     if (!localStorage.getItem('access-token')) {
    //         alert('plz login first')
    //         // return this.$router.push('/login')
    //     }
    // }
}

export default student_dashboard