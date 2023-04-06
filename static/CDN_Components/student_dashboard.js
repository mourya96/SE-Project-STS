const student_dashboard = {
    template: `
    <div>
        <h1 class="text-center">Student Dashboard</h1>
        <div class="position-relative" style="margin-left: 3%; margin-right: 3%;">
            <h3 class=" ms-3">Welcome {{username}}</h3>
            <div class="text-end me-1 position-absolute top-0 end-0">
                <button @click="logout" style="font-size: large;" class="btn btn-info">
                    Logout <i class="bi bi-box-arrow-right"></i>
                </button>
            </div>
            <hr>
        </div>
        <div v-if="!ready">
            <h1>Please wait Loading</h1>
        </div>
        <div class="row" v-else>
            <div class="col-sm-4" v-for="(faq, subject) in subjects" :key="subject">
                <div class="card position-relative " style="margin-left: 5%; margin-right: 5%;">
                    <div class="card-body dark-mode">
                        <h3 class="card-title text-center">{{subject}}</h3>
                        <hr class="ms-3">
                        <ul v-for="title in faq" :key="title">
                            <li class="card-title">{{title}}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    data() {
        return {
            username: 'student',
            subjects: {},
            ready: false,
            darkMode: false
        }
    },
    methods: {
        logout() {
            fetch('/logout')
                .then(res => {
                    if (res.ok) {
                        alert("Logout Successfully")
                        window.localStorage.clear()
                    } else {
                        alert("Error occured during logout")
                    }
                })
        }
    },
    beforeMount() {
        this.subjects = {
            'MLT': ['faq.title1', 'faq.title2', 'faq.title3'],
            'BDM': ['faq.title1', 'faq.title2', 'faq.title3', 'faq.title4'],
            'BA': ['faq.title1', 'faq.title2'],
            'PDSA': ['faq.title1',],
        }
        this.ready = true
    }
}

export default student_dashboard